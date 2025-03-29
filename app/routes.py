from flask import Blueprint, render_template, request, flash, jsonify
from . import socketio
from flask_socketio import disconnect
import json

bp = Blueprint('main', __name__)
dropdown_list = ['NIFTY', 'BANKNIFTY', 'TCS', 'INFY', 'RELIANCE', 'ICICIBANK', 'SBIN']

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', dropdown_list=dropdown_list)

@bp.route('/send-signal', methods=['POST'])
def send_signal():
    data = request.json
    action = data.get('action')
    field1 = data.get('field1')
    field2 = data.get('field2')
    dropdown_value = data.get('dropdown_value')

    payload = {
        'field1': field1,
        'field2': field2,
        'dropdown': dropdown_value,
        'action': action
    }

    try:
        socketio.emit('signal', payload)
        flash(f'Signal Sent: {action}', 'success')
        return jsonify({"status": "success", "message": f"Signal sent: {action}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to send signal: {str(e)}"})

# Load tokens from JSON
with open('allowed_tokens.json', 'r') as f:
    data = json.load(f)

# Extract all values
allowed_tokens = list(data.values())

@socketio.on('connect')
def handle_connect(auth):
    token = auth.get('token') if auth else None
    print(f"Allowed Tokens {allowed_tokens}")
    if token not in allowed_tokens:
        print(f"Unauthorized Connection Attempt: {token}")
        disconnect()
    else:
        print(f"User connected with token: {token}")