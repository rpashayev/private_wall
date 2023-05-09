from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, comment
from flask import flash
import re

POST_REGEX = re.compile(r'^\s*$')

class Post:
    DB = 'msg_coding_dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.comments = None
        self.creator = None
    
    
    @classmethod
    def get_all_posts(cls):
        all_posts = []
        query = '''
            SELECT *
            FROM posts
            JOIN users ON users.id = posts.user_id
            ORDER BY posts.created_at DESC;
        '''
        results = connectToMySQL(cls.DB).query_db(query)

        for row in results:
            one_post = cls(row)
        
            creator_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
        
            one_post.creator = user.User(creator_info)
            
            data = {
                'id': row['id']
            }
            one_post.comments = comment.Comment.get_comments(data)
            
            all_posts.append(one_post)
            
        return all_posts
    
    @classmethod
    def get_user_posts(cls, data):
        user_posts = []
        query = '''
            SELECT *
            FROM posts
            WHERE user_id = %(user_id)s;
        '''

        results = connectToMySQL(cls.DB).query_db(query, data)
        
        for post in results:
            user_posts.append(cls(post))
        
        return user_posts
    
    @classmethod
    def save_post(cls, data):
        query = '''
            INSERT 
            INTO posts(content, user_id)
            VALUES ( %(content)s, %(user_id)s );
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_post(cls, data):
        query = '''
            DELETE
            FROM posts
            WHERE id = %(post_id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) == 0 or POST_REGEX.match(post['content']):
            flash('Post cannot be empty!', 'post_error')
            is_valid = False

        return is_valid
    