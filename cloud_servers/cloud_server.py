#!/usr/bin/env python3
"""
Simple Cloud Server simulator that holds user states in memory.
Run two instances (VM1 and VM2) on different ports to simulate federated clouds.

Endpoints:
 - POST /users/signup   -> store user {username,password,data}
 - POST /users/login    -> returns user state if present
 - POST /users/import   -> import/replace user state (used for migration)
 - POST /users/delete   -> delete user
 - GET  /users/list     -> list users (for demo)
"""

from flask import Flask, request, jsonify
import argparse

app = Flask(__name__)
store = {}  # username -> {password, data}

@app.route('/users/signup', methods=['POST'])
def signup():
    payload = request.get_json() or {}
    user = payload.get('username')
    pwd = payload.get('password')
    data = payload.get('data', {})
    if not user or not pwd:
        return jsonify({'error': 'username and password required'}), 400
    if user in store:
        return jsonify({'error': 'user exists'}), 409
    store[user] = {'password': pwd, 'data': data}
    return jsonify({'status': 'ok', 'vm': app.config.get('VM_NAME', 'VM')}), 201

@app.route('/users/login', methods=['POST'])
def login():
    payload = request.get_json() or {}
    user = payload.get('username')
    pwd = payload.get('password')
    if not user or not pwd:
        return jsonify({'error': 'username and password required'}), 400
    if user not in store:
        return jsonify({'error': 'not found'}), 404
    if store[user]['password'] != pwd:
        return jsonify({'error': 'invalid credentials'}), 403
    return jsonify({
        'status': 'ok',
        'user': user,
        'data': store[user]['data'],
        'vm': app.config.get('VM_NAME', 'VM')
    })

@app.route('/users/import', methods=['POST'])
def import_user():
    payload = request.get_json() or {}
    user = payload.get('username')
    state = payload.get('state')
    if not user or state is None:
        return jsonify({'error': 'username and state required'}), 400
    store[user] = state
    return jsonify({'status': 'imported', 'vm': app.config.get('VM_NAME', 'VM')}), 200

@app.route('/users/delete', methods=['POST'])
def delete_user():
    payload = request.get_json() or {}
    user = payload.get('username')
    if not user:
        return jsonify({'error': 'username required'}), 400
    if user in store:
        del store[user]
        return jsonify({'status': 'deleted', 'vm': app.config.get('VM_NAME', 'VM')}), 200
    return jsonify({'error': 'not found'}), 404

@app.route('/users/list', methods=['GET'])
def list_users():
    return jsonify({'vm': app.config.get('VM_NAME', 'VM'), 'users': list(store.keys())})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001, help='port to run server on')
    parser.add_argument('--name', type=str, default='VM', help='VM name shown in responses')
    args = parser.parse_args()
    app.config['VM_NAME'] = args.name
    print(f"Starting cloud server {args.name} on port {args.port}")
    app.run(host='0.0.0.0', port=args.port, debug=False)
