from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import post

@app.route('/posts/create', methods=['POST'])
def create_post():
    if not post.Post.validate_post(request.form):
        return redirect('/wall')
    
    data = {
        'content': request.form['content'],
        'user_id': session['id'],
    }
    
    post.Post.save_post(data)
    
    return redirect('/wall')

@app.route('/posts/delete', methods=['POST'])
def delete_one_post():
    
    post.Post.delete_post(request.form)
    
    return redirect('/wall')
