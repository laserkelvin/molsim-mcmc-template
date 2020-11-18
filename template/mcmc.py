
import numpy as np

from molsim.mcmc import TMC1FourComponent, EmceeHelper
from molsim.file_handling import load_mol

WALKERS = 200
ITERATIONS = 1500

RESTART = False

MOLECULE = ""

model = TMC1FourComponent.from_yml(f"{MOLECULE}.yml")

if RESTART:
    mcmc = EmceeHelper.from_netcdf(f"{MOLECULE}_posterior.nc", restart=RESTART)
else:
    initial = np.load("initial_parameters.npy")
    mcmc = EmceeHelper(initial)
mcmc.sample(model, WALKERS, ITERATIONS, workers=1, scale=None, restart=RESTART)

mcmc.save_posterior(f"{MOLECULE}_posterior.nc")
