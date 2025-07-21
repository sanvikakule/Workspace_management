import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                address TEXT NOT NULL,
                email TEXT NOT NULL,
                qualification TEXT NOT NULL,
                phone TEXT NOT NULL,
                employee_id TEXT UNIQUE NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                assigned_to TEXT NOT NULL,
                assigned_by TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_to) REFERENCES users(username),
                FOREIGN KEY (assigned_by) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_by TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uploaded_by) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                organizer TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (organizer) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meeting_participants (
                meeting_id INTEGER,
                username TEXT,
                PRIMARY KEY (meeting_id, username),
                FOREIGN KEY (meeting_id) REFERENCES meetings(meeting_id),
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                logout_time TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        self.conn.commit()

    def verify_login(self, username, password, role):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ? AND role = ?',
                      (username, password, role))
        return cursor.fetchone() is not None

    def register_user(self, user_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password, role, name, age, address, email, 
                                 qualification, phone, employee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['username'],
                user_data['password'],
                user_data['role'],
                user_data['name'],
                user_data['age'],
                user_data['address'],
                user_data['email'],
                user_data['qualification'],
                user_data['phone'],
                user_data['employee_id']
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_users_with_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT u.*, COUNT(t.task_id) as task_count
            FROM users u
            LEFT JOIN tasks t ON u.username = t.assigned_to
            WHERE u.role = 'user'
            GROUP BY u.username
        ''')
        return cursor.fetchall()

    def remove_user(self, username):
        try:
            cursor = self.conn.cursor()
            # First delete associated tasks
            cursor.execute('DELETE FROM tasks WHERE assigned_to = ?', (username,))
            # Then delete associated files
            cursor.execute('DELETE FROM files WHERE username = ?', (username,))
            # Finally delete the user
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def assign_task(self, task_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (assigned_by, assigned_to, task_title, task_description, 
                                 due_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                task_data['assigned_by'],
                task_data['assigned_to'],
                task_data['task_title'],
                task_data['task_description'],
                task_data['due_date'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get_user_tasks(self, username):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT t.*, u.name as assigned_by_name 
            FROM tasks t 
            JOIN users u ON t.assigned_by = u.username 
            WHERE t.assigned_to = ?
            ORDER BY t.created_at DESC
        ''', (username,))
        return cursor.fetchall()

    def update_task_status(self, task_id, status):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE tasks 
                SET status = ? 
                WHERE task_id = ?
            ''', (status, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def submit_file(self, username, filename, filetype):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO files (username, filename, filetype, uploaded_at)
                VALUES (?, ?, ?, ?)
            ''', (
                username,
                filename,
                filetype,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get_user_details(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            return cursor.fetchone()
        except sqlite3.Error:
            return None

    def update_user_profile(self, user_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET name = ?, age = ?, address = ?, email = ?, 
                    qualification = ?, phone = ?
                WHERE username = ?
            ''', (
                user_data['name'],
                user_data['age'],
                user_data['address'],
                user_data['email'],
                user_data['qualification'],
                user_data['phone'],
                user_data['username']
            ))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def schedule_meeting(self, meeting_data):
        try:
            cursor = self.conn.cursor()
            # Insert meeting details
            cursor.execute('''
                INSERT INTO meetings (title, description, date, time, organizer, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                meeting_data['title'],
                meeting_data['description'],
                meeting_data['date'],
                meeting_data['time'],
                meeting_data['organizer'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            # Get the meeting_id of the inserted meeting
            meeting_id = cursor.lastrowid
            
            # Insert participants
            for participant in meeting_data['participants']:
                cursor.execute('''
                    INSERT INTO meeting_participants (meeting_id, username)
                    VALUES (?, ?)
                ''', (meeting_id, participant))
            
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get_user_meetings(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT m.*, u.name as organizer_name,
                       GROUP_CONCAT(p.username) as participants
                FROM meetings m
                JOIN users u ON m.organizer = u.username
                LEFT JOIN meeting_participants mp ON m.meeting_id = mp.meeting_id
                LEFT JOIN users p ON mp.username = p.username
                WHERE m.organizer = ? OR mp.username = ?
                GROUP BY m.meeting_id
                ORDER BY m.date, m.time
            ''', (username, username))
            return cursor.fetchall()
        except sqlite3.Error:
            return []

    def mark_attendance(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO attendance (username, login_time)
                VALUES (?, CURRENT_TIMESTAMP)
            ''', (username,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False

    def mark_logout(self, username):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE attendance 
                SET logout_time = CURRENT_TIMESTAMP
                WHERE username = ? AND logout_time IS NULL
            ''', (username,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error marking logout: {e}")
            return False

    def get_attendance_report(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT 
                    a.username,
                    u.name,
                    u.role,
                    a.login_time,
                    a.logout_time,
                    ROUND(CAST((JULIANDAY(COALESCE(a.logout_time, CURRENT_TIMESTAMP)) - JULIANDAY(a.login_time)) * 24 AS FLOAT), 2) as duration
                FROM attendance a
                JOIN users u ON a.username = u.username
                ORDER BY a.login_time DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting attendance report: {e}")
            return []

    def __del__(self):
        self.conn.close() 