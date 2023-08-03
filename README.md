# stackexchange

Simulations for my questions and answers on
[stats.stackexchange.com](https://stats.stackexchange.com/users/337906/) and
[stackoverflow.com](https://stackoverflow.com/users/18758987/).


| dir/file link                                                                                                         | q/a link                                                                                                                                                         |
|-----------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`var_pred_var_error`](https://github.com/kddubey/stats-stackexchange/tree/main/var_pred_var_error)                   | [Does higher variance in predictions <br>result in higher variance error estimation?](https://stats.stackexchange.com/q/568492/337906)                           |
| [`model_vs_noisy_labels.ipynb`](https://github.com/kddubey/stats-stackexchange/blob/main/model_vs_noisy_labels.ipynb) | [Prove that a model can outperform its <br>noisy training labels](https://stats.stackexchange.com/a/580894/337906)                                               |
| [`select_on_test.ipynb`](https://github.com/kddubey/stats-stackexchange/blob/main/select_on_test.ipynb)               | [Demonstrate that a model can simultaneously be <br>selected and evaluated on a test set](https://stats.stackexchange.com/a/570680/337906)                       |
| (external) [`copa.ipynb`](https://github.com/kddubey/cappr/blob/main/demos/superglue/copa.ipynb)                      | [Demonstrate that a more usable version of <br>zero-shot text classification works](https://stats.stackexchange.com/q/601159/337906)                             |
| [`train_on_test_features`](https://github.com/kddubey/stats-stackexchange/tree/main/train_on_test_features)           | [Is training on test set features (not labels) ok?](https://stats.stackexchange.com/q/611877/337906)                                                             |
| [`sample_via_gumbel`](https://github.com/kddubey/stats-stackexchange/blob/main/sample_via_gumbel)                     | [Demonstrate that one can sample directly in <br>log-space](https://stackoverflow.com/a/76230531/18758987)                                                       |
| [`precision_drop.ipynb`](https://github.com/kddubey/stackexchange/blob/main/precision_drop.ipynb)                     | A simple answer to: why did precision drop in <br>production?                                                                                                    |
| [`auprc.ipynb`](https://github.com/kddubey/stackexchange/blob/main/auprc.ipynb)                                       | [Demonstrate that intuitive ways to reduce model <br>compute result in optimistic average precision <br>scores](https://stats.stackexchange.com/a/623015/337906) |


## Setup

Create an environment `se` using venv:

```
cd /your/venvs

python -m venv se

source se/bin/activate

python -m pip install -r /path/to/stackexchange/requirements.txt
```

If the notebook says that it needs to run on a GPU machine, and you have a Google
account, [open the notebook in Google
Colab](https://stackoverflow.com/a/67344477/18758987).


## Usage

Interact w/ the code via Jupyter. I like [VS code notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
