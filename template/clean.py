
from molsim.mcmc import preprocess
from molsim.file_handling import load_mol
from joblib import dump

"""
Requirements to run:

    1. SPCAT catalog at 300 K
    2. Partition function file in molsim format
    3. NumPy array containing frequency/intensity of spectrum
"""

MOLECULE = ""
DATA_PATH = "../tmc1_spectra.npy"
CAT_PATH = f"../catalogs/{MOLECULE}.npz"
QPART_PATH = f"../qpart/{MOLECULE}.qpart"

# width of spectra to extract in radial velocity
delta_v = 0.5
# nominal velocity offset to use
vlsr = 5.8
# cut off threshold for simulated line intensity, as a percentage
# of the strongest line in the catalog. the more lines you use
# the better the analysis, but the longer it takes.
sim_cutoff = 0.01
# choose whether to block strong interloping lines. If you expect
# to see individual lines of this molecule in this spectrum, set
# this to False
block = False

# pre-package the molecule object; comprises an SPCAT catalog
# and partition function data
molecule = load_mol(CAT_PATH, type="SPCAT", qpart_file=QPART_PATH)
dump(molecule, f"{MOLECULE}.mol")

# this generates a bunch of datafiles to be used for the MCMC
data = preprocess.preprocess_spectrum(
    MOLECULE,
    DATA_PATH,
    CAT_PATH,
    delta_v=delta_v,
    vlsr=vlsr,
    sim_cutoff=sim_cutoff,
    legacy=True,
    block_interlopers=block
    )

