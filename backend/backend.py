import time
import sys

# At the beginning of your backend.py file
print("Waiting for database to be ready...")
time.sleep(10)  # Give MySQL some time to initialize

# backend.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import uvicorn
import random
import string
import mysql.connector
from mysql.connector import pooling
import json
import asyncio
from datetime import datetime

app = FastAPI()



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection pool
db_pool = pooling.MySQLConnectionPool(
    pool_name="chat_pool",
    pool_size=5,
    host="db",
    user="root",
    password="password",
    database="chat_db"
)

# Store active connections
active_connections: Dict[str, WebSocket] = {}
waiting_users: List[str] = []
active_chats: Dict[str, str] = {}  # Maps user_id to partner_id


def get_db_connection():
    return db_pool.get_connection()

def generate_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.on_event("startup")
async def startup_event():
    # Create tables if they don't exist
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id VARCHAR(100),
            receiver_id VARCHAR(100),
            message TEXT,
            timestamp DATETIME
        )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error during startup: {e}")
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the chat API"}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    
    # Add the connection to active connections
    active_connections[user_id] = websocket
    
    try:
        # Check if the user is already in a chat
        if user_id in active_chats:
            partner_id = active_chats[user_id]
            await websocket.send_json({"type": "connected", "partner_id": partner_id})
        else:
            # User is not in a chat, so add to waiting list
            waiting_users.append(user_id)
            await websocket.send_json({"type": "waiting"})
            
            # Try to match with another user
            await match_users()
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat_message":
                partner_id = active_chats.get(user_id)
                if partner_id and partner_id in active_connections:
                    # Send message to partner
                    message_content = message_data["message"]
                    await active_connections[partner_id].send_json({
                        "type": "chat_message",
                        "sender_id": user_id,
                        "message": message_content
                    })
                    
                    # Save message to database
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (%s, %s, %s, %s)",
                        (user_id, partner_id, message_content, datetime.now())
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
            elif message_data["type"] == "disconnect":
                await disconnect_chat(user_id)
    
    except WebSocketDisconnect:
        # Handle disconnection
        await disconnect_chat(user_id)
    finally:
        if user_id in active_connections:
            del active_connections[user_id]
        if user_id in waiting_users:
            waiting_users.remove(user_id)

async def match_users():
    """Match waiting users into pairs"""
    if len(waiting_users) >= 2:
        user1 = waiting_users.pop(0)
        user2 = waiting_users.pop(0)
        
        # Make sure users are still connected
        if user1 in active_connections and user2 in active_connections:
            # Create a chat between the two users
            active_chats[user1] = user2
            active_chats[user2] = user1
            
            # Notify both users
            await active_connections[user1].send_json({
                "type": "connected",
                "partner_id": user2
            })
            await active_connections[user2].send_json({
                "type": "connected",
                "partner_id": user1
            })

async def disconnect_chat(user_id: str):
    """Handle user disconnection from a chat"""
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        
        # Remove both users from active chats
        del active_chats[user_id]
        if partner_id in active_chats:
            del active_chats[partner_id]
        
        # Notify partner if they're still connected
        if partner_id in active_connections:
            await active_connections[partner_id].send_json({
                "type": "partner_disconnected"
            })

@app.get("/new-user")
async def create_new_user():
    user_id = generate_user_id()
    return {"user_id": user_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)