import os
from pathlib import Path

from system_stats_log import get_stats, write_log


if __name__ == "__main__":
    filepath = Path(
        os.getenv("SYS_STATS_LOG_FILEPATH", "C:\\tmp\\sys-stats-log.tsv"),
    )
    system_stats = get_stats()
    write_log(system_stats, filepath)
