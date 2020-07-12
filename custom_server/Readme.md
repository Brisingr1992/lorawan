### How to compile and run
1. Compile and run using `./server.py` or `make all`. This will start the server with the details of
   hostname and port used.
2. Sample of details `Server started on HOST-(128.226.114.201), Port-(8080)`

### Implementation
1. Implemented by creating a master socket using local hostname / IP and default port of 8080.
   Server run by calling socket fd unix command and then binds the port to the IP, listens for 
   any new connections and accepts them using accept() blocking socket command.
2. After accepting the connection, accept returns a new socket fd which is then used by a newly created    thread to recieve the request messafe and send a proper http response as per the assignment   guidelines.
3. After sending the response server closes the socket and exits the thread.

### Sample Input / Output
`wget -S [title](http://128.226.114.201:8080/asf-logo.gif)`
```--2019-09-24 19:51:19--  http://128.226.114.201:8080/asf-logo.gif
Connecting to 128.226.114.201:8080... connected.
HTTP request sent, awaiting response...
  HTTP/1.1 200 OKContent-Type: image/gif; encoding=utf8
  Content-Length: 7279
  Connection: close
  Date: Tue, 24 Sep 2019 23:51:19 GMT
  Server: ssaxena3Server
  Last-Modified: Thu, 19 Sep 2019 23:43:34 GMT
Length: 7279 (7.1K)
Saving to: 'asf-logo.gif.13'

asf-logo.gif.13           100%[==================================>]   7.11K  --.-KB/s    in 0s

2019-09-24 19:51:19 (771 MB/s) - 'asf-logo.gif.13' saved [7279/7279]
```