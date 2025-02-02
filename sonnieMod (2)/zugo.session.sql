INSERT INTO zugo_users (
    user_id,
    username,
    email,
    phone,
    password_hash,
    created_at,
    last_login,
    account_status,
    verification_status
  )


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


CREATE INDEX idx_username ON zugo_users(username);
CREATE INDEX idx_email ON zugo_users(email);


CREATE TABLE user_wallets (
    wallet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    wallet_type VARCHAR(50),
    wallet_address VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES zugo_users(user_id)
);


CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    transaction_type VARCHAR(50),
    amount DECIMAL(19,4),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES zugo_users(user_id)
);


DELIMITER //

CREATE PROCEDURE register_user(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(255),
    IN p_phone VARCHAR(20),
    IN p_password VARCHAR(255)
)
BEGIN
    INSERT INTO zugo_users (
        username, 
        email, 
        phone, 
        password_hash
    ) VALUES (
        p_username,
        p_email,
        p_phone,
       
        SHA2(p_password, 256)
    );
END //

DELIMITER ;


CREATE INDEX idx_transaction_user ON transactions(user_id);
CREATE INDEX idx_transaction_date ON transactions(transaction_date);


CREATE INDEX idx_user_email ON zugo_users(email);
CREATE INDEX idx_user_phone ON zugo_users(phone);
CREATE INDEX idx_user_username ON zugo_users(username);


