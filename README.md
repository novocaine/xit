# Install

Install redis. On windows, you can install it from https://github.com/MSOpenTech/redis/releases

Then to install the python deps, in a virtualenv do 

```pip install -r requirements.txt```

# Run

Start redis (on windows you can run C:\Program Files\Redis\redis-server.exe)

Start the webserver

``` python web.py```

Start the celery - for me this looks like 

```venv/Scripts/celery -A tasks worker --loglevel=info ```

