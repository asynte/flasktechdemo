from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required, UserMixin
from app import app, db, lm
from .forms import LoginForm, RegistrationForm
from .models import User, Post
from oauth import OAuthSignIn



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = Post.query.all()
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts
                           )

@app.route('/likes/<id>', methods = ['GET', 'POST'])
@login_required
def increment_like(id):
    user = g.user
    x = Post.query.filter_by(user_id = id).first()
    if x:
        x.amountlike = x.amountlike + 1
        db.session.flush()
        db.session.commit()
    posts = Post.query.all()
    return render_template('index.html',
                            user = user,
                            posts = posts
                            )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate() == False:
          return render_template('login.html', form=form)
        else:
          session['email'] = form.email.data
          return redirect(url_for('index'))
                 
    elif request.method == 'GET':
        return render_template('login.html', form=form)     

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm();

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('register.html', form=form)
        else:
            newuser = User(" ", form.userID.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            login_user(newuser, False)          
            return redirect(request.args.get('next') or url_for('index'))
        
    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#OAuth stuff start

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, userID=username, email=email, password = None)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))
