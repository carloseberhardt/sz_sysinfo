import psutil
import platform
from datetime import datetime
from typing import List
from pydantic import BaseModel


class CoreUsage(BaseModel):
    core: int
    usage: float


class CpuInfo(BaseModel):
    physicalCores: int
    totalCores: int
    maxFrequency: float
    minFrequency: float
    currentFrequency: float
    usage: float
    coreUsage: List[CoreUsage]


class MemInfo(BaseModel):
    total: str
    available: str
    used: str
    percentage: float


class SwapInfo(BaseModel):
    total: str
    free: str
    used: str
    percentage: float


class DiskInfo(BaseModel):
    total: str
    used: str
    free: str
    percentage: float


class SystemInfo(BaseModel):
    system: str
    node: str
    release: str
    version: str
    machine: str
    processor: str
    bootTime: datetime
    cpuInfo: CpuInfo
    memInfo: MemInfo
    swapInfo: SwapInfo
    diskInfo: DiskInfo


def scale_bytes(bytes, suffix="B"):
    """
    scale a value in bytes to KB, MB, GB, TB, PB
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_sysinfo():
    """
    get system info and return a SystemInfo object
    """
    uname = platform.uname()
    bootTime = datetime.fromtimestamp(psutil.boot_time())
    cpuInfo = CpuInfo(
        physicalCores=psutil.cpu_count(logical=False),
        totalCores=psutil.cpu_count(logical=True),
        maxFrequency=psutil.cpu_freq().max,
        minFrequency=psutil.cpu_freq().min,
        currentFrequency=psutil.cpu_freq().current,
        usage=psutil.cpu_percent(),
        coreUsage=[CoreUsage(core=i, usage=usage)
                   for i, usage in enumerate(psutil.cpu_percent(percpu=True))],
    )
    memInfo = MemInfo(
        total=scale_bytes(psutil.virtual_memory().total),
        available=scale_bytes(psutil.virtual_memory().available),
        used=scale_bytes(psutil.virtual_memory().used),
        percentage=psutil.virtual_memory().percent,
    )
    swapInfo = SwapInfo(
        total=scale_bytes(psutil.swap_memory().total),
        free=scale_bytes(psutil.swap_memory().free),
        used=scale_bytes(psutil.swap_memory().used),
        percentage=psutil.swap_memory().percent,
    )
    diskInfo = DiskInfo(
        total=scale_bytes(psutil.disk_usage("/").total),
        used=scale_bytes(psutil.disk_usage("/").used),
        free=scale_bytes(psutil.disk_usage("/").free),
        percentage=psutil.disk_usage("/").percent,
    )
    sysInfo = SystemInfo(
        system=uname.system,
        node=uname.node,
        release=uname.release,
        version=uname.version,
        machine=uname.machine,
        processor=uname.processor,
        bootTime=bootTime,
        cpuInfo=cpuInfo,
        memInfo=memInfo,
        swapInfo=swapInfo,
        diskInfo=diskInfo,
    )
    return sysInfo


# if run from console, print the system info
if __name__ == "__main__":
    print(get_sysinfo().json())
