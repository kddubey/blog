# My blog

Here also lies a list of my [contributions to open source
software](https://github.com/kddubey/stackexchange/blob/main/oss.md).


## Posts

Mostly simulations for some questions and answers on
[stats.stackexchange.com](https://stats.stackexchange.com/users/337906/) and
[stackoverflow.com](https://stackoverflow.com/users/18758987/).

[[post]](https://stats.stackexchange.com/a/570680/337906)
[`select_on_test.ipynb`](./select_on_test.ipynb): Demonstrate that a model can
simultaneously be selected and evaluated on a test set

[[post]](https://stats.stackexchange.com/a/614033)
[`train_on_test_features`](./train_on_test_features): For high rank data and a small
test set, train a PCA on test set features to boost test set performance!

[`precision_drop.ipynb`](./precision_drop.ipynb): A simple answer to: why did precision
drop in production?

[[post]](https://stats.stackexchange.com/a/623015/337906)
[`auprc.ipynb`](./auprc.ipynb): Demonstrate that integral approximators are trying to
hurt you

[`db_sampling_rate.ipynb`](./db_sampling_rate.ipynb): Calculate a sampling rate for a
database query

[[post]](https://stats.stackexchange.com/q/623900/337906)
[`negative_vs_downsampling.ipynb`](./negative_vs_downsampling.ipynb): What's
the need to formulate negative sampling for contrastive training? (not done)

[`to_batch_or_not_to_batch`](./to_batch_or_not_to_batch): Mathematically analyze
and demo continuous batching (bad!)

[[post]](https://stats.stackexchange.com/q/568492/337906)
[`var_pred_var_error`](./var_pred_var_error): Does higher variance in predictions result
in higher variance error estimation?

[[post]](https://stackoverflow.com/a/76230531/18758987)
[`sample_via_gumbel`](./sample_via_gumbel): Demonstrate that one can sample directly in
log-space

[[post]](https://stats.stackexchange.com/q/601159/337906)
[`cappr`](https://github.com/kddubey/cappr/): Demonstrate that a more usable version of
zero-shot text classification works

[`langchain_save_all`](./langchain_save_all): Save all method calls. Inspired by [this
issue](https://github.com/langchain-ai/langchain/issues/912)

My dumber code dumps are in [dumpy](https://github.com/kddubey/dumpy).


## Setup

Need Python 3.8+

Create an environment `blog` using venv:

```
cd /your/venvs

python -m venv blog

source blog/bin/activate

python -m pip install -r /path/to/blog/requirements.txt
```

If the notebook says that it needs to run on a GPU machine, and you have a Google
account, [open the notebook in Google
Colab](https://stackoverflow.com/a/67344477/18758987).


## Usage

Interact w/ the code via Jupyter. I like [VS code
notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
