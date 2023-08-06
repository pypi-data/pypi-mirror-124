import concurrent.futures as cfut
from functools import lru_cache

from mjooln.experimental.store import *
from mjooln.experimental.system import System


class AppError(MjoolnException):
    pass


class App(Doc):
    _store = ConfigStore

    @classmethod
    @lru_cache()
    def _key(cls):
        return Key.elf(cls.__name__)

    @classmethod
    def from_doc(cls, doc: dict):
        doc['atom'] = Atom.from_seed(doc['atom'])
        doc['runfile'] = File.glass(doc['runfile'])
        return super().from_doc(doc)

    @classmethod
    def load(cls):
        if not cls._store.exists(cls._key()):
            raise AppError(f'Missing store file: {cls._store.file(cls._key())}')
        doc = cls._store.get(cls._key())
        return cls.from_doc(doc)

    def __init__(self,
                 atom=None,
                 max_workers=None,
                 num_tasks=10,
                 min_wait_s=0.2,
                 pause_s=2.0,
                 continuous=True,
                 runfile=True,
                 **kwargs):
        if not max_workers:
            max_workers = System.cores(fraction=0.5)

        if atom is None:
            atom = Atom(self._key())
        self.atom = Atom.glass(atom)
        self.max_workers = max_workers
        self.num_tasks = num_tasks
        self.min_wait_s = min_wait_s
        self.pause_s = pause_s
        if runfile:
            if isinstance(runfile, bool):
                runfile = HOME.append('app').file(self.atom.seed())
            else:
                runfile = File.glass(runfile)
        self.runfile = runfile
        self.continuous = continuous
        self._executor = None
        self._futures = []
        self._multithreading = self.max_workers is not None and self.max_workers > 0
        if self._multithreading:
            self._executor = cfut.ThreadPoolExecutor(max_workers=self.max_workers)

        self._continue = False
        self._logger = logging.getLogger(self._key().seed())
        super().__init__(**kwargs)

    def to_doc(self):
        doc = super().to_doc()
        doc['runfile'] = str(doc['runfile'])
        return doc

    def save(self, crypt_key=None, password=None):
        doc = self.to_doc()
        self._store.put(self._key(), doc, crypt_key=crypt_key, password=password)

    def tasks(self):
        raise AppError('tasks() must be overridden in child class')

    def execute(self, task):
        raise AppError('execute() must be overridden in child class')

    def execute_bulk(self):
        tic = Tic()
        tasks = self.tasks()
        self._continue = self.continuous or len(tasks) == self.num_tasks
        for task in tasks:
            if self._multithreading:
                self._futures.append(self._executor.submit(self.execute, task))
            else:
                self.execute(task)

        if self._multithreading:
            while len(self._futures) > 0:
                done, self._futures = cfut.wait(self._futures, timeout=1)
                elapsed_time_s = tic.elapsed_time()
                if len(self._futures) > 0:
                    self._logger.debug(f'Elapsed time: {elapsed_time_s}, '
                                       f'Remaining tasks: {len(self._futures)}')
                    time.sleep(self.min_wait_s)
                else:
                    avg = elapsed_time_s / len(tasks)
                    self._logger.info(f'Average processing time: {avg:.3f} seconds')
                    self._futures = []
        else:
            elapsed_time_s = tic.elapsed_time()
            self._logger.debug(f'Completed {len(tasks)} tasks '
                               f'in {elapsed_time_s:.3f} seconds')
        if self.pause_s > 0:
            tic.tac(self.pause_s)

    def run(self):
        self._logger.debug('Start app')
        self._continue = True
        if self.runfile and isinstance(self.runfile, File):
            self.runfile.touch()
        while self._continue and self.runfile and self.runfile.exists():
            self.execute_bulk()
        if self.runfile and isinstance(self.runfile, File):
            self.runfile.untouch()
        self._logger.debug('Stop app')


class TestApp(App):
    count = 0

    def tasks(self):
        ts = [x + self.count for x in range(self.num_tasks)]
        self.count += self.num_tasks
        return ts

    def execute(self, task):
        print(f'Execute task: {task}')
        time.sleep(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    ta = TestApp()
    ta.save()
    tr = TestApp.load()
    tr.run()


# LAdele24


