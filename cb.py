from functools import wraps
from datetime import datetime, timedelta
import requests, time
import redis
from time import sleep

rdbb = redis.Redis(host='localhost')

class CircuitBreaker(object):
    def __init__(self, name=None, expected_exception=Exception, max_failure_to_open=2, reset_timeout=10):
        self._name = name
        self._expected_exception = expected_exception
        self._max_failure_to_open = max_failure_to_open
        self._reset_timeout = reset_timeout
        # Set the initial state
        self.close()
 
    def close(self):
        self._is_closed = True
        self._failure_count = 0
        
    def open(self):
        self._is_closed = False
        self._opened_since = datetime.utcnow()
        
    def can_execute(self):
        if not self._is_closed:
            self._open_until = self._opened_since + timedelta(seconds=self._reset_timeout)
            self._open_remaining = (self._open_until - datetime.utcnow()).total_seconds()
            return self._open_remaining <= 0
        else:
            return True

    def __call__(self, func):
        if self._name is None:
            self._name = func.__name__

        @wraps(func)
        def with_circuitbreaker(*args, **kwargs):
            return self.call(func, *args, **kwargs)

        return with_circuitbreaker

    def call(self, func, *args, **kwargs):
        probserv = rdbb.lindex("connlist",0)
	print "cb called"
        if not self.can_execute():	  
	    print "cb is in open state"
            print "removing %s server"%rdbb.lindex("connlist",0)  
	    rdbb.lrem("connlist",probserv, 0) 
            nexser = rdbb.lindex("connlist",0) 
	    print "Connecting to next server: %s" %nexser
	 
            err = 'CircuitBreaker[%s] is OPEN until %s (%d failures, %d sec remaining)' % (
                self._name,
                self._open_until,
                self._failure_count,
                round(self._open_remaining)
            )
            #raise Exception(err)
	          
        try:     
            bad_server= "http://"+bad_server+"/v1/expenses"
            print "retrying to connecting on %s" %prbserver
	    result = requests.get(bad_server)  	
  
          
        except Exception, e:
	    self._failure_count += 1
            if self._failure_count >= self._max_failure_to_open:
                self.open()
            raise
        self.close()
        return result

