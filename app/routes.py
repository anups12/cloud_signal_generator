from flask import Blueprint, render_template, request, flash, jsonify
from . import socketio
from flask_socketio import disconnect
import json

bp = Blueprint('main', __name__)
dropdown_list =  ['Solana (OTC)', 'FTSE China A50 Index', 'GBP/CAD (OTC)', 'USD/PHP (OTC)', 'Dogwifhat (OTC)', 'Intel (OTC)', 'GBP/JPY (OTC)', 'USD/INR (OTC)', 'Floki (OTC)', 'Pepe (OTC)', 'Microsoft (OTC)', 'NZD/CHF (OTC)', 'Gold (OTC)', 'USD/MXN (OTC)', 'EUR/JPY (OTC)', 'CAD/CHF (OTC)', 'S&P/ASX 200', 'GBP/CHF (OTC)', 'NZD/USD (OTC)', 'Litecoin (OTC)', 'USD/ZAR (OTC)', 'Dow Jones', 'GBP/AUD (OTC)', 'NZD/JPY (OTC)', 'USD/NGN (OTC)', 'FTSE 100', 'CAC 40', 'USD/IDR (OTC)', 'Bitcoin Cash (OTC)', 'Bitcoin (OTC)', 'USD/TRY (OTC)', 'USD/ARS (OTC)', 'AUD/USD (OTC)', 'USD/JPY (OTC)', 'AUD/CAD (OTC)', 'American Express (OTC)', 'GBP/NZD (OTC)', 'Silver (OTC)', 'Hong Kong 50', 'Binance Coin (OTC)', 'EUR/NZD (OTC)', 'Shiba Inu (OTC)', 'Bonk (OTC)', 'USD/BDT (OTC)', 'EUR/CHF (OTC)', 'GBP/USD (OTC)', 'IBEX 35', 'Ethereum (OTC)', 'TRON (OTC)', 'AUD/NZD (OTC)', 'EUR/AUD (OTC)', 'Boeing Company (OTC)', 'USD/CHF (OTC)', 'EUR/SGD (OTC)', 'USD/BRL (OTC)', 'Johnson & Johnson (OTC)', 'USD/EGP (OTC)', 'AUD/JPY (OTC)', 'CHF/JPY (OTC)', 'EUR/CAD (OTC)', 'EURO STOXX 50', 'Pfizer Inc (OTC)', 'Toncoin (OTC)', 'Dogecoin (OTC)', 'USD/PKR (OTC)', 'AUD/CHF (OTC)', 'USD/COP (OTC)', 'NASDAQ 100', 'USD/DZD (OTC)', 'Trump (OTC)', 'EUR/USD (OTC)', 'UKBrent (OTC)', 'USD/CAD (OTC)', 'Ripple (OTC)', "McDonald's (OTC)", 'FACEBOOK INC (OTC)', 'CAD/JPY (OTC)', 'Nikkei 225', 'USCrude (OTC)', 'EUR/GBP (OTC)', 'NZD/CAD (OTC)']

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