import time
from decorator import decorator

SLEEP_PENALTY = .0001 # penalty in second for sleeping / context switching, etc.
UPDATE_EVERY_N_SECONDS = 2

class safe(object):
    """
    a decorator for keeping a function from
    raising an exception to its caller
    """
    def __init__(self, function_description):
        self.function_description = function_description

    def __call__(self, f):
        def wrapped_f(func, *args, **kwargs):
            try:
                print args
                print kwargs
                func(*args, **kwargs)
            except Exception as e:
                print 'ERROR [%s]: %s' % (self.function_description, e)
        return decorator(wrapped_f, f)

class loop_at_target_frequency(object):
    """
    a decorator for executing a function in a loop at
    a specified frequency

    params:
        service     the thing that needs to be running
                    for this loop to be executing. The loop
                    will continue to execute until <service>.running
                    is False-ish

        target_frequency    the target frequency at which the
                            function should be executed
    """
    def __init__(self, service, target_frequency):
        self.service = service
        self.target_frequency = target_frequency

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            last = 0
            last_updated_time = 0
            while self.service.running:

                # special case for if the frequency is 0
                if self.target_frequency() == 0:
                    time.sleep(UPDATE_EVERY_N_SECONDS)
                    continue

                now = time.time()
                if now - last_updated_time > UPDATE_EVERY_N_SECONDS:
                    last_updated_time = now
                    target_period = 1. / self.target_frequency()

                now = time.time()
                since_last = now - last
                if since_last > target_period:
                    last = now
                    f()
                else:
                    sleep_for = target_period - since_last - SLEEP_PENALTY
                    if sleep_for > 0:
                        time.sleep(sleep_for)
        return decorator(wrapped_f, f)

