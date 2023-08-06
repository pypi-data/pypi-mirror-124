

class ExcprocessError(Exception):
    """Generic exception for excprocess"""


class UnknownSubprocessException(ExcprocessError):
    """A type of exception has occurred within the subprocess,
    that cannot be found and imported in the outside Python environment.
    """


class InvalidSubprocessExceptionOutput(ExcprocessError):
    """Subprocess output cannot be interpreted"""