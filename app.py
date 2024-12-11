from flask import Flask, request, jsonify
import sqlite3
import numpy as np
from scipy.stats import linregress
import statistics

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('currency_exchange.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.route('/currencies', methods=['GET'])
def currencies():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM currency_data')
    rows = cur.fetchall()
    conn.close()

    # Convert row objects to dictionary
    currencies = [dict(row) for row in rows]
    return jsonify(currencies)
#Fetching Latest Rates: This endpoint retrieves the most recent 
# rates by finding entries with the latest timestamp in the database.

@app.route('/rates/latest', methods=['GET'])
def get_latest_rates():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM currency_data
        WHERE last_updated = (SELECT MAX(last_updated) FROM currency_data)
    ''')
    rates = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rates]), 200

#Historical Data: This endpoint fetches historical rates based on optional 
# parameters for the bank name and currency code. If not specified, it returns all records.
@app.route('/rates/historical', methods=['GET'])
def get_historical_rates():
    bank_name = request.args.get('bank', default='%')  # Default '%' is for SQL LIKE wildcard
    code = request.args.get('code', default='%')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM currency_data
        WHERE bank_name LIKE ? AND code LIKE ?
        ORDER BY last_updated DESC
    ''', (bank_name, code))
    rates = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rates]), 200

#Comparisons: This endpoint allows users to compare rates from 
# two specific dates for a given currency code.

@app.route('/rates/compare', methods=['GET'])
def compare_rates():
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    code = request.args.get('code')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bank_name, name, code, buying, selling, last_updated
        FROM currency_data
        WHERE code = ? AND last_updated IN (?, ?)
    ''', (code, date1, date2))
    rates = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rates]), 200

@app.route('/stats', methods=['GET'])
def get_statistics():
    code = request.args.get('code', default='USD', type=str)
    conn = sqlite3.connect('currency_exchange.db')
    cursor = conn.cursor()
    query = f"SELECT buying FROM currency_data WHERE code = ?"
    cursor.execute(query, (code,))
    rates = cursor.fetchall()
    rates = [float(rate[0]) for rate in rates if rate[0]]

    if not rates:
        return jsonify({'error': 'No data available for the specified currency code.'}), 404

    mean_rate = np.mean(rates)
    median_rate = statistics.median(rates)
    std_dev = np.std(rates)

    # Calculate trend using linear regression
    slope, _, _, _, _ = linregress(range(len(rates)), rates)
    trend = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"

    return jsonify({
        'currency_code': code,
        'mean': mean_rate,
        'median': median_rate,
        'standard_deviation': std_dev,
        'trend': trend
    })

if __name__ == '__main__':
    app.run(debug=True)

