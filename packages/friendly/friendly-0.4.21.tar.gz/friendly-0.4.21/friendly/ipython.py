from ._ipython import *  # noqa
from ._ipython import version
from friendly_traceback import __version__
from IPython.core import magic  # noqa
from friendly import current_lang

_ = current_lang.translate
# By default, we assume a terminal with a dark background.
set_formatter("dark")  # noqa
print(
    f"friendly_traceback {__version__}; friendly {version}.\nType 'Friendly' for information."
)


@magic.register_line_cell_magic
def pprint(_line=None, _cell=None):
    print(
        _(
            "'%pprint' is not supported by Rich (used by friendly).\n"
            "If you absolutely need to use '%pprint', restart ipython\n"
            "and import friendly.ipython_plain instead of friendly.ipython."
        )
    )