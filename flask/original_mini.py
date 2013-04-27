#!/usr/bin/env python

import flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = flask.Flask(__name__)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    time = db.Column(db.DateTime)

@app.before_request
def get_user():
    flask.g.username = flask.session.get('username')

@app.route('/')
def home():
    return flask.render_template('messages.html', messages=Message.query.all())

@app.route('/logout')
def logout():
    flask.session.pop('username', '')
    flask.flash('Flash message: Signed out')
    return flask.redirect(flask.url_for('home'))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if flask.request.method == 'POST':
        text = flask.request.form['message']
        message = Message(text=text, time=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('new.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        flask.flash('Flash message: USERNAME has been set to ' + username)
        flask.session['username'] = username
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('login.html')

@app.template_filter()
def justthedate(value):
    return str(value)[0:10]

if __name__ == '__main__':
    db.create_all()
    app.run()

