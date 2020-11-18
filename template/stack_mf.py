from shutil import copy2

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from molsim.utils import process_mcmc_json
from molsim.stats import get_rms
from molsim.functions import velocity_stack
from molsim.file_handling import load_mol, load_obs

# Change this to match the name of files
MOLECULE = ""


obs = load_obs("../tmc1_spectra.txt", type=None)
molecule = load_mol(
    f"../gotham_catalogs/{MOLECULE}.npz",
    type="molsim",
    qpart_file=f"../qpart/{MOLECULE}.qpart",
)

# Use molsim functionality to interpret mean result
sources, sims, spec, json_dict = process_mcmc_json(
    f"{MOLECULE}_mcmc_result.json", molecule, obs, make_plots=False, return_json=True
)

internal_stack_params = {
    "selection": "lines",
    "freq_arr": obs.spectrum.frequency,
    "int_arr": obs.spectrum.Tb,
    "freq_sim": spec.freq_profile,
    "int_sim": spec.int_profile,
    "res_inp": 0.0014,
    "dV": np.mean([x for x in json_dict["dV"]["mean"]]),
    "dV_ext": 40,
    "vlsr": np.mean([x for x in json_dict["VLSR"]["mean"]]),
    "vel_width": 40,
    "v_res": 0.02,
    "blank_lines": True,
    "blank_keep_range": [
        -5 * np.mean([x for x in json_dict["dV"]["mean"]]),
        5 * np.mean([x for x in json_dict["dV"]["mean"]]),
    ],
    "flag_lines": False,
    "flag_sigma": 5,
}
# run stacking routine and then cross-correlate
stack = velocity_stack(internal_stack_params)

matched_filter = np.correlate(stack.snr, stack.int_sim, mode="same")
matched_filter /= get_rms(matched_filter)

# dump the result to disk
df = pd.DataFrame(
    list(zip(stack.velocity, stack.snr, stack.int_sim, matched_filter)),
    columns=["Velocity", "SNR", "Simulation", "MatchedFilter"],
)

df.to_csv(f"../results/{MOLECULE}_stack-MF.csv", index=False)
copy2(f"{MOLECULE}_mcmc_result.json", "../results/")
