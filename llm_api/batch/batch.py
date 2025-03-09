"""
Batch inputs, pack each batch into a prompt, and get completions.
"""

from math import ceil
from typing import Generic, Iterable, Sequence, TypeVar

import openai
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.lib.streaming.chat import ChatCompletionStream
from pydantic import BaseModel, create_model
from tqdm.auto import tqdm


def batch_texts_by_token_count(
    texts: Iterable[str],
    max_tokens: int,
    avg_num_chars_per_token: float = 4.0,
    max_batch_size: int = 100,  # TODO: there's a max # parameters for most schemas
):
    """
    Generate batches of texts with at most `max_tokens` per batch.
    Tokens are roughly counted according to `avg_num_chars_per_token`.

    If a text exceeds `max_tokens`, it's in its own batch. **It isn't truncated.**

    Parameters
    ----------
    texts : Iterable[str]
        _description_
    max_tokens : int
        _description_
    avg_num_chars_per_token : float, optional
        _description_, by default 4.0

    Yields
    ------
    _type_
        _description_
    """

    batch: list[str] = []
    num_tokens_batch_estimate = 0
    for text in texts:
        num_tokens_text_estimate = ceil(len(text) / avg_num_chars_per_token)

        if num_tokens_text_estimate > max_tokens:
            if batch:
                # Yield existing batch first to maintain the order of texts.
                yield batch
            yield [text]
            batch = []
            num_tokens_batch_estimate = 0
            continue

        if num_tokens_batch_estimate + num_tokens_text_estimate > max_tokens:
            yield batch
            batch = []
            num_tokens_batch_estimate = 0
        batch.append(text)
        num_tokens_batch_estimate += num_tokens_text_estimate

    if batch:
        # The last batch didn't hit max_tokens. It needs to be yielded.
        yield batch


def _input_ids(texts: list[str]) -> list[str]:
    return [f"input_{idx}" for idx in range(1, len(texts) + 1)]


def _batch_instructions(input_ids: list[str]) -> str:
    input_ids_str = "\n".join(input_ids)
    return (
        "You will be given a sequence of inputs. Each input is identified like so: "
        "input_{id}."
        "You must return a result for each input. Here are the input IDs you need to "
        "return results for:"
        f"{input_ids_str}"
    )


def _id_texts(input_ids: list[str], texts: list[str]) -> list[str]:
    inputs = [
        f"{input_id}: {text}" for input_id, text in zip(input_ids, texts, strict=True)
    ]
    delim = "\n\n-------\n\n"
    inputs_str = delim.join(inputs)
    return inputs_str


ResponseFormat = TypeVar("ResponseFormat", bound=BaseModel)


class Batch(BaseModel, Generic[ResponseFormat]):
    def _single_response(self, input_id: str) -> ResponseFormat:  # for type inference
        return getattr(self, input_id)


def _create_batched_response_format(
    response_format: type[ResponseFormat], input_ids: list[str]
) -> type[Batch[ResponseFormat]]:
    model_name = f"BatchOf{response_format.__name__}"
    field_definitions = {input_id: (response_format, ...) for input_id in input_ids}
    return create_model(model_name, __base__=Batch[ResponseFormat], **field_definitions)


def _responses(
    input_ids: list[str],
    completion: ParsedChatCompletion[Batch[ResponseFormat]],
) -> list[ResponseFormat]:
    batched_response = completion.choices[0].message.parsed
    if batched_response is None:
        raise ValueError("The batched response is None :-(")
    return [batched_response._single_response(input_id) for input_id in input_ids]


def _stream_responses(stream: ChatCompletionStream[ResponseFormat], num_responses: int):
    # TODO: need to make sure we yield the depth=1 ResponseFormat, not any deeper. Maybe
    # can input depth or something ha.
    # num_responses is for tqdm
    raise NotImplementedError()
    for event in stream:
        if event.type == "content.delta":
            if event.parsed is not None:
                # Print the parsed data as JSON
                print("content.delta parsed:", event.parsed)
        elif event.type == "content.done":
            print("content.done")
        elif event.type == "error":
            print("Error in stream:", event.error)


def _handle_tools():
    # TODO: pretty sure this is possible, not sure about accuracy.
    raise NotImplementedError()


def complete_batch(
    client: openai.OpenAI,
    batch: list[str],
    response_format: type[ResponseFormat],
    messages: list[ChatCompletionMessageParam],
    instruction: str = "",
    **openai_parse_kwargs,
):
    input_ids = _input_ids(batch)
    batch_instruction = _batch_instructions(input_ids)
    inputs_str = _id_texts(input_ids, batch)
    BatchOfResponseFormat = _create_batched_response_format(response_format, input_ids)
    messages_batch = [
        {"role": "developer", "content": "\n".join([instruction, batch_instruction])},
        {"role": "user", "content": inputs_str},
    ]
    completion = client.beta.chat.completions.parse(
        messages=messages + messages_batch,
        response_format=BatchOfResponseFormat,
        **openai_parse_kwargs,
    )
    # TODO: option to stream
    responses = _responses(input_ids, completion)
    return responses


def complete(
    client: openai.OpenAI,
    texts: Iterable[str],
    response_format: type[ResponseFormat],
    max_tokens: int = 10_000,  # rename this
    avg_num_chars_per_token: float = 4.0,
    messages: Iterable[ChatCompletionMessageParam] | None = None,
    instruction: str = "",
    **openai_parse_kwargs,
):
    if messages is None:
        messages = []
    else:
        messages = list(messages)

    # TODO: send a small batch to estimate # tokens per completion
    # Then adjust max_tokens accordingly

    batches = batch_texts_by_token_count(texts, max_tokens, avg_num_chars_per_token)
    if isinstance(texts, Sequence):
        # It's fine to generate all the batches so we can show a progress bar
        batches = list(batches)
        batches = tqdm(batches, total=len(batches), desc="Completing batches")

    for batch in batches:
        yield complete_batch(
            client,
            batch,
            response_format,
            messages,
            instruction=instruction,
            **openai_parse_kwargs,
        )
