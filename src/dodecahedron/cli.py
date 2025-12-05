# -*- coding: utf-8 -*-
"""Command-Line Interface

The command-line interface is a wrapper around the argparse library which receives
any arguments the user provides and calls the appropriate service function.

"""

# pylint: disable=no-self-use

# Standard Library Imports
import argparse
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Constants
PROCESS = "process"


class AbstractCommandLineInterface:
    """Class represents an abstract command-line interface (CLI)."""

    def __init__(
        self,
        __parser: argparse.ArgumentParser,
        __processes: Dict[str, Callable[..., None]],
    ) -> None:
        log.debug("Starting command-line interface...")
        self._parser = __parser
        self._processes = __processes
        self._add_process_argument()
        self._parser.set_defaults(func=self.execute)

    def __call__(self, argv: argparse.Namespace) -> None:
        self.execute(argv)

    def _add_process_argument(self) -> None:
        """Add process argument to parser."""
        self._parser.add_argument(
            PROCESS,
            type=str,
            choices=list(self._processes.keys()),
            help=f"{PROCESS} to run",
        )

    def execute(self, argv: Optional[argparse.Namespace] = None) -> None:
        """Executes a function based on the provided arguments.

        Args:
            argv: List of command line arguments passed.

        """
        args = (
            self._parser.parse_args(argv)
            if not isinstance(argv, argparse.Namespace)
            else argv
        )

        process: str = getattr(args, PROCESS)

        log.debug("Executing '%s' process...", process)
        self._run_process(process.lower())

    def _run_process(
        self,
        __process: str,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Run process.

        Args:
            __process: Name of process.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        """
        process = self._processes[__process]
        process(*args, **kwargs)
