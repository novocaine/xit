# Install

Install redis. On windows, you can install it from https://github.com/MSOpenTech/redis/releases

Then to install the python deps, in a virtualenv do 

```pip install -r requirements.txt```

# Run

Start redis (on windows you can run C:\Program Files\Redis\redis-server.exe - I found it 
didn't work properly unless I ran it as administrator, ymmv)

Start the webserver

``` python web.py```

Start the celery - for me this looks like 

```venv/Scripts/celery -A tasks worker --loglevel=info ```

# Tests

The tests use environment variables, you need to run something like this:

WEB_URL=http://localhost:5000 XPLAN_USERNAME=a XPLAN_PASSWORD=a XPLAN_URL=http://localhost:1983/autotestuk/ /cygdrive/c/python27/scripts/nosetests
