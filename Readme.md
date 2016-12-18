Readme

1. Run proxy.py, so the server will be running on http://localhost:8080 
2. Run all the server files (Server1.py, Server2.py, Server3.py) , the servers will register themselves in redis when they are run
4. Make a get call from postman on this http://localhost:8080/v1/expenses
5. This will send the request to the first server registered on redis which depends on the order on which you have run the servers
6. Second request will go to the second server registered on redis and so on..
