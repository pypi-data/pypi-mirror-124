#!/usr/bin/env python3
# vim: set filetype=python sts=4 ts=4 sw=4 expandtab tw=88 cc=+1:
# vim: set filetype=python tw=88 cc=+1:

# mypy: warn-unused-configs, disallow-any-generics, disallow-subclassing-any
# mypy: disallow-untyped-calls, disallow-untyped-defs, disallow-incomplete-defs
# mypy: check-untyped-defs, disallow-untyped-decorators, no-implicit-optional,
# mypy: warn-redundant-casts, warn-unused-ignores, warn-return-any,
# mypy: no-implicit-reexport, strict-equality,

"""
This module is boilerplate for a python CLI script.
"""

# python3 -m pylint --rcfile=/dev/null boilerplate.py
# python3 -m mypy boilerplate.py

import argparse
import contextlib
import inspect
import logging
import os.path
import pathlib
import sys
import typing

from ._version import __version__

LOGGER = logging.getLogger(__name__)

SCRIPT_DIRNAME = os.path.dirname(__file__)
SCRIPT_DIRNAMEABS = os.path.abspath(SCRIPT_DIRNAME)
SCRIPT_BASENAME = os.path.basename(__file__)

SCRIPT_PATH = pathlib.Path(__file__)

GenericT = typing.TypeVar("GenericT")


def coalesce(*args: typing.Optional[GenericT]) -> typing.Optional[GenericT]:
    for arg in args:
        if arg is not None:
            return arg
    return None


def vdict(*keys: str, obj: typing.Any = None) -> typing.Dict[str, typing.Any]:
    if obj is None:
        lvars = typing.cast(typing.Any, inspect.currentframe()).f_back.f_locals
        return {key: lvars[key] for key in keys}
    return {key: getattr(obj, key, None) for key in keys}


ArgsT = typing.List[str]
OptArgsT = typing.Optional[ArgsT]
OptParseResultT = typing.Optional[argparse.Namespace]
OptParserT = typing.Optional[argparse.ArgumentParser]


class Application:
    parser: argparse.ArgumentParser
    args: OptArgsT
    parse_result: OptParseResultT

    def __init__(self, parser: OptParserT = None):
        LOGGER.info("entry: mark-000")
        self.parse_result = None
        self.args = None
        self._do_init(parser)

    def _do_init(self, parser: OptParserT = None) -> None:
        LOGGER.debug("entry ...")
        if parser is None:
            own_parser = True
            self.parser = argparse.ArgumentParser(add_help=True)
        else:
            self.parser = parser
            own_parser = False
        parser = self.parser
        if own_parser:
            parser.add_argument(
                "-v",
                "--verbose",
                action="count",
                dest="verbosity",
                help="increase verbosity level",
            )
        parser.add_argument(
            "--version", "-V", action="version", version=("%(prog)s " + __version__)
        )
        parser.set_defaults(handler=self.handle)
        parsers: typing.List[argparse.ArgumentParser] = [parser]

        @contextlib.contextmanager
        def new_subparser(
            name: str,
            parser_args: typing.Dict[str, typing.Any] = {},  # noqa: B006
            subparsers_args: typing.Dict[str, typing.Any] = {},  # noqa: B006
        ) -> typing.Generator[argparse.ArgumentParser, None, None]:
            parent_parser = parsers[-1]
            if not hasattr(parent_parser, "_xsubparsers"):
                setattr(  # noqa: B010
                    parent_parser,
                    "_xsubparsers",
                    parent_parser.add_subparsers(
                        dest=f"subparser_{len(parsers)}", **subparsers_args
                    ),
                )
            parent_subparsers = getattr(parent_parser, "_xsubparsers")  # noqa: B009
            parsers.append(parent_subparsers.add_parser(name, **parser_args))
            try:
                yield parsers[-1]
            finally:
                parsers.pop()

        with new_subparser("s3") as subparser:
            parsers[-2]._xsubparsers.required = True  # type: ignore
            subparser.set_defaults(handler=self.handle_sub)
            with new_subparser("s3.1") as subparser:
                parsers[-2]._xsubparsers.required = True  # type: ignore
                with new_subparser("s3.1.1") as subparser:
                    subparser.add_argument("--what")
            with new_subparser("s3.2") as subparser:
                with new_subparser("s3.2.1") as subparser:
                    subparser.add_argument("--what")

    def _parse_args(self, args: OptArgsT = None) -> None:
        LOGGER.debug("entry ...")
        self.args = coalesce(args, self.args, sys.argv[1:])
        self.parse_result = self.parser.parse_args(self.args)

        verbosity = self.parse_result.verbosity
        if verbosity is not None:
            root_logger = logging.getLogger("")
            root_logger.propagate = True
            new_level = (
                root_logger.getEffectiveLevel()
                - (min(1, verbosity)) * 10
                - min(max(0, verbosity - 1), 9) * 1
            )
            root_logger.setLevel(new_level)

        LOGGER.debug(
            "args = %s, parse_result = %s, logging.level = %s, LOGGER.level = %s",
            self.args,
            self.parse_result,
            logging.getLogger("").getEffectiveLevel(),
            LOGGER.getEffectiveLevel(),
        )

        if "handler" in self.parse_result and self.parse_result.handler:
            self.parse_result.handler(self.parse_result)

    def do_invoke(self, args: OptArgsT = None) -> None:
        self._parse_args(args)

    # parser is so this can be nested as a subcommand ...
    @classmethod
    def invoke(cls, *, parser: OptParserT = None, args: OptArgsT = None) -> None:
        app = cls(parser)
        app.do_invoke(args)

    def handle(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.parse_result = parse_result = coalesce(parse_result, self.parse_result)

        LOGGER.info("stuff to do goes here ...")

    def handle_sub(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.handle(parse_result)
        parse_result = self.parse_result


def main() -> None:
    logging.basicConfig(
        level=os.environ.get("PYLOGGING_LEVEL", logging.INFO),
        stream=sys.stderr,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format=(
            "%(asctime)s %(process)d %(thread)d %(levelno)03d:%(levelname)-8s "
            "%(name)-12s %(module)s:%(lineno)s:%(funcName)s %(message)s"
        ),
    )

    Application.invoke()


if __name__ == "__main__":
    main()
