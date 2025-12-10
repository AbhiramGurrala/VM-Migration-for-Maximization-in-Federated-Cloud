from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .forms import SignupForm, LoginForm

# endpoints for our two simulated cloud servers
VM_ENDPOINTS = {
    "VM1": "http://127.0.0.1:5001",
    "VM2": "http://127.0.0.1:5002"
}

def index(request):
    return render(request, "migration_app/index.html", {"vms": list(VM_ENDPOINTS.keys())})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            resp = requests.post(
                f"{VM_ENDPOINTS[data['vm']]}/users/signup",
                json={"username": data['username'], "password": data['password'], "data": {"preferences": data.get("preferences")}}
            )
            if resp.status_code == 201:
                messages.success(request, f"User {data['username']} created on {data['vm']}")
                return redirect('index')
            messages.error(request, f"Signup failed: {resp.json().get('error')}")
    else:
        form = SignupForm()
    return render(request, "migration_app/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            resp = requests.post(
                f"{VM_ENDPOINTS[d['vm']]}/users/login",
                json={"username": d['username'], "password": d['password']}
            )
            if resp.status_code == 200:
                # store session info for migration step
                request.session['username'] = d['username']
                request.session['source_vm'] = d['vm']
                messages.success(request, f"Logged in from {d['vm']}")
                return redirect('migrate')
            messages.error(request, f"Login failed: {resp.json().get('error')}")
    else:
        form = LoginForm()
    return render(request, "migration_app/login.html", {"form": form})

def migrate(request):
    username = request.session.get('username')
    source = request.session.get('source_vm')
    if not username or not source:
        messages.error(request, "Please login first")
        return redirect('login')

    if request.method == 'POST':
        dest = request.POST.get('dest')
        password = request.POST.get('password')  # for demo we ask password again
        # fetch state from source vm
        r = requests.post(f"{VM_ENDPOINTS[source]}/users/login", json={"username": username, "password": password})
        if r.status_code != 200:
            messages.error(request, "Failed to fetch state from source VM")
            return redirect('index')
        state = {
            "password": password,
            "data": r.json().get('data', {})
        }
        # import to destination
        r2 = requests.post(f"{VM_ENDPOINTS[dest]}/users/import", json={"username": username, "state": state})
        if r2.status_code == 200:
            # delete from source
            requests.post(f"{VM_ENDPOINTS[source]}/users/delete", json={"username": username})
            messages.success(request, f"Migrated {username} from {source} to {dest}")
            # update session
            request.session['source_vm'] = dest
            return redirect('index')
        messages.error(request, "Migration to destination failed")
    return render(request, "migration_app/migrate.html", {"username": username, "source": source, "vms": list(VM_ENDPOINTS.keys())})
