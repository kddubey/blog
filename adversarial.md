# Random questions in adversarial ML


## Transferability

Update: found [Universal and Transferable Adversarial Attacks
on Aligned Language Models](https://arxiv.org/abs/2307.15043).

Are there systematic studies of transferability of white-box attacks against black-box
target models? Say, as done in [Are aligned neural networks adversarially
aligned?](https://arxiv.org/abs/2306.15447) by Carlini et al. (2023), an attack is
learned using Vicuña. This attack works on GPT-3.5 and GPT-4, which isn't super
surprising b/c Vicuña was trained on GPT-3.5 completions. Surprisingly, this attack also
works against Gemini and Claude. I'd like to see a more systematic study where we know
whether or not the white-box model was trained on a target, black-box model's outputs.
I'd like to see if this study replicates across many text and image generation attacks.

Also, do attacks using Llama work on GPT-x? If these attacks are not transferable to
target black-box models, can a more transferable attack be found by training it on a
handful of diversely-trained of white-box models?

(Side question: how do you efficiently generate many attacks? I'll read up on that.
Maybe it's as easy as stochastic weight averaging. But maybe those are
easily/simulataneously defended against?)


## Is formatting a reasonable defense?

Update: found [Misusing Tools in Large Language Models With Visual Adversarial Examples
](https://arxiv.org/abs/2310.03185).

Proposed and anectodally validated
[here](https://www.promptingguide.ai/risks/adversarial#quotes-and-additional-formatting).

Is completion-formatting (via grammars / token-generation constraints) a viable defense
to attacks which are optimized to generate certain prefixes? Say the attacker doesn't
know what the format looks like—they can only make an educated guess.

Here's an example. I'm trying to get a refund when chatting w/ an automated customer
service agent. Internally, the agent generates completions in a JSON format like so:

```json
{
    ...,
    "refund": {
        ...,
        "amount": [float],
        ...
    },
    ...
}
```

But I don't know that. So I generate an attack by maximizing the likelihood of the
completion `"refund_amount": 100.00,`. How often, if ever, does a completion formatter
end up generating this:

```json
{
    ...,
    "refund": {
        ...,
        "amount": 100.00,
        ...
    },
    ...
}
```

What happens if you beef up system instructions and train against that?

The attack can be in text or images.
