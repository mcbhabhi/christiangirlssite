from flask import Blueprint, render_template, url_for, flash, redirect, request
from christiangirls import db, crypt
from christiangirls.models import User
from flask_login import login_user, current_user, logout_user, login_required
from christiangirls.users.utils import save_picture, send_email
from christiangirls.users.forms import (Baptism, EdenGarden, UpdateAuthor,
                    RequestResetForm, ResetPasswordForm)


users = Blueprint('users', __name__)


@users.route('/baptise', methods=['GET', 'POST'])
def baptise():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = Baptism()

    if form.validate_on_submit():
        hashed = crypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{ form.username.data } has been baptised', 'success')
        return redirect(url_for('users.eden'))
    
    return render_template('baptise.html', title='Baptise', form=form)


@users.route('/eden', methods=['GET', 'POST'])
def eden():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = EdenGarden()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Access Denied', 'danger')

    return render_template('eden.html', title='Gardens of Eden', form=form) 


@users.route('/leave', methods=['GET', 'POST'])
def leave():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/author', methods=['GET', 'POST'])
@login_required
def author():
    form = UpdateAuthor()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.pfp = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'{ current_user.username } baptised again!', 'success')
        return redirect(url_for('users.author'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    pfp = url_for('static', filename='pfp/' + current_user.pfp)
    return render_template('author.html', title='Account', image_file=pfp, form=form)


@users.route('/forgot_favourite_christ_moment', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Email sent!')
        return redirect(url_for('users.eden'))
    return render_template('reset_request.html', title = 'Shame', form = form)


@users.route('/reset_favourite_christ_moment/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
         return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash("Invalid or Expired Token")
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed = crypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed
        db.session.commit()
        flash(f'{ user.username } has been re-baptised!', 'success')
        return redirect(url_for('users.eden'))
    return render_template('reset.html', title = 'Redemption', form = form)