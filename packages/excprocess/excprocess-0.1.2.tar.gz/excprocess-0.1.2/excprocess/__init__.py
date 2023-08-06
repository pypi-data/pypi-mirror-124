__version__ = '0.1.2'



import subprocess
import json

from importlib import import_module

from .exceptions import UnknownSubprocessException, InvalidSubprocessExceptionOutput



_template = """
import json
from sys import stderr

try:
{code}
    
except Exception as e:
    pickled = json.dumps(dict(
        module = e.__class__.__module__,
        name = e.__class__.__name__,
        args = e.args
    ))
    stderr.write(pickled)
"""


def run(code: str, python_path: str = 'python', reraise: bool = True, *args, **kwargs):
    """Run Python code in a subprocess.
    Any exception that is raised within the process is poorly sent outside to be reraised.
    """

    # Indent lines
    code = '\n'.join([f'    {line}' for line in code.splitlines()])

    # Insert into template
    code = _template.format(code=code)

    # Run process and raise any potential exceptions within
    stderr = subprocess.run(
        [python_path, '-c', code],
        capture_output=True, text=True,
        *args, **kwargs
    ).stderr

    if stderr:
        # Load JSON object passed by the subprocess
        try:
            exc_info = json.loads(stderr)
        except json.JSONDecodeError:
            raise InvalidSubprocessExceptionOutput(
                    'Subprocess did not return a JSON object')
        

        # Attempt to import the exception type and raise it
        if reraise:
            try:
                module = import_module(exc_info['module'])
                exc_type = getattr(module, exc_info['name'])

            except (ModuleNotFoundError, AttributeError):
                raise UnknownSubprocessException(
                        f'Exception could not be found: {exc_info["module"]}.{exc_info["name"]}')

            except KeyError:
                raise InvalidSubprocessExceptionOutput(
                        'Subprocess did not return information about the exception in a valid format')

            raise exc_type(*exc_info['args'])

        return exc_info
    
    return None