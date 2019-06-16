from flask import Flask, render_template,request, flash,redirect,url_for
from models import create_tables, drop_tables, User, Post
from forms import UserForm
import click
app = Flask(__name__)

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
        user = User.create(username=fake.first_name(), name=fake.name(),
         firstname = fake.first_name(),mail = fake.text(),mdp = fake.text())
        for post_pk in range(0, 3):
            post = Post.create( title = fake.text(), body = fake.text(),
             dateCreate = fake.date(), refUser = user)    
      

@app.cli.command()
def testdata():
    for pk in User.select():
        print(pk.username)
        print(pk.name)
        print(pk.firstname)

app.secret_key = 'HelloWorld' #Don't use it .. !

@app.route('/user/create', methods=['GET', 'POST', ])
def user_create():
    user = User()
    form = UserForm()
    if form.validate_on_submit():
        form.populate_obj(user)
        user.save()
        flash('Hooray ! User created !')
        return redirect(url_for('user_create'))
    return render_template('user.html', form=form)