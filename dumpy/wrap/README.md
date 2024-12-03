# Function utilities

Decorators which automate some things about docstrings and function annotations. They
dynamically modify the function's `__doc__` and `__annotations__` attributes, so static
code analyzers unfortunately won't reflect the modifications. After using these
decorators, I realized that I like being able to rely on docstrings that static code
analyzers show me. I assume other users do to. So I opted for copy-pasting parts of
docstrings instead of using these automations.
