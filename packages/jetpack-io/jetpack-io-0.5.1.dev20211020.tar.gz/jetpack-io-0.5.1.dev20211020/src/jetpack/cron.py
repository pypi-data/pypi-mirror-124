import os
from typing import Any, Callable

import cronitor
import schedule
from schedule import every  # Use this to whitelist what we allow

from jetpack import utils
from jetpack.config import symbols

cronjob_suffix = os.environ.get("JETPACK_CRONJOB_SUFFIX", "-missing-suffix")


def repeat(repeat_pattern: schedule.Job) -> Callable[..., Any]:
    def wrapper(func: Callable[..., Any]) -> Any:
        name = symbols.get_symbol_table().register(func)
        name_with_suffix = name + cronjob_suffix
        cronitor_wrapped_func = cronitor.job(name_with_suffix)(func)
        return schedule.repeat(repeat_pattern)(cronitor_wrapped_func)

    return wrapper
