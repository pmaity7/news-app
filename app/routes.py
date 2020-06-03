from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, PostForm, EditPostForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from sqlalchemy import desc

@app.route('/')
@app.route('/home')
def home():
        return render_template('home.html', title='Home page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('home'))
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are succesfully registered')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/news')
@login_required
def news():
        posts = Post.query.order_by(desc(Post.timestamp)).all()
        return render_template('news.html', title='News page', posts=posts)

@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.content.data, user_id=form.author.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post was posted')
        return redirect(url_for('news'))
    return render_template('add_news.html', title="Add news", form=form)

@app.route('/delete/<title>')
def delete(title):
    post = Post.query.filter_by(title=title).first()
    db.session.delete(post)
    db.session.commit()
    flash('News deleted')
    return redirect(url_for('news'))

@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title):
    form = EditPostForm()
    post = Post.query.filter_by(title=title).first()
    form.title.data = post.title
    form.author.data = post.user_id
    form.content.data = post.body
    if form.validate_on_submit():
        post.title = form.title.data
        post.user_id = form.author.data
        post.body = form.content.data
        db.session.commit()
        flash('Post updated')
        return redirect(url_for('news'))

    return render_template('edit_news.html', title="Edit news", form=form)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('user.html', users=users)

@app.route('/contact')
def contact():
    return render_template('about.html', title="About")
        
