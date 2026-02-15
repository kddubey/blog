# Matryoshka experiments

Experiments inspired by the [MRL paper](https://arxiv.org/abs/2205.13147).

[`./memory`](./memory) sees how much memory is saved by backwarding inside the loop over
dims instead of appending to the computation graph. It won't save much b/c savings only
scale w/ the batch size and the number of final embedding tensors. The number of them
scales w/ $\log_2 d$ where $d$ is the model's full embedding dimension. And the
embeddings themselves are small in comparsion to all of the model's parameters.

The notebook [`./matryoshka.ipynb`](./matryoshka.ipynb) does some gradient analysis on a
toy problem to see if the Matryoshka effect can be achieved via vector re-scaling. Looks
like the answer is no. This idea is then empirically evaluated in
[`./train.ipynb`](./train.ipynb), which confirms that re-scaling isn't sufficient. Also
see Tom Aarsen's [similar
research](https://github.com/UKPLab/sentence-transformers/pull/2593#issuecomment-2056720029).
