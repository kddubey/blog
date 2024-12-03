import typing


def _is_nonempty_iterable(obj) -> bool:
    try:
        iterator = iter(obj)
        next(iterator)
    except:
        return False
    else:
        return True


def type_str(obj) -> str:
    """
    Returns a string representation for the type of data stored inside `obj`, beyond
    what `obj.__class__.__name__` might tell you. If `obj` is not iterable or is an
    empty iterable, returns `obj.__class__.__name__`.
    """
    map_edge_cases = {"NoneType": "None"}  ## are there are more like these?
    ## some manual handling of two edge cases
    if not _is_nonempty_iterable(obj):
        type_ = obj.__class__.__name__
        return map_edge_cases.get(type_, type_)
    if isinstance(obj, str):
        ## it's iterable, but we know it's just a string.
        ## is there an ABC which covers these sort of types?
        return obj.__class__.__name__
    types = set()
    for elt in obj:
        cls_name = elt.__class__.__name__
        ## cases are in increasing order of generality
        if isinstance(elt, typing.Mapping):
            type_keys = type_str(elt.keys())
            type_vals = type_str(elt.values())
            type_ = f"{cls_name}[{type_keys}, {type_vals}]"
        elif isinstance(elt, str):
            type_ = "str"
        elif (
            isinstance(elt, typing.Sequence)
            and not isinstance(elt, typing.MutableSequence)
            and _is_nonempty_iterable(elt)
        ):
            ## immutable sequence => there are a specific set of types.
            ## so show all of them.
            _types = ", ".join([type_str(e) for e in elt])
            type_ = f"{cls_name}[{_types}]"
        elif _is_nonempty_iterable(elt):
            _types = type_str(elt)
            type_ = f"{cls_name}[{_types}]"  ## not a dict, so just one type in []
        else:
            type_ = cls_name
        types.add(map_edge_cases.get(type_, type_))
    if len(types) >= 2:
        return " | ".join(sorted(types))
    else:
        return list(types)[0]
