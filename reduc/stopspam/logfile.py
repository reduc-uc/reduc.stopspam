import os


class LogFile:
    """Helper class for log files.

    This class offers a read() method that returns the file content since the
    last read() invocation. It is smart enough to detect if the file has been
    rotated, in which case, read() returns the rest of the old file, plus the
    full content of the new one. It detects file rotation by opening it again
    and checking if its first line has changed.
    """
    def __init__(self, filename):
        self.filename = filename
        self._open()

    def read(self):
        """Returns the content added since last read."""
        text = self.file.read()

        if self._has_rotated():
            self._open()
            text = text + self.file.read()

        return text

    def seek_end(self, pos=0):
        """Jumps to the end of the file."""
        self.file.seek(pos, os.SEEK_END)

    def _open(self):
        """Opens the log file for reading."""
        self.file = open(self.filename)
        self.firts_line = self._get_first_line()

    def _has_rotated(self):
        """True if the file has been log rotated."""
        return self.firts_line != self._get_first_line()

    def _get_first_line(self):
        """Gets the first line of the current file"""
        f = open(self.filename)
        line = f.readline()
        f.close()
        return line
