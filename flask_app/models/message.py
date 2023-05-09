from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, session
import re

MSG_REGEX = re.compile(r'^\s*$')

class Message:
    DB = 'msg_coding_dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.sender = data['sender']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def send_message(cls, data):
        query = '''
            INSERT 
            INTO messages(content, receiver_id, sender_id)
            VALUES ( %(content)s, %(receiver_id)s, %(sender_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_message(cls, data):
        query = '''
            DELETE 
            FROM messages
            WHERE id = %(msg_id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_inbox_messages(cls, data):
        all_messages = []
        query = '''
            SELECT *
            FROM messages
            JOIN users ON users.id = messages.sender_id
            WHERE messages.receiver_id = %(id)s
            ORDER BY messages.created_at DESC; 
        '''
        
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return all_messages
        for row in results:
            sender_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            sender = user.User(sender_info)

            message_info = {
                'id': row['id'],
                'content': row['content'],
                'sender': sender,
                'receiver': session['id'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }

            all_messages.append(cls(message_info))
        
        return all_messages
    
    @staticmethod
    def validate_message(message):
        is_valid = True
        if len(message['content']) == 0 or MSG_REGEX.match(message['content']):
            flash('Message cannot be empty!', 'msg_error')
            is_valid = False

        return is_valid
    