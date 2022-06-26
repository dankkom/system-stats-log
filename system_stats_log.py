__version__ = "0.1.0"


import csv
import platform
import time
from pathlib import Path
from typing import Any

import psutil
from pythonping import ping

OS = platform.system()

if OS == "Windows":
    import wmi


CSV_HEADER = (
    "timestamp",
    "ram_usage_pct",
    "cpu_temp",
    "cpu_usage_pct",
    "cpu_freq",
    "net_bytes_sent",
    "net_bytes_recv",
    "net_latency",
)


def get_cpu_temp():
    cpu_temp = None
    if OS == "Windows":
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        cpu_temp = w.Sensor()[-1].Value
    else:
        cpu_temp = psutil.sensors_temperatures()["cpu_thermal"][0].current
    return cpu_temp


def get_stats():
    timestamp = time.time()
    ram_usage_pct = psutil.virtual_memory().percent
    cpu_usage_pct = psutil.cpu_percent(interval=1.0)
    cpu_freq = psutil.cpu_freq().current
    cpu_temp = get_cpu_temp()
    net_stats = psutil.net_io_counters()
    net_bytes_sent = net_stats.bytes_sent
    net_bytes_recv = net_stats.bytes_recv
    response_list = ping("8.8.8.8", size=40, count=3)
    net_latency = response_list.rtt_avg_ms
    return {
        "timestamp": timestamp,
        "ram_usage_pct": ram_usage_pct,
        "cpu_temp": cpu_temp,
        "cpu_usage_pct": cpu_usage_pct,
        "cpu_freq": cpu_freq,
        "net_bytes_sent": net_bytes_sent,
        "net_bytes_recv": net_bytes_recv,
        "net_latency": net_latency,
    }


def write_log(system_stats: dict[str, Any], filepath: Path) -> None:
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True)
    file_not_exists = not filepath.exists()
    with filepath.open("a", encoding="utf-8", newline="\n") as f:
        writer = csv.DictWriter(f, delimiter="\t", fieldnames=CSV_HEADER)
        if file_not_exists:
            writer.writeheader()
        writer.writerow(system_stats)
