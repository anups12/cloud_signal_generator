from flask import Blueprint, render_template, request, flash, jsonify
from . import socketio
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
