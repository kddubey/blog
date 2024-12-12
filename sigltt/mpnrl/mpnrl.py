"""
MPNRL = MultiplePositivesNegativesRankingLoss

Sigmoid lets us pass multiple positives at once per anchor. They're treated as a bunch
of independent classifications.
"""

from collections import defaultdict
from typing import Any, Iterable

from datasets import Dataset
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.data_collator import SentenceTransformerDataCollator
import torch


def group_positives_by_anchor(
    dataset: Iterable[dict[str, str]],
) -> dict[str, dict[str, None]]:
    anchor_to_positives = defaultdict(dict)
    # Using a dict to de-duplicate. Not using a set so that positives and negatives are
    # in a deterministic (insertion) order.
    for record in dataset:
        anchor_to_positives[record["anchor"]][record["positive"]] = None
    return anchor_to_positives


class MPNRLDataCollator(SentenceTransformerDataCollator):
    def __init__(self, dataset: Dataset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO: SentenceTransformerDataCollator actually assumes that first is anchor,
        # next is positive, rest are negative, regardless of the actual column names.
        # Here, we assume they're labeled "anchor", "positive", "negative".
        self.anchor_to_positives = group_positives_by_anchor(dataset)

    def __call__(self, features: list[dict[str, str]]):
        # Using a dict for deterministic (insertion) order.
        anchors = list({record["anchor"]: None for record in features})
        positives = list({record["positive"]: None for record in features})
        negatives = list({record["negative"]: None for record in features})

        positive_idxs = [
            [
                j
                for j, positive in enumerate(positives)
                if positive in self.anchor_to_positives[anchor]
            ]
            for anchor in anchors
        ]
        # positive_idxs[i] is a list of all indices of positives which are positives for
        # anchors[i]. It's structured like this (instead of, e.g., a flat list of (i, j)
        # pairs) b/c it may be useful to batch by anchors later.

        # TODO: this is gettin hacky
        batch = (
            super().__call__([{"anchor": anchor} for anchor in anchors])
            | super().__call__([{"positive": positive} for positive in positives])
            | super().__call__([{"negative": negative} for negative in negatives])
        )
        batch["label"] = positive_idxs
        return batch

    def maybe_warn_about_column_order(self, *args, **kwargs):
        # TODO: this is temporarily overriden and suppressed.
        pass


class MultiplePositivesNegativesRankingLoss(torch.nn.Module):
    def __init__(
        self,
        model: SentenceTransformer,
        scale: float = 20.0,
        similarity_fct=util.cos_sim,
        bias: float = -10.0,
    ) -> None:
        super(MultiplePositivesNegativesRankingLoss, self).__init__()
        self.model = model
        self.scale = torch.nn.Parameter(torch.tensor(scale, device=model.device))
        self.similarity_fct = similarity_fct
        self.bias = torch.nn.Parameter(torch.tensor(bias, device=model.device))
        # TODO: the learning rate for scale and bias should probably be higher. See
        # https://github.com/UKPLab/sentence-transformers/blob/679ab5d38e4cf9cd73d4dcf1cda25ba2ef1ad837/sentence_transformers/trainer.py#L1206-L1219
        self.bce_with_logits_loss = torch.nn.BCEWithLogitsLoss(reduction="sum")

    def forward(
        self, sentence_features: Iterable[dict[str, torch.Tensor]], labels: torch.Tensor
    ) -> torch.Tensor:
        # Compute the embeddings and distribute them to anchor and candidates (positive and optionally negatives)
        embeddings = [
            self.model(sentence_feature)["sentence_embedding"]
            for sentence_feature in sentence_features
        ]
        anchors = embeddings[0]  # (batch_size, embedding_dim)
        candidates = torch.cat(
            embeddings[1:]
        )  # (batch_size * (1 + num_negatives), embedding_dim)

        # For every anchor, we compute the similarity to all other candidates (positives and negatives),
        # also from other anchors. This gives us a lot of in-batch negatives.
        scores: torch.Tensor = (
            self.similarity_fct(anchors, candidates) * self.scale
        ) + self.bias
        # (batch_size, batch_size * (1 + num_negatives))

        positive_pairs: list[list[int]] = labels
        labels = torch.zeros_like(scores)
        for i, positive_indices in enumerate(positive_pairs):
            for j in positive_indices:
                labels[i, j] = 1.0

        return self.bce_with_logits_loss(scores, labels) / len(anchors)

    def get_config_dict(self) -> dict[str, Any]:
        return {
            "scale": self.scale.item(),
            "similarity_fct": self.similarity_fct.__name__,
            "bias": self.bias.item(),
        }

    @property
    def citation(self) -> str:
        return """
@inproceedings{zhai2023sigmoid,
    title={Sigmoid loss for language image pre-training},
    author={Zhai, Xiaohua and Mustafa, Basil and Kolesnikov, Alexander and Beyer, Lucas},
    booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
    pages={11975--11986},
    year={2023}
}
"""
