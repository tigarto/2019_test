## Referencias ##
1. https://www.bogotobogo.com/python/Multithread/python_multithreading_subclassing_Timer_Object.php
2. https://docs.python.org/2.4/lib/timer-objects.html
3. https://docs.python.org/3/library/sched.html
4. https://docs.python.org/2/library/sched.html
5. https://www.geeksforgeeks.org/timer-objects-python/


import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def f():
    logging.debug('thread function running')
    return

if __name__ == '__main__':
    t1 = threading.Timer(5, f)
    t1.setName('t1')
    t2 = threading.Timer(5, f)
    t2.setName('t2')

    logging.debug('starting timers...')
    t1.start()
    t2.start()

    logging.debug('waiting before canceling %s', t2.getName())
    time.sleep(2)
    logging.debug('canceling %s', t2.getName())
    print 'before cancel t2.is_alive() = ', t2.is_alive()
    t2.cancel()
    time.sleep(2)
    print 'after cancel t2.is_alive() = ', t2.is_alive()

    t1.join()
    t2.join()

    logging.debug('done')
