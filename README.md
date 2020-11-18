# molsim-mcmc-template

File structure for reproducible molsim MCMC

## Instructions

1a. If you don't have `gh` CLI, clone this directory with

```
git clone https://github.com/laserkelvin/molsim-mcmc-template.git
```

1b. If you _do_ have `gh` CLI, run

```
gh repo --use-template laserkelvin/molsim-mcmc-template
```

2. Place spectra as text files in the `spectra` folder. This expects two column data, frequency and intensity, space delimited.
3. Place target molecule catalog and `.qpart` files into `catalog` and `qpart`. It helps if they're named the same thing in both folders, with `.cat` and `.qpart` extensions.
4. Copy the `template` folder and name it after your molecule

This setup allows you to run a "pipeline" somewhat manually. The sequence of scripts is:

1. `clean.py`
2. `mcmc.py`
3. `stack_mf.py`

### `clean.py`

This script will preprocess the data for use in the MCMC code, isolating chunks of your spectrum that are coincident with a specified catalog.

There are variables in this script that will need your attention. The first two, `MOLECULE` and `DATA`, will point the script to where files are in the filestructure. The remaining parameters determine how the chunking and filtering will be done: `delta_v`, `vlsr`, `sim_cutoff`, and `block`. The string comments for each of these explain what they do. Note that `sim_cutoff` specifies the strongest lines _on a normal (not log) scale_.

Assuming `molsim` is installed on the `python` environment you're using, you can simply run

```
python clean.py
```

All the steps taken in this process will be logged in `{MOLECULE}_analysis.log`.

### `mcmc.py`

This script will look for settings in a `{MOLECULE}.yml` file that defines the prior used for the MCMC, as well as parameters like how many walkers and steps for the simulation. The `RESTART` variable, intuitively, determines whether the simulation is being restart from the last step.

