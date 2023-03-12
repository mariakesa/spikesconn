from flask import Flask, render_template, url_for
from one.api import ONE
from one.alf.exceptions import ALFObjectNotFound, ALFMultipleCollectionsFound
import io
from flask import make_response
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

@app.route('/')
def home():
    eids = one.search(data='channels.mlapdv')
    return render_template('experiments.html', eids=eids)

def generate_mlapdv_plot(mlapdv,ind):
    atlas=at.AllenAtlas()

    # create the xyz array
    xyz = np.c_[mlapdv[:, 0].astype(np.float64) / 1e6, mlapdv[:, 1].astype(np.float64) / 1e6, mlapdv[:, 2].astype(np.float64) / 1e6]

    fit=at.Trajectory.fit(xyz)
    proj=fit.project(xyz)
    print('PROJ', proj)

    # create a figure with subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    

    # render the first image
    ax0 = atlas.plot_tilted_slice(xyz, 0, ax=axs[0])
    ax0[0].scatter(proj[:, 1]*1e6, proj[:, 2]*1e6, c='pink', s=5)
    

    # render the second image
    ax1 = atlas.plot_tilted_slice(xyz, 1, ax=axs[1])
    ax1[0].scatter(proj[:, 0]*1e6, proj[:, 2]*1e6, c='pink', s=5)

    # Save the plot to a file
    fig.savefig(f'static/mlapdv_plot{ind}.png', bbox_inches='tight')

    # Return the path to the saved file
    return f'static/mlapdv_plot{ind}.png'



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
    try:
        path00 = generate_mlapdv_plot(mlapdv_probe00,'00')
    except:
        path00=None
    try:
        path01 = generate_mlapdv_plot(mlapdv_probe01,'01')
    except:
        path01=None

    # render the template with the image buffer
    return render_template('images.html', plot_path00=path00, plot_path01=path01)
    
if __name__ == '__main__':
    app.run(debug=True)

