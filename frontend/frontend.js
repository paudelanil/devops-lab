const express = require('express');
const app = express();
const path = require('path');
const http = require('http');
const server = http.createServer(app);
const axios = require('axios');

// Define constants
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// Route for index page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Route for chat page
app.get('/chat', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'chat.html'));
});

// API route to get a new user ID from the backend
app.get('/api/new-user', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/new-user`);
    res.json(response.data);
  } catch (error) {
    console.error('Error getting new user ID:', error);
    res.status(500).json({ error: 'Failed to get new user ID' });
  }
});

// Start the server
server.listen(PORT, () => {
  console.log(`Frontend server running on port ${PORT}`);
});