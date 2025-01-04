import concurrent
import os
import queue
import weakref
from concurrent.futures.process import (_ExecutorManagerThread as _EMT, ProcessPoolExecutor as PPE,
                                        _CallItem, _ExceptionWithTraceback, _sendback_result)

from loguru import logger

_threads_wakeups = weakref.WeakKeyDictionary()


class _ExecutorManagerThread(_EMT):

    def __init__(self, executor):
        super().__init__(executor)
        self.wlock = executor.wlock

    def add_call_item_to_queue(self):
        while True:
            if self.call_queue.full():
                return
            try:
                work_id = self.work_ids_queue.get(block=False)
            except queue.Empty:
                return
            else:
                work_item = self.pending_work_items[work_id]

                if work_item.future.set_running_or_notify_cancel():
                    #################################################
                    with self.wlock:
                        # print(f'{self.wlock=}\n', end='')
                        logger.debug(f'{self.wlock=}')
                        #################################################
                        self.call_queue.put(_CallItem(work_id,
                                                      work_item.fn,
                                                      work_item.args,
                                                      work_item.kwargs),
                                            block=True)
                else:
                    del self.pending_work_items[work_id]
                    continue


class ProcessPoolExecutor(PPE):
    def __init__(self, max_workers=None, mp_context=None,
                 initializer=None, initargs=(), *, max_tasks_per_child=None):
        super().__init__(max_workers, mp_context,
                         initializer, initargs, max_tasks_per_child=max_tasks_per_child)

        self.rlock = mp_context.Lock()
        self.wlock = mp_context.Lock()

    def _start_executor_manager_thread(self):
        if self._executor_manager_thread is None:
            # Start the processes so that their sentinels are known.
            if not self._safe_to_dynamically_spawn_children:  # ie, using fork.
                self._launch_processes()
            self._executor_manager_thread = _ExecutorManagerThread(self)
            self._executor_manager_thread.start()
            _threads_wakeups[self._executor_manager_thread] = \
                self._executor_manager_thread_wakeup

    def _spawn_process(self):
        p = self._mp_context.Process(
            target=_process_worker,
            args=(
                self.rlock,
                self._call_queue,
                self._result_queue,
                self._initializer,
                self._initargs,
                self._max_tasks_per_child))
        p.start()
        self._processes[p.pid] = p


def _process_worker(
        rlock, call_queue, result_queue, initializer, initargs, max_tasks=None
):
    if initializer is not None:
        try:
            initializer(*initargs)
        except BaseException:
            concurrent.futures._base.LOGGER.critical('Exception in initializer:', exc_info=True)
            return
    num_tasks = 0
    exit_pid = None
    while True:
        ###########################################
        with rlock:
            # print(f'{rlock=}\n', end='')
            logger.debug(f'{rlock=}')
            #######################################
            call_item = call_queue.get(block=True)
        if call_item is None:
            result_queue.put(os.getpid())
            return

        if max_tasks is not None:
            num_tasks += 1
            if num_tasks >= max_tasks:
                exit_pid = os.getpid()

        try:
            r = call_item.fn(*call_item.args, **call_item.kwargs)
        except BaseException as e:
            exc = _ExceptionWithTraceback(e, e.__traceback__)
            _sendback_result(result_queue, call_item.work_id, exception=exc,
                             exit_pid=exit_pid)
        else:
            _sendback_result(result_queue, call_item.work_id, result=r,
                             exit_pid=exit_pid)
            del r

        del call_item

        if exit_pid is not None:
            return


logger.configure(
    handlers=[
        dict(
            sink='./processpool.log',

            format="<level><green>{time:YYYY-MM-DD HH:mm:ss.SS}</green>|{level:<5}"
                   "|{process.name:<14}|{thread.name:<13}|{function:>22}:{line:<3}|"
                   "<cyan>{message:<}</cyan></level>",
            level="DEBUG",
            enqueue=True,

        )
    ]
)
