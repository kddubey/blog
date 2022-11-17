# stats-stackexchange
Simulations for [my questions and answers on stats.stackexchange.com](https://stats.stackexchange.com/users/337906/chicxulub).


| dir/file link                                                                                                       | q/a link                                                                                                                               |
|---------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| [`var_pred_var_error`](https://github.com/kddubey/stats-stackexchange/tree/main/var_pred_var_error)                 | [Does higher variance in predictions <br>result in higher variance error estimation?](https://stats.stackexchange.com/q/568492/337906) |
| [`model_vs_noisy_labels.ipynb`](https://github.com/kddubey/stats-stackexchange/blob/main/model_vs_noisy_labels.ipynb) | [Verify that a model can outperform its <br>noisy training labels](https://stats.stackexchange.com/a/580894/337906)                      |
| [`select_on_test.ipynb`](https://github.com/kddubey/stats-stackexchange/blob/main/select_on_test.ipynb)             | [Verify that a model can simultaneously be <br>selected and evaluated on a test set](https://stats.stackexchange.com/a/570680/337906)  |

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

```bash
conda env create -f environment.yml

conda activate stats-se
```

## Usage

Interact w/ the code via Jupyter. I like [VS code notebooks](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

## Future questions

### Model selection + decision theory

In most cases we care about Var(test error) to some degree.

Something I'm trying to get at: say the expected errors (so we don’t have to
think about inferring from observed errors) are:

| model | train error | test error |
|-------|-------------|------------|
| A     | 0           | 0.1        |
| B     | 0.1         | 0.101      |

How much does one have to care about Var(test error) to select model B over A?
Does E(test error) - E(train error) > other model's tell you that
Var(test predictions) is greater than the other model's? (Though still need to
prove/demonstrate that Var(test predictions) => higher Var(test error).)

### Hierarchical labels

Say labels are hierarchical. Are higher-level classification problems easier
than lower-level ones? If the # examples per class is the same, are they
equivalently hard?

Hypothesis: lower-level is harder in former case, equivalent in latter, i.e.,
only thing that matters is # examples per class.

### Fixed test set vs sampled

Keep eval data fixed or random? How biased will further evaluations on a fix set
of test data become?

Hypothesis: fixed is slightly better for a limited # evaluations b/c model
differences are paired => more precision in model selection. This effect is
even more pronounced for problems where Var(predictions) is high.

### "Extreme" classification

Is metric learning a good solution to the problem of "extreme" (i.e., super
high # classes + variable set) classification? We know it’s a way to get good
embeddings, but what about the separate task of classification?

Hypothesis: don’t have one yet. Read
