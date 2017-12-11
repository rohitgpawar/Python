"""
The flask Web Application package.
"""

from flask import Flask, session,request, flash, redirect, url_for,render_template
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps
from datetime import datetime

app = Flask(__name__)


'''
DATABASE SCRIPTS
create database flaskWebApp;
create table users(id INT(11) AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100),email VARCHAR(100), password VARCHAR(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
'''

# CONFIG MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'flaskwebapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# INITIALIZE MYSQL
mysql = MySQL(app)

# HOME PAGE / INDEX PAGE
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

#CONTACT INFORMATION
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        year=datetime.now().year,
        title='Rohit Pawar.'
    )


# USER RESISTRATION FORM
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max = 50)])
    email = StringField('Email',[validators.Length(min =6, max=50)])
    password = PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

#REGISTER USER
@app.route('/register', methods=['GET','POST'])
def register():
    """Renders the register page."""
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        #Create Cursor
        cur = mysql.connection.cursor()

        # Get user by email
        db_users = cur.execute("SELECT * FROM users WHERE email = %s", [email])
        if db_users == 0:
            cur.execute("INSERT INTO users(name, email, password) VALUES (%s, %s, %s)", (name,email,password))
            #Commit to DB
            mysql.connection.commit()
            flash('Registration Successful. Please Login', 'success')
        else:
            flash('Account already exits for this email. Please Login', 'danger')
        #Close Connection
        cur.close()

        return redirect(url_for('login'))

    return render_template(
        'register.html',
        title='Registration',
        year=datetime.now().year,
        form = form
    )

#USER LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    """Renders the login page."""
    if request.method == 'POST':
        #Get email Password
        email = request.form['email']
        password_given = request.form['password']
        #Create cursor
        cur = mysql.connection.cursor()
        #Get user by email

        db_users = cur.execute("SELECT * FROM users WHERE email = %s",[email])
        if db_users > 0:

            #Get Hash Password
            db_user = cur.fetchone()
            password = db_user['password']

            #Validate user
            if sha256_crypt.verify(password_given,password):
                session['logged_in'] = True
                session['email'] = email
                flash('You are now logged in', 'success')
                return redirect((url_for('dashboard')))
            else:
                error = 'Invalid Login'
                return render_template(
                    'login.html',
                    title='Login',
                    year=datetime.now().year,
                    error=error
                )
            cur.close()
        else:
            error = 'Email Not Found'
            return render_template(
                'login.html',
                title='Login',
                year=datetime.now().year,
                error = error
            )
    return render_template(
        'login.html',
        title='Login',
        year=datetime.now().year
    )

#CHECK AUTHENTICATED
def is_logged_in(data):
    @wraps(data)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return data(*args,**kwargs)
        else:
            flash('Unauthorized Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.clear();
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


#DASHBOARD
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.secret_key = 'mySecretKey_123'
    app.run(debug=True)
