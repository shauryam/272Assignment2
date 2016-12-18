import socket
import select
#import time
import sys
from time import sleep
import redis
from cb import CircuitBreaker

rdbb = redis.Redis(host='localhost')


# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001
forward_to = ('localhost', 5000)
_failure_count = 0
threshold = 3
class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        while True:
		try:
		    
		    self.forward.connect((host, int(port)))
		    return self.forward
		except Exception, e:
		  
		    print "Unable to reach server, Call Circuit Breaker!"
                    run()
		    server.main_loop()


class TheServer(object):
    input_list = [1]
    channel = {}
    def __init__(self, host, port):
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((host, port))
            self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:	   
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
		print self.s
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self): 
	_failure_count = 0
	if _failure_count < threshold:	
		host , port = get_server()
		forward = Forward().start(host, port)
		clientsock, clientaddr = self.server.accept()		
		if forward:
			
			self.input_list.append(clientsock)
			self.input_list.append(forward)
			self.channel[clientsock] = forward
			self.channel[forward] = clientsock
		else:
			print "Can't establish connection with remote server.",
			print "Closing connection with client side", clientaddr
			clientsock.close()
			#exception+=1
			_failure_count += 1 
	else: 
		#err = 'CircuitBreaker is OPEN %d failures' % _failure_count
            	
            	raise Exception(err)
                

		

    def on_close(self):
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        self.channel[self.s].send(data)

def get_server():

	rdbb.rpoplpush("connlist","connlist")
	try:	
		server1=rdbb.lindex("connlist",0)
		if server1:
			print "connecting to server: %s " %server1
			host, port=server1.split(":")
		else:
			print "No more server in db!!"
			sys.exit(1)
	except Exception, e:
		print "e"
	return host, port


@CircuitBreaker(max_failure_to_open=2, reset_timeout=10)
def dependency_call(call_num):
    '''if call_num in (1, 2, 5, 6, 7, 17, 19):
        #raise Exception(MY_EXCEPTION)
	#print "no manual excption created"
    else:
        return 'SUCCESS'
	'''
	#return 'SUCCESS'
        
    #return host, port

def run():
    num_success = 0
    num_failure = 0
    num_circuitbreaker_passthrough_failure = 0
    for i in range(1,4):
        try:
            print "Call-%d:" % i
            print "Result=%s" %dependency_call(i)
            num_success += 1
        except Exception as ex:
            num_failure += 1
            if ex.message == MY_EXCEPTION:
                num_circuitbreaker_passthrough_failure += 1
            print ex.message

        sleep(0.5)
    return num_success, num_failure, num_circuitbreaker_passthrough_failure

if __name__ == '__main__':
        server = TheServer('127.0.0.1', 8080)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
sys.exit(1)
