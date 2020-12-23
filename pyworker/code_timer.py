import time


class CodeTimerError(Exception):
    pass
    """Custom exception """
    
class CodeTimer:
    def __init__(self):
        self._start_time = None
    
    def start(self):
        if self._start_time is not None:
            raise CodeTimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        if self._start_time is None:
            raise CodeTimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return elapsed_time
        #print(f"Elapsed time: {elapsed_time:0.4f} seconds")
