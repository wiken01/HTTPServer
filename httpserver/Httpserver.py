#Httpserver.py
'''
name:wiken
time:2018-10-1
module
'''
from socket import *
import sys
import re
from threading import Thread
from setting import *
import time

class HTTPServer(object):

    # default port of http is 80
    def __init__(self,addr= ('0.0.0.0',80)):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr = addr
        self.bind(addr)     

    def bind(self,addr):      
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)        

    # start http server
    def server_forever(self):
        self.sockfd.listen(10)
        print("Listen the port %d..."%self.port)
        while True:
            print("waiting for connecting...")
            connfd,addr = self.sockfd.accept()
            print("connect from ",addr)
            handle_client = Thread(target = self.handle_request,args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()          

    def handle_request(self,connfd):
        # receive request from browser
        request = connfd.recv(4096)

        print(request,'request')
        request_lines = request.splitlines()
        # get request line
        print(request_lines,'lines')
        request_line = request_lines[0].decode()  
              

        # 正则表达式提取请求方法和请求内容　
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            print("except")
            respone_handlers = "HTTP/1.1 500 ServerError\r\n"
            respone_handlers += '\r\n'
            response_body= "Server Error"
            response = response_handlers + response_body
            connfd.send(response.encode())
            return
        print(env,"env")

        # send request to frame and get result data from return
        status,response_body = \
            self.send_request(env['METHOD'],env["PATH"])
        # 根据响应码组织　响应内容　
        response_handlers = self.get_handlers(status)
        #将结果　组织为http　response 发送给客户端
        response= response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()

    # interaction with frame for request and response
    def send_request(self,method,path):
        s = socket()
        s.connect(frame_addr)

        # send method and path to frame
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status = s.recv(128).decode()
        response_body = s.recv(4096).decode()

        return status,response_body


    def get_handlers(self,status):
        if status == '200':
            response_headlers = "HTTP/1.1 200 OK\r\n"
            response_headlers += '\r\n'
        elif status == '400':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'

        return response_headlers


        


if __name__ == "__main__":    
    httpd = HTTPServer(ADDR)
    httpd.server_forever()