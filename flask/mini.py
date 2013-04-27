import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('upload.html')

@app.route('/create/<hash>', methods=['POST'])
def create(hash):
    code = flask.request.form['code']
    github_id = github_ids[hash] 

    f = open('/tmp/' + github_id + '.txt', 'w')
    print >> f, code
    f.close()
    
    return flask.redirect(flask.url_for('feedback'))

@app.route('/upload/<hash>/')
def upload(hash):
    return flask.render_template('upload.html', hash=hash)

@app.route('/feedback')
def feedback():
    return flask.render_template('feedback.html')

if __name__ == '__main__':
    
    github_ids = {
        '9962afd7d9bc7f38388519f95deaf4a8': 'dserban',
        '202c36cceaeb55d090b397849b119d52': 'andreimacavei'
    }
    
    app.run()
