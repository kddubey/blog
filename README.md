# stackexchange

Simulations for my questions and answers on
[stats.stackexchange.com](https://stats.stackexchange.com/users/337906/) and
[stackoverflow.com](https://stackoverflow.com/users/18758987/).

And some other random things.

Here also lies a list of my [contributions to open source
software](https://github.com/kddubey/stackexchange/blob/main/oss.md).


| dir/file link                                                                                                         | q/a link                                                                                                                                                  |
|-----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`select_on_test.ipynb`](https://github.com/kddubey/stats-stackexchange/blob/main/select_on_test.ipynb)               | [Demonstrate that a model can simultaneously be <br> selected and evaluated on a test set](https://stats.stackexchange.com/a/570680/337906)               |
| [`train_on_test_features`](https://github.com/kddubey/stats-stackexchange/tree/main/train_on_test_features)           | [For high rank data and a small test set, train <br> a PCA on test set features to boost test set performance!](https://stats.stackexchange.com/a/614033) |
| [`precision_drop.ipynb`](https://github.com/kddubey/stackexchange/blob/main/precision_drop.ipynb)                     | A simple answer to: why did precision drop in <br> production?                                                                                            |
| [`auprc.ipynb`](https://github.com/kddubey/stackexchange/blob/main/auprc.ipynb)                                       | [Demonstrate that integral approximators are <br> trying to hurt you](https://stats.stackexchange.com/a/623015/337906)                                    |
| [`db_sampling_rate.ipynb`](https://github.com/kddubey/stackexchange/blob/main/db_sampling_rate.ipynb)                 | Calculate a sampling rate for a database query                                                                                                            |
| [`negative_vs_downsampling.ipynb`](https://github.com/kddubey/stackexchange/blob/main/negative_vs_downsampling.ipynb) | (not done) [What's the need to formulate negative <br> sampling for contrastive training?](https://stats.stackexchange.com/q/623900/337906)               |
| [`to_batch_or_not_to_batch`](https://github.com/kddubey/stackexchange/tree/main/to_batch_or_not_to_batch)             | (bad!) Mathematically analyze and demo dynamic <br> batching                                                                                              |
| [`var_pred_var_error`](https://github.com/kddubey/stats-stackexchange/tree/main/var_pred_var_error)                   | [Does higher variance in predictions result in <br> higher variance error estimation?](https://stats.stackexchange.com/q/568492/337906)                   |
| [`sample_via_gumbel`](https://github.com/kddubey/stats-stackexchange/blob/main/sample_via_gumbel)                     | [Demonstrate that one can sample directly in <br> log-space](https://stackoverflow.com/a/76230531/18758987)                                               |
| (external) [`cappr`](https://github.com/kddubey/cappr)                                                                | [Demonstrate that a more usable version of <br> zero-shot text classification works](https://stats.stackexchange.com/q/601159/337906)                     |
| [`langchain_save_all.ipynb`](https://github.com/kddubey/stackexchange/blob/main/langchain_save_all.ipynb)             | Save all method calls. Inspired by [this issue](https://github.com/langchain-ai/langchain/issues/912)                                                     |

My dumber code dumps are in [dumpy](https://github.com/kddubey/dumpy).

## Setup

Need Python 3.8+

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

Interact w/ the code via Jupyter. I like [VS code
notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
