FROM python:2.7-onbuild

EXPOSE 5000

CMD ["python", "./manage.py", "server", "-h", "0.0.0.0", "-p", "5000"]
