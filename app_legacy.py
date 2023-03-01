from flask import Flask, render_template
from one.api import ONE
from one.alf.exceptions import ALFObjectNotFound, ALFMultipleCollectionsFound
import io
from flask import make_response
import matplotlib.pyplot as plt
import io
import base64
from flask import render_template
import matplotlib.pyplot as plt
import numpy as np
import brainbox as bb
from ibllib.atlas import atlas as at
import matplotlib.pyplot as plt
from one.api import ONE
from one.alf.exceptions import ALFObjectNotFound
from ibllib.atlas import AllenAtlas
from ibllib.atlas import atlas as at
from one.api import ONE
import numpy as np

app = Flask(__name__)
one = ONE(base_url='https://openalyx.internationalbrainlab.org',password='international', silent=True)
atlas=at.AllenAtlas()

@app.route('/')
def home():
    eids = one.search(data='channels.mlapdv')
    return render_template('experiments.html', eids=eids)

def generate_mlapdv_plot(mlapdv):
    

    # create the xyz array
    xyz = np.c_[mlapdv[:, 0].astype(np.float64) / 1e6, mlapdv[:, 1].astype(np.float64) / 1e6, mlapdv[:, 2].astype(np.float64) / 1e6]

    # create a figure with subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # render the first image
    ax = atlas.plot_tilted_slice(xyz, 0, ax=axs[0], volume='image', cmap='gray')
    ax.scatter(mlapdv[:, 1], mlapdv[:, 2], c='b', s=1)

    # render the second image
    ax = atlas.plot_tilted_slice(xyz, 1, ax=axs[1], volume='image', cmap='gray')
    ax.scatter(mlapdv[:, 0], mlapdv[:, 2], c='b', s=1)

    # save the figure to a buffer
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # return the image buffer
    return buf



@app.route('/<eid>')
def show_mlapdv(eid):
    # Load mlapdv.npy for probe00 if it exists
    try:
        mlapdv_probe00 = one.load_dataset(eid, 'channels.mlapdv.npy', collection=f'alf/probe00/pykilosort')
    except ALFObjectNotFound:
        mlapdv_probe00 = None

    # Load mlapdv.npy for probe01 if it exists
    try:
        mlapdv_probe01 = one.load_dataset(eid, 'channels.mlapdv.npy', collection=f'alf/probe01/pykilosort')
    except ALFObjectNotFound:
        mlapdv_probe01 = None
    
    # render the images for the given eid
    buf = generate_mlapdv_plot(mlapdv_probe00)

    # render the template with the image buffer
    return render_template('images.html', eid=eid, image=url_for('static', filename='img.png'), buffer=buf.read())
    
if __name__ == '__main__':
    app.run(debug=True)
