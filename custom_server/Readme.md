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
