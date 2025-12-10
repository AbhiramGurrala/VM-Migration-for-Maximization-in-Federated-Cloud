# VM Migration — Federated Cloud (Demo)

## Quick start
1. Create a Python virtualenv and install:
   `pip install -r requirements.txt`
2. Start two cloud servers (two terminals):
   - `python cloud_servers/cloud_server.py --port 5001 --name VM1`
   - `python cloud_servers/cloud_server.py --port 5002 --name VM2`
3. Start Django app:
   - `cd django_app`
   - `python manage.py runserver`
4. Open http://127.0.0.1:8000

## Flow
- Sign up on VM1 or VM2
- Login from that VM
- Use "Migrate" to move user state to the other VM

> This is a demo: in production you'd add encryption, authentication tokens, transactional state transfer and logging.
What it shows: how VM state can be moved between cloud providers to reduce cost or balance load.

Architecture: two lightweight cloud servers (Flask) + central orchestration (Django).

Real improvements for production: use HTTPS, authentication tokens, chunked state transfer, state checksums, and an orchestration layer (Kubernetes/Redis/etcd).
