"""Constants.py program for storing paths and variables names."""

# Place all your constants here
import os
import numpy as np
import pathlib
from sys import platform
import cmocean.cm as cmo

# Note: constants should be UPPER_CASE

# Basic location defaults, to be referenced from here:
constants_path = os.path.realpath(__file__)
SRC_PATH = os.path.dirname(constants_path)
PROJECT_PATH = os.path.dirname(SRC_PATH)
DATA_PATH = os.path.join(PROJECT_PATH, "nc")
FIGURE_PATH = os.path.join(PROJECT_PATH, "figures")
KO_PATH = os.path.join(SRC_PATH, "data", "kim_(&orsi)_altimetric_fronts")

# Data directory on GWS
# Figure type
FIGURE_TYPE = ".png"

# start ****DATA LOCATION section***
# This will certainly need to be changed on your macine
GWS_DATA_DIR = DATA_PATH



GEN_DATA_PATH: str = os.path.join(GWS_DATA_DIR, "bsose_data")
BSOSE_PATH: str = os.path.join(GEN_DATA_PATH, "bsose_stuv")
DEFAULT_NC: str = os.path.join(
        str(GWS_DATA_DIR), "nc", "i-metric-joint-k-5-d-3.nc"  # not valid in jasmin.
    )

os.makedirs(GEN_DATA_PATH ,exist_ok=True)
# end ****DATA LOCATION section***

# Salt, Theta, Uvel, Vvel
SALT_FILE: str = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Salt.nc")
THETA_FILE: str = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Theta.nc")
VVEL_FILE: str = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Vvel.nc")
UVEL_FILE: str = os.path.join(BSOSE_PATH, "bsose_i106_2008to2012_monthly_Uvel.nc")

# COORDS within BSOSE-i106
Z_COORD: str = "Z"
D_COORD: str = "Depth" # this is actually a variable, not the same as the others
Y_COORD: str = "YC"
X_COORD: str = "XC"
T_COORD: str = "time"

# COORDS created in my variables
P_COORD: str = "pair" # the name for the paired i metric dimension/coordinate
CLUST_COORD: str = "cluster" # the name for the cluster coordinate/ dimension

# Particular names within BSOSE-i106
DEPTH_NAME: str = D_COORD
USELESS_LIST: list = ["iter", "Depth", "rA", "drF", "hFacC"] # list of variables from BSOSE to discard before processing
VAR_NAME_LIST: list = ["SALT", "THETA"] # variables used in to fit the pcm model on
FEATURES_D: dict = {"THETA": "THETA", "SALT": "SALT"} # Mapping for within pyxpcm

# Naming of intermediate files
INTERP_FILE_NAME: str = os.path.join(DATA_PATH, "interp.nc")
REMAKE: bool = False  # whether or not to prefer remaking the interp

# Chosen hyperparameters in the model run:
RUN_NAME: str = "010"  # the seed as a string
SEED: int = int(RUN_NAME) # the seed as an int
np.random.seed(SEED)  # feed the run name to np random seed - synchronises all

# random variables used locally to make it reproducible.
MIN_DEPTH: float = 300  # the depth of the minimum cut off (m)
MAX_DEPTH: float = 2000  # the depth of the maximum cut off (m)
K_LIST: list = [5, 4, 2, 10]  # K's to make when running batch script.
K_CLUSTERS: int = 5  # number of clusters for the main example figure.
D_PCS: int = 3  # number of principal components to be used.
EXAMPLE_TIME_INDEX: int = 40  # the default time to go for.
EXAMPLE_Z_INDEX: int = 0  # Surface layer.
ALL_NAME: str = "all"  # starting combination script.

# plotting specifications
# This is for diverging colormaps.
DEFAULT_COLORMAP = cmo.balance
# This is for the hard assingment cluster images.
CLUST_COLORS: str = "Set1" # "Dark1"

# Move plots to location
FINAL_LOC: str = "../FBSO/images"

# info for profile plots
ZS = [-x for x in range(300, 2000, 10)] # Z levels.
LZ = len(ZS) # number of Z levels.
