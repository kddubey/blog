# stats-stackexchange
Simulations for [my questions and answers on stats.stackexchange.com](https://stats.stackexchange.com/users/337906/chicxulub).


| dir                  | q/a link                                                                                                                                                                                                               |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `var_pred_var_error` | [Does higher variance in predictions <br>result in higher variance error estimation?](https://stats.stackexchange.com/questions/568492/does-higher-variance-in-predictions-result-in-higher-variance-error-estimation) |
| `model_vs_human`     | [Verify that a model can beat a noisy human](https://stats.stackexchange.com/questions/443282/can-precision-and-recall-of-a-dnn-trained-on-human-labeled-data-be-higher-than-p/580894#580894)                          |

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
