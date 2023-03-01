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

app = Flask(__name__)
one = ONE(base_url='https://openalyx.internationalbrainlab.org',password='international', silent=True)

@app.route('/')
def home():
    eids = one.search(data='channels.mlapdv')
    return render_template('experiments.html', eids=eids)

def generate_mlapdv_plot(mlapdv):
    from ibllib.atlas import atlas as at
    from one.api import ONE
    import numpy as np

    atlas=at.AllenAtlas()
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))
    xyz=np.c_[mlapdv[:,0].astype(np.float64) / 1e6, mlapdv[:,1].astype(np.float64) / 1e6, mlapdv[:,2].astype(np.float64) / 1e6]
    #fig,axs=atlas.plot_tilted_slice(xyz,0)
    axs[0].scatter(mlapdv[:,1],mlapdv[:,2],c='b',s=1)
    #axs[1]=atlas.plot_tilted_slice(xyz,1)
    axs[1].scatter(mlapdv[:,0],mlapdv[:,2],c='b',s=1)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)

    return base64.b64encode(buf.getbuffer()).decode('ascii')



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
    
    # Create the matplotlib figure
    fig = generate_mlapdv_plot(mlapdv_probe00)
    
    # Render the mlapdv_matplotlib.html template with the figure and eid
    return render_template('mlapdv.html', eid=eid, fig=fig)
    
if __name__ == '__main__':
    app.run(debug=True)
