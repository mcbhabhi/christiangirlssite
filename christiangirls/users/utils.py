import secrets, os
from christiangirls import mail
from flask_mail import Message
from flask import url_for, current_app

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pfp', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def send_email(user):
    token = user.get_reset_token()
    msg = Message('Forgot Favourite Christ Moment?', 
                  sender = 'noreply@demo.com', 
                  recipients=[user.email])
    msg.body = f'''
    
To re-baptise yourself, visit {url_for('users.reset_token', token=token, _external=True)}

Though your sins are like scarlet, they shall be as white as snow; though they are red as crimson, they shall be like wool.
'''
    mail.send(msg)