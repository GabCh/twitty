import hashlib
import binascii

from flask import Flask, render_template, request, session, url_for, redirect
from src.data.babblerdb import BabblerDB


app = Flask(__name__)
app.config.from_object(__name__)

app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = ''
app.config['DB_NAME'] = 'Babbler'

#  Hashing salt
salt = '1WZZhonPwvMWzu3pU5J+4fp1d9SCHYi3qQ4QpxTvznatMsSzl4iOKCtF++vBJ+ZQPOXCDIs0ipiaPAlEI2RSGQ=='

db = BabblerDB(app)


@app.route('/')
def main():
    logged = 'username' in session
    return render_template('index.html',
                           new_login=request.args.get('new_login'),
                           babbler=request.args.get('babbler'),
                           logged=logged)


@app.route('/login', methods=['GET', 'POST'])
def login():
    view = render_template('partials/login.html',
                           newly_registered=request.args.get('newly_registered'),
                           invalid=request.args.get('invalid'))
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 65336)
        password = str(binascii.hexlify(password))[2:-1]

        result = db.authenticate(username, password)
        if result:
            return 'True'
    return view


@app.route('/register', methods=['GET', 'POST'])
def register():
    view = render_template('/partials/register.html')
    if request.method == 'POST':
        data = request.form
        password = hashlib.pbkdf2_hmac('sha256', data['password'].encode(), salt.encode(), 65336)
        password = str(binascii.hexlify(password))[2:-1]

        db.add_babbler(data['username'], data['public_name'], password)
    return view


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/myprofile')
def my_profile():
    if session['logged_in']:
        return render_template('myprofile.html')
    else:
        return redirect(url_for('/login'))


@app.route('/myfeed')
def feed():
    babbles = db.get_babbles_from_followed_babblers('GabCh')
    return render_template('partials/feed.html', babbles=babbles)


@app.route('/babblers/<username>')
def babbler_profile(username):
    view = render_template('/partials/profile.html', user=username)
    return view


@app.route('/tag/<tag>')
def tag_page(tag):
    babbles = db.read_babbles_with_tag(tag)
    view = render_template('/partials/tag_results.html', babbles=babbles, tag=tag)
    return view


@app.route('/search')
def search_form():
    keyword = request.args.get('keyword')
    if keyword:
        babbles = db.read_babbles(keyword)
        babblers = db.read_babblers(keyword)
        return render_template('/partials/search_results.html', keyword=keyword, babbles=babbles, babblers=babblers)
    else:
        return render_template('index.html')


# Validate if <username> is already taken.

@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    exists = False
    if db.validate_username(username):
        exists = True
    return str(exists)


if __name__ == '__main__':
    app.run()
