import importlib
import importlib.abc
import importlib.util
import os
import sys
from typing import cast

import click

from jetpack import cli as c
from jetpack._job.job import Job
from jetpack.config import symbols
from jetpack.config.symbols import Symbol

_using_new_cli = False


def is_using_new_cli() -> bool:
    """
    for legacy uses, we keep old cli. This function disables that logic to ensure
    we don't run the cli command twice.
    """
    return _using_new_cli


@click.group()
def cli() -> None:
    global _using_new_cli
    _using_new_cli = True


@click.command()
@click.option("--entrypoint", required=True)
@click.option("--exec-id", required=True)
@click.option("--job-name", required=True)
@click.option("--encoded-args", default="")
def job(entrypoint: str, exec_id: str, job_name: str, encoded_args: str) -> None:
    # We could use importlib.import_module but we want to guarantee entrypoint
    # is loaded with the correct module name. (e.g. main.py should be module main)
    # See jetpack.utils.qualified_name for how we generage job names
    # In particular, app/main.py should be module "main" and not "app.main"

    # We ensure the entrypoint path is in path so that imports work as expected.
    sys.path.append(os.path.dirname(entrypoint))
    module_name = os.path.basename(entrypoint).split(".")[0]
    spec = importlib.util.spec_from_file_location(module_name, entrypoint)
    assert spec is not None
    entrypoint_module = importlib.util.module_from_spec(spec)
    cast(importlib.abc.Loader, spec.loader).exec_module(entrypoint_module)

    func = symbols.get_symbol_table()[Symbol(job_name)]
    Job(func).exec(exec_id, encoded_args)


cli.add_command(job)
