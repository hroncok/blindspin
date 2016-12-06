import sys
import threading
import time
import itertools


class Spinner(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self, force=False):
        self._force = force
        self.stop_running = None
        self.spin_thread = None

    def start(self):
        if sys.stdout.isatty() or self._force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.25)
            sys.stdout.write('\b')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def spinner(force=False):
    """This function creates a context manager that is used to display a
    spinner on stdout as long as the context has not exited.

    The spinner is created only if stdout is not redirected, or if the spinner
    is forced using the `force` parameter.

    Parameters:

      force (bool): Force creation of spinner even when stdout is redirected.

    Example usage::

        with spinner():
            do_something()
            do_something_else()

    """
    return Spinner(force)


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
