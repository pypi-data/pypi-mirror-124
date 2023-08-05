from .errors import ExecuteError


def execute(code, *args):
    if code == "add to the end of array":
        if not isinstance(args[0], list):
            raise ExecuteError("First argument must be a list!")
        args[0].append(args[1])
        return args[1]