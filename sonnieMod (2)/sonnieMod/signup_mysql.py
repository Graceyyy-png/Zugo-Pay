from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import re
import bcrypt
import secrets
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
CORS(app)


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='zugo_database',
            user='your_mysql_username',
            password='your_mysql_password'
        )
        return connection
    except Error as e:
        logging.error(f"Database Connection Error: {e}")
        return None


def create_users_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

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
        connection.commit()
        logging.info("Users table created successfully")
    except Error as e:
        logging.error(f"Error creating users table: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def validate_username(username):
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None

def validate_phone(phone):
    return re.match(r'^254\d{9}$', phone) is not None

def validate_password(password):
  
    return (
        len(password) >= 8 and 
        re.search(r'[A-Z]', password) and 
        re.search(r'[a-z]', password) and 
        re.search(r'\d', password) and 
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

  
    if not all([username, email, phone, password]):
        return jsonify({
            'success': False,
            'message': 'All fields are required'
        }), 400

  
    if not validate_username(username):
        return jsonify({
            'success': False,
            'message': 'Invalid username format'
        }), 400

    if not validate_email(email):
        return jsonify({
            'success': False,
            'message': 'Invalid email format'
        }), 400

    if not validate_phone(phone):
        return jsonify({
            'success': False,
            'message': 'Invalid phone number'
        }), 400

    if not validate_password(password):
        return jsonify({
            'success': False,
            'message': 'Password does not meet complexity requirements'
        }), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Check existing user
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = %s OR email = %s OR phone = %s
        ''', (username, email, phone))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username, email, or phone already exists'
            }), 409

       
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

       
        verification_token = secrets.token_urlsafe(32)
        token_expires = datetime.now() + timedelta(hours=24)

     
        insert_query = '''
        INSERT INTO users 
        (username, email, phone, password_hash, verification_token, verification_token_expires) 
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (
            username, 
            email, 
            phone, 
            password_hash, 
            verification_token, 
            token_expires
        ))
        connection.commit()

        # TODO: Send verification email with verification_token
        logging.info(f"User {username} registered successfully")

        return jsonify({
            'success': True,
            'message': 'Registration successful. Please check your email to verify your account.',
            'redirect': '/verify-email'
        }), 201

    except Error as e:
        logging.error(f"Signup error: {e}")
        return jsonify({
            'success': False,
            'message': 'Registration failed'
        }), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email and password are required'
        }), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

      
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401

       
        if user['account_locked_until'] and user['account_locked_until'] > datetime.now():
            return jsonify({
                'success': False,
                'message': 'Account temporarily locked. Try again later.'
            }), 403

      
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
          
            cursor.execute('''
                UPDATE users 
                SET failed_login_attempts = 0, 
                    last_login = CURRENT_TIMESTAMP,
                    account_locked_until = NULL 
                WHERE id = %s
            ''', (user['id'],))
            connection.commit()

           
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'role': user['role']
                },
                'redirect': '/dashboard'
            }), 200
        else:
            
            failed_attempts = (user ['failed_login_attempts'] + 1)
            cursor.execute('UPDATE users SET failed_login_attempts = %s WHERE id = %s', (failed_attempts, user['id']))
            connection.commit()

            
            if failed_attempts >= 5:
                lock_until = datetime.now() + timedelta(minutes=15)
                cursor.execute('UPDATE users SET account_locked_until = %s WHERE id = %s', (lock_until, user['id']))
                connection.commit()
                return jsonify({
                    'success': False,
                    'message': 'Account locked due to too many failed login attempts. Try again later.'
                }), 403

            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401

    except Error as e:
        logging.error(f"Login error: {e}")
        return jsonify({
            'success': False,
            'message': 'Login failed'
        }), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


@app.before_first_request
def initialize_database():
    create_users_table()

if __name__ == '__main__':
    app.run(debug=True, port=5000)