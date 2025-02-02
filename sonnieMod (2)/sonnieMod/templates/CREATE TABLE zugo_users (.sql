CREATE TABLE zugo_users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    account_status ENUM('ACTIVE', 'SUSPENDED', 'INACTIVE') DEFAULT 'ACTIVE',
    verification_status BOOLEAN DEFAULT FALSE
);

INSERT INTO users (username, email) VALUES
('john', 'john@example.com'),
('jane', 'jane@example.com');
INSERT INTO transactions (user_id, transaction_type, amount) VALUES
(1, 'deposit', 100.0000),
(2, 'withdrawal', 50.0000);