from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL Configuration from Environment Variables
DB_HOST = os.getenv('DATABASE_HOST', 'database')
#DB_PORT = os.getenv('DATABASE_PORT', 3306)
DB_PORT = int(os.getenv('DATABASE_PORT', 3306))  # Ensure it's converted to an integer

DB_USER = os.getenv('DATABASE_USER', 'root')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'password')
DB_NAME = os.getenv('DATABASE_NAME', 'blog_db')

# Function to Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/blogs', methods=['GET'])
def get_blogs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blogs")
    blogs = cursor.fetchall()
    conn.close()
    return jsonify(blogs), 200

@app.route('/blogs', methods=['POST'])
def create_blog():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO blogs (title, content) VALUES (%s, %s)", (data['title'], data['content']))
    conn.commit()
    blog_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": blog_id, "title": data['title'], "content": data['content']}), 201

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blogs WHERE id = %s", (blog_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Blog deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

