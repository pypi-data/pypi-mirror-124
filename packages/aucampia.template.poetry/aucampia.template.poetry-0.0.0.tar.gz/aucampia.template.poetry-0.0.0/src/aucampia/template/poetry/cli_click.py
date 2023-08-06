#!/usr/bin/env python3
# vim: set filetype=python sts=4 ts=4 sw=4 expandtab tw=88 cc=+1:
# vim: set filetype=python tw=88 cc=+1:

# mypy: allow-untyped-decorators

import inspect
import logging
import os
import sys
import typing

import click

LOGGER = logging.getLogger(__name__)

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


"""
https://click.palletsprojects.com/en/7.x/api/#parameters
https://click.palletsprojects.com/en/7.x/options/
https://click.palletsprojects.com/en/7.x/arguments/
"""


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-v",
    "--verbose",
    "verbosity",
    # type=None,
    # required=False,
    # default=None,
    # callback=None,
    # nargs=None,
    # metavar=None,
    # expose_value=True,
    # is_eager=False,
    # envvar=None,
    # autocompletion=None,
    # show_default=False,
    # prompt=False,
    # confirmation_prompt=False,
    # hide_input=False,
    # is_flag=None,
    # flag_value=None,
    # multiple=False,
    count=True,
    # allow_from_autoenv=True,
    help="Increase verbosity",
    # hidden=False,
    # show_choices=True,
    # show_envvar=False,
)
@click.version_option(version="0.0.0")
@click.pass_context
def cli(ctx: click.Context, verbosity: int) -> None:
    ctx.ensure_object(dict)

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
        "entry: ctx.parent.params = %s, ctx.params = %s",
        ({} if ctx.parent is None else ctx.parent.params),
        ctx.params,
    )
    LOGGER.debug(
        "logging.level = %s, LOGGER.level = %s",
        logging.getLogger("").getEffectiveLevel(),
        LOGGER.getEffectiveLevel(),
    )


@cli.group(name="sub")
@click.pass_context
def cli_sub(ctx: click.Context) -> None:
    LOGGER.debug(
        "entry: ctx.parent.params = %s, ctx.params = %s",
        ({} if ctx.parent is None else ctx.parent.params),
        ctx.params,
    )


@cli_sub.command(name="leaf")
@click.option(
    "--name",
    type=str,
    # required=False,
    default="fake",
    # callback=None,
    # nargs=None,
    # metavar=None,
    # expose_value=True,
    # is_eager=False,
    # envvar=None,
    # autocompletion=None,
    # show_default=False,
    # prompt=False,
    # confirmation_prompt=False,
    # hide_input=False,
    # is_flag=None,
    # flag_value=None,
    # multiple=False,
    # count=False,
    # allow_from_autoenv=True,
    help="The name ...",
    # hidden=False,
    # show_choices=True,
    # show_envvar=False,
)
@click.argument(
    "numbers",
    type=int,
    # required=False,
    # default=None,
    # callback=None,
    nargs=-1,
    # metavar=None,
    # expose_value=True,
    # is_eager=False,
    # envvar=None,
)
@click.pass_context
def cli_sub_leaf(
    ctx: click.Context,
    name: typing.Optional[str],
    numbers: typing.Optional[typing.Sequence[int]],
) -> None:
    LOGGER.debug(
        "entry: ctx.parent.params = %s, ctx.params = %s",
        ({} if ctx.parent is None else ctx.parent.params),
        ctx.params,
    )


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

    cli(obj={})


if __name__ == "__main__":
    main()
