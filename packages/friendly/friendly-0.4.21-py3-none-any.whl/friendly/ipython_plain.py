from friendly import current_lang
from friendly_traceback.functions_help import add_help_attribute
from ._ipython import *  # noqa
from ._ipython import version
from friendly_traceback import __version__

_ = current_lang.translate

# We do not want to install Rich so that %pprint will work
set_formatter("repl")  # noqa
print(
    f"friendly_traceback {__version__}; friendly {version}.\nType 'Friendly' for information."
)


def set_formatter(_arg=None):
    print(_("set_formatter is not supported by ipython_plain."))


add_help_attribute({"set_formatter": set_formatter})
helpers["set_formatter"] = set_formatter
Friendly.add_helper(set_formatter)

del colorama