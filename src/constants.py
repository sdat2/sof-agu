"""Constants.py program for storing paths and variables names."""

# Place all your constants here
import os
from typing import Literal, List, Dict
import numpy as np
from sys import platform
import cmocean.cm as cmo

# Note: constants should be UPPER_CASE

# TODO move some of these to a config file.

# Basic location defaults, to be referenced from here:
constants_path: str = os.path.realpath(__file__)
SRC_PATH: str = os.path.dirname(constants_path)
PROJECT_PATH: str = os.path.dirname(SRC_PATH)
DATA_PATH: str = os.path.join(PROJECT_PATH, "nc")
FIGURE_PATH: str = os.path.join(PROJECT_PATH, "figures")
KO_PATH: str = os.path.join(SRC_PATH, "data", "kim_(&orsi)_altimetric_fronts")

# Figure type
FIGURE_TYPE: Literal[".png", ".pdf"] = ".png"

# start ****DATA LOCATION section***
# This will certainly need to be changed on your machine

# Paths to BSOSE (unique to Jasmin)
if platform in ["Linux", "linux"]:
    # Data directory on GWS
    GEN_ROOT = DATA_PATH  # "/gws/nopw/j04/ai4er/users/sdat2/OLD")
    GEN_DATA_PATH: str = os.path.join(GEN_ROOT, "bsose_data")
    BSOSE_PATH: str = os.path.join(GEN_DATA_PATH, "bsose_stuv")
    DEFAULT_NC: str = os.path.join(
        GEN_ROOT, "i-metric-joint-k-5-d-3.nc"  # not valid in jasmin.
    )

# Paths to different BSOSE-i106 files (unique to my machine):
elif platform in ["Darwin", "darwin"]:
    # GEN_ROOT = os.path.join("/Users", "simon")
    GEN_ROOT: str = DATA_PATH
    BSOSE_PATH: str = os.path.join(GEN_ROOT, "bsose_monthly")
    GEN_DATA_PATH: str = BSOSE_PATH
    DEFAULT_NC: str = os.path.join(DATA_PATH, "i-metric-joint-k-5-d-3.nc")

else:
    assert False

# end ****DATA LOCATION section***


os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(FIGURE_PATH, exist_ok=True)
os.makedirs(KO_PATH, exist_ok=True)
os.makedirs(GEN_DATA_PATH, exist_ok=True)
os.makedirs(BSOSE_PATH, exist_ok=True)

# Salt, Theta, Uvel, Vvel
SALT_FILE: str = os.path.join(BSOSE_PATH, "bsose_stuv", "bsose_i106_2008to2012_monthly_Salt.nc")
THETA_FILE: str = os.path.join(BSOSE_PATH, "bsose_stuv", "bsose_i106_2008to2012_monthly_Theta.nc")
VVEL_FILE: str = os.path.join(BSOSE_PATH, "bsose_stuv", "bsose_i106_2008to2012_monthly_Vvel.nc")
UVEL_FILE: str = os.path.join(BSOSE_PATH, "bsose_stuv", "bsose_i106_2008to2012_monthly_Uvel.nc")

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
USELESS_LIST: List[str] = ["iter", "Depth", "rA", "drF", "hFacC"] # list of variables from BSOSE to discard before processing
VAR_NAME_LIST: List[str] = ["SALT", "THETA"] # variables used in to fit the pcm model on
FEATURES_D: Dict[str, str] = {"THETA": "THETA", "SALT": "SALT"} # Mapping for within pyxpcm

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
K_LIST: List[int] = [5, 4, 2, 10]  # K's to make when running batch script.
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

FINAL_LOC: str = os.path.join(PROJECT_PATH, "images") # "../FBSO/images"
os.makedirs(FINAL_LOC, exist_ok=True)

# info for profile plots
ZS: List[int] = [-x for x in range(300, 2000, 10)] # Z levels.
LZ: int = len(ZS) # number of Z levels.
