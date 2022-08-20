# stats-stackexchange
Simulations for [my questions and answers on stats.stackexchange.com](https://stats.stackexchange.com/users/337906/chicxulub).


| dir/file               | q/a link                                                                                                                               |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `var_pred_var_error`   | [Does higher variance in predictions <br>result in higher variance error estimation?](https://stats.stackexchange.com/q/568492/337906) |
| `model_vs_human.ipynb` | [Verify that a model can outperform its <br>noisy training data](https://stats.stackexchange.com/a/580894/337906)                    |
| `select_on_test.ipynb` | [Verify that a model can simultaneously be <br>selected and evaluated on a test set](https://stats.stackexchange.com/a/570680/337906)  |

If the notebook appears too vertically narrow in your browser, refresh.

## Setup

Most of this code is in Python 3.7+. So create an environment `stats-se` using venv
or conda:

Using venv:

```
cd /your/venvs

python -m venv stats-se

source stats-se/bin/activate

python -m pip install -r /path/to/stats-stackexchange/requirements.txt
```

Using conda:

```
conda env create -f environment.yml

conda activate stats-se
```

## Usage

Interact w/ the code via Jupyter. I like [VS code notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
