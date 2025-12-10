echo off
start cmd /k python cloud_servers\cloud_server.py --port 5001 --name VM1
start cmd /k python cloud_servers\cloud_server.py --port 5002 --name VM2
cd django_app
start cmd /k python manage.py runserver
