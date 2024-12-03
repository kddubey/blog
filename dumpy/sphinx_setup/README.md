# Sphinx docs setup

This script automatically sets up [Sphinx](https://www.sphinx-doc.org/en/master/)
documentation in a style that's to my liking. My preferences are:
  * Separate source and build directories, because this structure is the one which the
    Read the Docs builder
    [assumes](https://docs.readthedocs.io/en/stable/tutorial/#preparing-your-project-on-github)
  * No "Submodule ...", "Subpackage ...", "...  module", and "... package" headers, as
    these distinctions shouldn't matter to the user
  * The code `[source]` button should link to the code in GitHub
      * I'm surprised at how much Googling (and some slightly unsuccessful ChatGPT-ing)
        I had to do to find a robust but bit-sized implementation of this. Big thanks to
        [this GitHub
        comment](https://github.com/readthedocs/sphinx-autoapi/issues/202#issuecomment-907582382)
  * Arguments in function signatures should be separated by newlines
  * Use the [PyData Sphinx
    Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html)
  * Use [NumPy
    docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).
    The default style is less readable as a developer and as a user (when I just wanna
    hover the code instead of opening up the documentation in my browser)
  * Use the `{package}.rst` file in the index, drop `modules.rst`.

Modify the global variables at the top of the script. Use at your own risk.
