from brainbox.task import trials
from one.api import ONE
import pandas as pd
import numpy as np
import GEMA

# Connecting to the API
one = ONE(base_url='https://openalyx.internationalbrainlab.org',
          password='international', silent=True)
# Setting an experimental id
eid = '58b1e920-cfc8-467e-b28b-7654a55d0977'

####
# Get data


def query_trials(eid):

    # Load trials into df
    trials = one.load_dataset(eid, 'alf/_ibl_trials.table.pqt')
    trials = pd.DataFrame(trials)
    print(trials)
    events = trials["stimOn_times"]
    # Get spike_times
    spike_times = one.load_dataset(
        eid, 'alf/probe00/pykilosort/spikes.times.npy')
    # Get clusters
    spike_clusters = one.load_dataset(
        eid, 'alf/probe00/pykilosort/spikes.clusters.npy')


def pipeline(eid):
    query_trials(eid)
