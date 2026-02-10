# -*- coding: utf-8 -*-
"""Command-Line Interface

The command-line interface is a wrapper around the argparse library which receives
arguments that the user provides and calls the appropriate service function.

"""

# pylint: disable=no-self-use

# Standard Library Imports
import abc
from argparse import ArgumentParser
from argparse import Namespace
import enum
import inspect
import logging
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union


# Initialize logger.
log = logging.getLogger("dodecahedron")

# Custom types
CommandLineArguments = Union[Namespace, Sequence[str]]

# Constants
PROCESS = "process"


class CommandLineInterface(abc.ABC):
    """Class implements a command-line interface (CLI).

    Args:
        parser: Parser.
        processes: Processes.

    Attributes:
        parser: Argument parser.

    """

    def __init__(
        self,
        parser: ArgumentParser,
        /,
        processes: Dict[str, Callable[..., None]],
    ) -> None:
        log.debug("Starting command-line interface...")
        self._parser = parser
        self._processes = processes
        self._parser.add_argument(
            PROCESS,
            type=str,
            choices=list(self._processes.keys()),
            help=f"{PROCESS} to run",
        )
        # TODO: Add arguments to parser from function signatures
        self._parser.set_defaults(func=self.execute)

    @property
    def parser(self) -> ArgumentParser:
        """Argument parser."""
        return self._parser

    @property
    def processes(self) -> Dict[str, Callable[..., None]]:
        """Processes."""
        return self._processes  # pragma: no cover

    def __call__(self, args: Namespace) -> None:
        self.execute(args)  # pragma: no cover

    def execute(
        self,
        args: Optional[CommandLineArguments] = None,
        /,
    ) -> None:
        """Execute function based on the provided argument(s).

        Args:
            args: Arguments passed to command line.

        """
        namespace = self._parse_arguments(args)
        process: str = getattr(namespace, PROCESS)
        self._execute_process(process.lower(), namespace)

    def _parse_arguments(
        self,
        args: Optional[CommandLineArguments],
        /,
    ) -> Namespace:
        """Parse command-line arguments.

        Args:
            args: Arguments passed to command line.

        """
        result = (
            self._parser.parse_args(args)
            if not isinstance(args, Namespace)
            else args
        )
        return result

    def _execute_process(
        self,
        __process: str,
        __namespace: Namespace,
        /,
    ) -> None:
        """Execute process.

        Args:
            __process: Name of process.
            __namespace: Namespace.

        """
        log.debug("Executing '%s' process...", __process)
        process = self._processes[__process]
        signature = inspect.signature(process)
        args = select_positional_arguments(__namespace, signature)
        kwargs = select_keyword_arguments(__namespace, signature)
        process(*args, **kwargs)


# ----------------------------------------------------------------------------
# Selectors
# ----------------------------------------------------------------------------
def select_positional_arguments(
    __namespace: Namespace,
    __signature: inspect.Signature,
    /,
) -> Tuple[Any, ...]:
    """Select positional arguments.

    Args:
        __namespace: Namespace.
        __signature: Signature.

    Returns:
        Positional Arguments.

    """
    results = get_positional_only_arguments(__namespace, __signature)
    return results


def select_keyword_arguments(
    __namespace: Namespace,
    __signature: inspect.Signature,
    /,
) -> Dict[str, Any]:
    """Select keyword arguments.

    Args:
        __namespace: Namespace.
        __signature: Signature.

    Returns:
        Keyword Arguments.

    """
    results: Dict[str, Any] = {
        **get_positional_or_keyword_arguments(__namespace, __signature),
        **get_keyword_only_arguments(__namespace, __signature),
    }
    return results


def get_positional_only_arguments(
    __namespace: Namespace,
    __signature: inspect.Signature,
    /,
) -> Tuple[Any, ...]:
    """Get positional-only arguments.

    Args:
        __namespace: Namespace.
        __signature: Signature.

    Returns:
        Positional-Only Arguments.

    """
    params: List[str] = [
        name
        for name, param in __signature.parameters.items()
        if param.kind.name == ParameterType.POSITIONAL_ONLY
    ]
    results = tuple(getattr(__namespace, param) for param in params)
    return results


def get_positional_or_keyword_arguments(
    __namespace: Namespace,
    __signature: inspect.Signature,
    /,
) -> Dict[str, Any]:
    """Get positional or keyword arguments.

    Args:
        __namespace: Namespace.
        __signature: Signature.

    Returns:
        Positional-or-Keyword Arguments.

    """
    params: List[str] = [
        name
        for name, param in __signature.parameters.items()
        if param.kind.name == ParameterType.POSITIONAL_OR_KEYWORD
    ]
    results = {param: getattr(__namespace, param) for param in params}
    return results


def get_keyword_only_arguments(
    __namespace: Namespace,
    __signature: inspect.Signature,
    /,
) -> Dict[str, Any]:
    """Get keyword-only arguments.

    Args:
        __namespace: Namespace.
        __signature: Signature.

    Returns:
        Keyword-Only Arguments.

    """
    params: List[str] = [
        name
        for name, param in __signature.parameters.items()
        if param.kind.name == ParameterType.KEYWORD_ONLY
    ]
    results = {param: getattr(__namespace, param, None) for param in params}
    return results


@enum.unique
class ParameterType(str, enum.Enum):
    """Implements parameter types."""

    KEYWORD_ONLY = "KEYWORD_ONLY"
    POSITIONAL_ONLY = "POSITIONAL_ONLY"
    POSITIONAL_OR_KEYWORD = "POSITIONAL_OR_KEYWORD"
