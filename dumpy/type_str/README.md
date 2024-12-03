# Precise types for iterables

Calling `.info()` or `.dtypes` on a dataframe is a typical step before starting any data
analysis. But the outputs can be uninformative for data pulled from Postgres. Arrays are
converted to lists, and JSONBs are converted to dictionaries. These get the
uninformative type `object` when pandas checks data types.

`type_str` gives accurate and more precise data types in the style of type hints. Use it
by running `df.apply(type_str)` in place of `df.dtypes`. You can actually use it to peek
into any opaque iterable. But note that `type_str` works recursively and scales poorly,
so maybe don't use it production :-)
