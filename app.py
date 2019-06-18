from flask import Flask, render_template,request, flash,redirect,url_for,abort,session
from models import create_tables, drop_tables, User, Post
from forms import UserForm,LoginForm
import click
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('base.html')


@app.cli.command()
def initdb():
    create_tables()
    click.echo('Database created')


@app.cli.command()
def dropdb():
    drop_tables()
    click.echo('Database dropped')

@app.cli.command()
def fakedata():
    from faker import Faker
    fake = Faker()
    for user_pk in range(0, 15):
        user = User.create(username=fake.first_name(),mail = fake.text(),mdp = fake.text())
        for post_pk in range(0, 3):
            post = Post.create( title = fake.text(), body = fake.text(),
             dateCreate = fake.date(), refUser = user)    
      

@app.cli.command()
def testdata():
    for pk in User.select():
        print(pk.username)
        print(pk.mdp)
        print(pk.mail)

app.secret_key = 'HelloWorld' #Don't use it .. !

#fonction qui permet d'enregistrer un nouvelle utilisateur
@app.route('/register', methods=['GET', 'POST', ])
def user_create():
    user = User()
    form = UserForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.mdp.data, method='sha256')
        form.populate_obj(user)
        user.mdp = hashed_password 
        user.save()
        flash('The user has been created succesfully!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


#fonction qui permet à un utilisateur de se connecter
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        users = User.select().where(User.username == form.username.data)
        if users:
            for user in users:
                if check_password_hash(user.mdp, form.password.data):              
                    #login_user(user)
                    session['logged_in'] = True
                    session['username'] = user.username
                    flash('Logged in successfully')
                    return redirect(url_for('BlogEntry'))
    return render_template('login.html', form=form)
   
   
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/BlogEntry')
@login_required
def BlogEntry():
#    form = PostCreate()
    message = Post.select()
    return render_template('BlogEntry.html',message=message)


@app.route('/logout')
@login_required
def logout():
    #if request.method == 'POST':
    session['logged_in'] = False
    session.clear()
    # logout_user()
    return redirect(url_for('index'))