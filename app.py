from flask import Flask, render_template
from one.api import ONE

app = Flask(__name__)
one = ONE(base_url='https://openalyx.internationalbrainlab.org',password='international', silent=True)

@app.route('/')
def home():
    eids = one.search(data='channels.mlapdv')
    return render_template('experiments.html', eids=eids)

if __name__ == '__main__':
    app.run(debug=True)
