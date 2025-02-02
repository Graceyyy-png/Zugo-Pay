from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import bcrypt
import re
import secrets
import logging
from datetime import datetime, timedelta
import os


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

class ZugoApp:
    def __init__(self):
      
        self.app = Flask(__name__, 
                         static_folder='static', 
                         template_folder='templates')
        
       
        self.app.secret_key = secrets.token_hex(32)
        
       
        CORS(self.app, resources={
            r"/*": {
                "origins": "*",
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        })
        
       
        self.db_config = self.get_database_config()
        
        
        self.register_routes()
        
       
        self.initialize_database()
    
    def get_database_config(self):
        """
        Retrieve database configuration 
        Recommended to use environment variables or a config file
        """
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'zugo_database'),
            'user': os.getenv('DB_USER', 'root'),  
            'password': os.getenv('DB_PASSWORD', ''), 
        }
    
    def get_db_connection(self):
        """Create a database connection with comprehensive error handling"""
        try:
           
            print("Attempting to connect with config:", self.db_config)
            
            connection = mysql.connector.connect(**self.db_config)
            
            if connection.is_connected():
                print("Database connection successful")
                return connection
            else:
                print("Failed to establish database connection")
                return None
        
        except mysql.connector.Error as e:
           
            logging.error(f"Database Connection Error: {e}")
            print(f"Detailed Connection Error: {e}")
            
           
            if e.errno == 1045:
                print("Access denied. Check your username and password.")
            elif e.errno == 1049:
                print("Unknown database. Ensure the database exists.")
            elif e.errno == 2005:
                print("Unknown MySQL server host.")
            
            return None
        except Exception as e:
            logging.error(f"Unexpected error connecting to database: {e}")
            print(f"Unexpected Connection Error: {e}")
            return None
    
    def initialize_database(self):
        """Create necessary database tables with robust error handling"""
        connection = None
        try:
           
            connection = self.get_db_connection()
            
          
            if connection is None:
                logging.error("Cannot initialize database: No database connection")
                return
            
            cursor = connection.cursor()

         
            cursor.execute("CREATE DATABASE IF NOT EXISTS zugo_database")
            cursor.execute("USE zugo_database")

           
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('user', 'admin', 'moderator') DEFAULT 'user',
                is_verified BOOLEAN DEFAULT FALSE,
                verification_token VARCHAR(100),
                verification_token_expires DATETIME,
                last_login TIMESTAMP NULL,
                failed_login_attempts INT DEFAULT 0,
                account_locked_until DATETIME NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

           
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                transaction_type VARCHAR(50),
                amount DECIMAL(10,2),
                status VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            ''')

           
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS wallets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                wallet_type VARCHAR(50),
                wallet_address VARCHAR(255),
                balance DECIMAL(10,2) DEFAULT 0,
                is_primary BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            ''')

            connection.commit()
            logging.info("Database tables created successfully")
        
        except mysql.connector.Error as e:
            logging.error(f"Database Initialization Error: {e}")
            print(f"Database Initialization Error: {e}")
        
        except Exception as e:
            logging.error(f"Unexpected error during database initialization: {e}")
            print(f"Unexpected Initialization Error: {e}")
        
        finally:
           
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
                print("Database connection closed")

  


if __name__ == '__main__':
    try:
        app_instance = ZugoApp()
        app_instance.app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logging.error(f"Application startup error: {e}")
        print(f"Startup Error: {e}")