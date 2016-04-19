- MC LiveFeed API & Admin Panel
Contains REST APIs for the MC LiveFeed Analytics Panel and Django admin for the backend support.

- Requirements
Python 3.4.3

- Setup
Install requirements (pip install -r requirements.txt)
Migrate Database (python manage.py migrate)

- IMPORTANT
Add Concerns by running "python manage.py add_concerns"


- WebSocket
To start a web socket for live dashboard use ""nohup nice python manage.py shell < apps/websocket.py &""
A ping will be sent on new addition of feedback
To stop the background process "ps aux | grep shell" and kill the process by ID
To setup your websockets with nginx refer to the link: https://www.nginx.com/blog/websocket-nginx/

- Email
Start redis server "redis-server” or make sure the reds is running already by “redis-cli ping"
Start celery worker “celery -A lively worker -l info"
To start the worker for emails "ps aux | grep celery" and kill the process by ID