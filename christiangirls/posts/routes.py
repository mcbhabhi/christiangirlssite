from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from christiangirls import db
from christiangirls.models import User, Post
from flask_login import current_user, login_required
from christiangirls.posts.forms import Create


posts = Blueprint('posts', __name__)


@posts.route('/journal/confess', methods=['GET', 'POST'])
@login_required
def create():
    form = Create()
    if form.validate_on_submit():
        essay = Post(title=form.title.data, content=form.content.data, author=current_user, bibliography=form.bibliography.data)
        db.session.add(essay)
        db.session.commit()
        flash('Your essay has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('confess.html', title='create', form=form,
                           legend='Create Post')


@posts.route('/journal/<string:author>', methods=['GET', 'POST'])
def journal(author):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=author).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='pfp/' + user.pfp)
    return render_template('journal.html', title='journal', posts=posts, journal_author=user, image_file=image_file)


@posts.route('/journal/<int:post_id>', methods=['GET', 'POST'])
def confession(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('confession.html', title='Post', post=post)


@posts.route('/journal/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Create()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.bibliography = form.bibliography.data
        db.session.commit()
        flash('Confession Updated', "success")
        return redirect(url_for('posts.confession', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.bibliography.data = post.bibliography
    return render_template('confess.html', title='Edit', form=form,
                           legend='Update Post')


@posts.route('/journal/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your confession has been deleted!', 'success')
    return redirect(url_for('main.home'))