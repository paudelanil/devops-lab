const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const BACKEND_SERVICE_URL = "http://backend:5000";

// Serve static files from public directory
app.use(express.static('public'));

// Verify static files serving
app.get('/styles.css', (req, res) => {
    res.sendFile(__dirname + '/public/styles.css');
});

app.get('/', async (req, res) => {
    try {
        const response = await axios.get(`${BACKEND_SERVICE_URL}/blogs`);
        const blogs = response.data;
        const html = `
            <html>
            <head>
                <title>Blog List</title>
                <h1> DevOps Project WOrk </h1>
                <link rel="stylesheet" href="/styles.css" />
            </head>
            <body>
                <div class="container">
                    <h1>Blog List</h1>
                    <ul class="blog-list">
                        ${blogs.map(blog => `
                            <li class="blog-item">
                                <strong>${blog.title}</strong>: ${blog.content}
                                <form action="/delete/${blog.id}" method="POST" class="delete-form">
                                    <button type="submit" class="delete-button">Delete</button>
                                </form>
                            </li>
                        `).join('')}
                    </ul>
                    <form action="/create" method="POST" class="blog-form">
                        <input name="title" placeholder="Title" required class="input-field"/>
                        <textarea name="content" placeholder="Content" required class="input-field"></textarea>
                        <button type="submit" class="submit-button">Create Blog</button>
                    </form>
                </div>
            </body>
            </html>
        `;
        res.send(html);
    } catch (error) {
        res.status(500).send("Error fetching blogs");
    }
});

app.post('/create', async (req, res) => {
    try {
        const { title, content } = req.body;
        await axios.post(`${BACKEND_SERVICE_URL}/blogs`, { title, content });
        res.redirect('/');
    } catch (error) {
        res.status(500).send("Error creating blog");
    }
});

app.post('/delete/:id', async (req, res) => {
    try {
        const { id } = req.params;
        await axios.delete(`${BACKEND_SERVICE_URL}/blogs/${id}`);
        res.redirect('/');
    } catch (error) {
        res.status(500).send("Error deleting blog");
    }
});

app.listen(3000, () => {
    console.log("Frontend running on http://localhost:3000");
});
