from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re

COMMENT_REGEX = re.compile(r'^\s*$')

class Comment:
    DB = 'msg_coding_dojo_wall_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.creator = None
    
    @classmethod
    def save_comment(cls, data):
        query = '''
            INSERT 
            INTO comments(content,post_id, user_id)
            VALUES (%(content)s, %(post_id)s, %(user_id)s);
        '''
        
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_comments(cls, data):
        all_comments = []
        query = '''
            SELECT *
            FROM comments
            JOIN posts ON posts.id = comments.post_id
            JOIN users ON users.id = comments.user_id
            WHERE posts.id = %(id)s
            ORDER BY comments.created_at; 
        '''
        
        results = connectToMySQL(cls.DB).query_db(query, data)
        
        for row in results:
            one_comment = cls(row)
            creator_info = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            one_comment.creator = user.User(creator_info)
            all_comments.append(one_comment)
        
        return all_comments
    
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['content']) == 0 or COMMENT_REGEX.match(comment['content']):
            flash('Comment cannot be empty!', 'comment_error')
            is_valid = False

        return is_valid
    