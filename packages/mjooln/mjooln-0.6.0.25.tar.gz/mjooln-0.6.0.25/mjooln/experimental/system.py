from multiprocessing import cpu_count

from mjooln import *


class System:

    @classmethod
    def cores(cls, fraction=None):
        """
        Get number of cores in system

        :param fraction: Fraction of cores to return. If None, total number
            of cores are returned. If, for example, fraction=0.5, half the number of cores
            are returned. Minimum return is 1
        :return: Number of cores available, or a fraction of them
        """
        num_cores = cpu_count()
        if fraction is not None:
            num_cores = round(num_cores*fraction)
            if num_cores < 1:
                num_cores = 1
        return num_cores

    @classmethod
    def current(cls):
        return {
            'memory': cls.memory(),
            'disk': cls.disk_usage(Folder.current()),
        }

    @classmethod
    def memory(cls):
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'percent': mem.percent,
            'used': mem.used,
            'free': mem.free,
        }

    @classmethod
    def disk_usage(cls, folder):
        usage = shutil.disk_usage(str(folder))
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': 100 * usage.used / usage.total,
        }