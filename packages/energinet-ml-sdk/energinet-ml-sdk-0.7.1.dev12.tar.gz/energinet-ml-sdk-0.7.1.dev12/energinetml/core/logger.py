"""The logger module is essential for logging an experiment important numbers
doing a training.
"""
import os
import io
import sys
from energinetml.settings import (
    DEFAULT_RELATIVE_ARTIFACT_PATH,
    DEFAULT_LOG_FILENAME,
    DEFAULT_LOG_ENCODING,
    make_sys_std_err_name,
)


class ConsoleLogger(object):
    """This class enables logging of stdout and stderr.
    The class is used during local trainings and finally uploaded to the azure ml
    expirment.

    Args:
        console (io.TextIOWrapper, optional): Possible values
            [sys.stdout, sys.stderr]. Defaults to sys.stdout.
        path (str, optional): Relative path for the log file.
            Defaults to "./outputs".

    Returns:
        object: A console logger object which can be used to overwrite
            the default sys.std* object.
    """

    _filename: str = DEFAULT_LOG_FILENAME
    _encoding: str = DEFAULT_LOG_ENCODING
    _path: str = DEFAULT_RELATIVE_ARTIFACT_PATH

    def __init__(
        self,
        console: io.TextIOWrapper = sys.stdout,
    ):
        """Init ConsoleLogger with either sys.stdout or sys.stderr."""
        self.console = console

        self.filename: str = None
        self.suffix: str = None
        self.ext: str = None
        self.filepath: str = None

        self._check()
        self._init_log_file()

    def _check(self) -> None:
        """Performs check of input argument."""
        self.con_name = self.console.name
        test = (self.con_name == "<stdout>") | (self.con_name == "<stderr>")
        assert test, f"You used a not valid sys.std* > {self.con_name}"

    def _init_log_file(self) -> None:
        """Performs Initialization of the log file and further enrich the object."""

        os.makedirs(self._path, exist_ok=True)

        filename, self.ext = self._filename.split(".")
        self.suffix = "out" if self.con_name == "<stdout>" else "err"
        self.filename = make_sys_std_err_name(filename, self.suffix, self.ext)

        self.filepath = f"{self._path}/{self.filename}"
        self.log = open(self.filepath, "w", encoding=self._encoding)

    def isatty(self) -> bool:
        """A requried function for sys.stdout and sys.stderr.

        Returns:
            bool: This function will only return False.
        """
        return False

    def write(self, message: str) -> None:
        """A requried function for sys.stdout and sys.stderr.
        The function will both print to file and to console.

        Args:
            message (str): The string which needs to be appended to the log.
        """
        self.log.write(message)
        self.console.write(message)

    def flush(self):
        """The function flush the io buffer.
        This function is called before uploading to azure ml.
        """
        self.log.flush()


class MetricsLogger(object):
    """
    TODO
    """

    def echo(self, s):
        """
        :param str s:
        """
        raise NotImplementedError

    def log(self, name, value):
        """
        :param str name:
        :param typing.Any value:
        """
        raise NotImplementedError

    def tag(self, key, value):
        """
        :param str key:
        :param str value:
        """
        raise NotImplementedError

    def dataframe(self, name, df):
        """
        :param str name:
        :param pandas.DataFrame df:
        """
        raise NotImplementedError
