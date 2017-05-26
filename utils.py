import sys

class Error:
    @staticmethod
    def fatal(process, error, action, message):
        print("[ERROR] [{}] {}".format(process, error))
        print(".......{} while {}".format(message, action))
        sys.exit(1)

    @staticmethod
    def warn(process, warning, action, message):
        print("[WARNING] [{}] {}".format(process, warning))
        print(".........{} while {}".format(message, action))

    @staticmethod
    def info(process, info, action, message):
        print("[INFO][{}] {}".format(process, info))
        print("......{} while {}".format(message, action))

class Result:
    def __init__(self, state, value):
        self._state = state
        self._value = value

    @classmethod
    def success(cls, value):
        return cls(True, value)

    @classmethod
    def failure(cls, value):
        return cls(False, value)

    def is_success(self):
        return self._state

    def is_failure(self):
        return not self._state

    def unwrap(self):
        if not self._state:
            raise ValueError("Unwrapped result in failure state")

        else:
            return self._value

    def unwrap_err(self):
        if self._state:
            raise ValueError("Unwraped error from result in success state")

        else:
            return self._value



