from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import message, user

@app.route('/messages')
def messages_page():
    if 'id' not in session:
        return redirect('/logout')
    id = {
        'id': session['id']
    }
    
    messages = message.Message.get_inbox_messages(id)
    users = user.User.get_other_users(id)

    return render_template('messages.html', all_messages=messages, users=users, current_user=user.User.get_one_user(id) )


@app.route('/messages/send', methods=['POST'])
def send_msg():
    if not message.Message.validate_message(request.form):
        return redirect('/messages')
    
    data = {
        'content': request.form['content'],
        'sender_id': session['id'],
        'receiver_id': request.form['receiver_id']
    }
    message.Message.send_message(data)
    
    return redirect('/messages')

@app.route('/messages/delete', methods=['POST'])
def delete_msg():

    message.Message.delete_message(request.form)
    
    return redirect('/messages')
