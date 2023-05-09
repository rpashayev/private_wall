from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^\s*$')

class User:
    DB = 'msg_coding_dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls, data):
        query = '''
            INSERT 
            INTO users(first_name, last_name, email, password)
            VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one_user(cls, data):
        query = '''
            SELECT *
            FROM users
            WHERE id = %(id)s;
        '''
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_by_email(cls,data):
        query = '''
            SELECT * 
            FROM users 
            WHERE email = %(email)s;
        '''
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_all_users(cls):
        users = []
        query = '''
                SELECT *
                FROM users;
        '''
        results = connectToMySQL(cls.DB).query_db(query)
        for user in results:
            users.append(cls(user))
        
        return users
    
    @classmethod
    def get_other_users(cls, data):
        users = []
        query = '''
                SELECT *
                FROM users
                WHERE id <> %(id)s
                ORDER BY users.first_name;
        '''
        results = connectToMySQL(cls.DB).query_db(query,data)
        for user in results:
            users.append(cls(user))
        
        return users
    
    @staticmethod
    def validate_user_registration(user):
        is_valid = True
        if User.get_user_by_email(user):
            flash('Email was already registered', 'reg_error')
            is_valid = False
        else:
            if len(user['first_name']) == 0 or len(user['last_name']) == 0 or len(user['email']) == 0 or NAME_REGEX.match(user['first_name']) or NAME_REGEX.match(user['last_name']):
                flash('All fields are required!', 'reg_error')
                is_valid = False
            if len(user['password']) < 8:
                flash('Password must be at least 8 symbols', 'reg_error')
                is_valid = False
            if not re.search(r'[0-9]', user['password']) or not re.search(r'[A-Z]', user['password']):
                flash('Password must contain at least 1 digit and 1 capital letter', 'reg_error')
                is_valid = False
            if user['password'] != user['c_password']:
                flash('Password dos not match', 'reg_error')
                is_valid = False
            if not EMAIL_REGEX.match(user['email']): 
                flash('Invalid email address!', 'reg_error')
                is_valid = False

        return is_valid
