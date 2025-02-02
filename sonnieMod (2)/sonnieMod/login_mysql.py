import os
import hashlib
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='zugo_database',
            user='your_username',
            password='your_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def create_database():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            role ENUM('user', 'admin') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

      
      def hash_password(password):
            return hashlib.sha256(password.encode()).hexdigest()

       
        sample_users = [
            ('admin@zugo.com', hash_password('ZugoAdmin2023!'), 'Admin', 'User', 'admin'),
            ('user@zugo.com', hash_password('ZugoUser2023!'), 'John', 'Doe', 'user')
        ]

       
        insert_query = '''
        INSERT IGNORE INTO users 
        (email, password, first_name, last_name, role) 
        VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.executemany(insert_query, sample_users)
        
        connection.commit()
        print("Database and users created successfully")

    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

   
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

      
        query = 'SELECT * FROM users WHERE email = %s AND password = %s'
        cursor.execute(query, (email, hashed_password))
        user = cursor.fetchone()

        if user:
          
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']

            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'role': user['role']
                },
                'redirect': '/admin-dashboard' if user['role'] == 'admin' else '/user-dashboard'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred'
        }), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


create_database()

if __name__ == '__main__':
    app.run(debug=True)