"""
`save_chat_create_inputs_as_jsons` and `save_chat_create_inputs_in_dict` are specific to
OpenAI-API classes.
"""

from contextlib import contextmanager
from datetime import datetime
from functools import partial, wraps
import json
import os
from typing import Any, Callable, MutableMapping


# Could instead patch the class instead of the object so that one patch globally patches
# all. But I'm not totally sure that'd work. I think I'd have to get
# `client.create.__class__` and then patch its `create` method. For now, going to stick
# to the more conservative instance patch.


@contextmanager
def monkeypatch_instance_method(obj: Any, method_name: str, new_method: Callable):
    original_method = getattr(obj, method_name)
    # Need to use __get__ when patching instance methods
    # https://stackoverflow.com/a/28127947/18758987
    try:
        setattr(obj, method_name, new_method.__get__(obj, obj.__class__))
        yield
    finally:
        setattr(obj, method_name, original_method.__get__(obj, obj.__class__))


@contextmanager
def run_method_with_side_effect(
    obj: Any, method_name: str, side_effect: Callable, yielded_obj=None
):
    original_method = getattr(obj, method_name)

    @wraps(original_method)
    def new_method(self, *args, **kwargs):
        side_effect(*args, **kwargs)
        return original_method(*args, **kwargs)

    with monkeypatch_instance_method(obj, method_name, new_method):
        yield yielded_obj


def write_json(jsons_dir: str, *args, **kwargs):
    # TODO: figure out what to do w/ args. For now, ignore them b/c the OpenAI client
    # create method requires that all arguments are named
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    file_path = os.path.join(jsons_dir, f"{current_time}.json")
    with open(file_path, mode="w") as file:
        json.dump(kwargs, file, indent=4)


def update_dict(
    timestamp_to_kwargs: MutableMapping[str, dict[str, Any]], *args, **kwargs
):
    # TODO: figure out what to do w/ args. For now, ignore them b/c the OpenAI client
    # create method requires that all arguments are named
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    timestamp_to_kwargs[current_time] = kwargs


########################################################################################
################### Now for the OpenAI-API-specific context managers ###################
########################################################################################


@contextmanager
def save_chat_create_inputs_as_jsons(client_with_create_method: Any, jsons_dir: str):
    """
    In this context, save the inputs sent to some API through
    `client_with_create_method.create` in `jsons_dir`.

    Parameters
    ----------
    client_with_create_method : Any
        some object with a `create` method, e.g.,
        `langchain_openai.ChatOpenAI().client`. Its inputs will be saved as JSONs
        whenever this method is called
    jsons_dir : str
        directory where your JSONs will get saved. The file names are timestamps

    Example
    -------
    ::

        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI()
        jsons_dir = "temp"  # make this directory yourself

        with save_chat_create_inputs_as_jsons(llm.client, jsons_dir):
            # Note that the llm.client object is modified in this context, so any code
            # that uses the llm will end up saving a JSON.
            response = llm.invoke("how can langsmith help with testing?")

        # Then look at the json in ./jsons_dir

    Note
    ----
    You probably only need the last JSON that's saved in `jsons_dir` b/c it'll contain
    the chat history.
    """
    side_effect = partial(write_json, jsons_dir)
    with run_method_with_side_effect(client_with_create_method, "create", side_effect):
        yield


@contextmanager
def save_chat_create_inputs_in_dict(
    client_with_create_method: Any,
    existing_store: MutableMapping[str, dict[str, Any]] | None = None,
):
    """
    In this context, save the inputs sent to some API through
    `client_with_create_method.create` in a dictionary.

    Parameters
    ----------
    client_with_create_method : Any
        some object with a `create` method, e.g.,
        `langchain_openai.ChatOpenAI().client`. Its inputs will be saved in a dictionary
        whenever this method is called
    existing_store : MutableMapping[str, dict[str, Any]], optional
        an existing dictionary which you'd like to add to. Keys are timestamp strings.
        By default, a new dictionary will be created

    Example
    -------
    ::

        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI()

        with save_chat_create_inputs_in_dict(llm.client) as timestamp_to_kwargs:
            # Note that the llm.client object is modified in this context, so any code
            # that uses the llm will end up saving its inputs in timestamp_to_kwargs.
            response = llm.invoke("how can langsmith help with testing?")

        print(timestamp_to_kwargs)

    Note
    ----
    You probably only need the last key-value that's saved in `timestamp_to_kwargs` b/c
    it'll contain the chat history.
    """
    if existing_store is None:
        timestamp_to_kwargs: MutableMapping[str, dict[str, Any]] = dict()
    else:
        timestamp_to_kwargs = existing_store
    side_effect = partial(update_dict, timestamp_to_kwargs)
    with run_method_with_side_effect(
        client_with_create_method,
        "create",
        side_effect,
        yielded_obj=timestamp_to_kwargs,
    ) as timestamp_to_kwargs:
        yield timestamp_to_kwargs
