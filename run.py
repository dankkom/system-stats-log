import os
from pathlib import Path

from system_stats_log import get_stats, write_log


if __name__ == "__main__":
    SYS_STATS_LOG_FILEPATH = os.getenv(
        "SYS_STATS_LOG_FILEPATH",
        "sys-stats-log.tsv",
    )
    filepath = Path(SYS_STATS_LOG_FILEPATH)
    system_stats = get_stats()
    print(system_stats)
    write_log(system_stats, filepath)
