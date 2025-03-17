CREATE DATABASE IF NOT EXISTS chat_db;
USE chat_db;

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id VARCHAR(100) NOT NULL,
    receiver_id VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);

-- Add indexes for faster queries
CREATE INDEX idx_sender_id ON messages (sender_id);
CREATE INDEX idx_receiver_id ON messages (receiver_id);
CREATE INDEX idx_timestamp ON messages (timestamp);