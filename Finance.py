from flask import Flask, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)
tickers = ['FB', 'TSLA', 'JPM', 'PG', 'V']

DATABASE = 'finance_database.db'


@app.route('/stock_data_by_date/<string:date>', methods=['GET'])
def get_stock_data_by_date(date):
    conn = sqlite3.connect('financial_data.db')
    query = f"""SELECT * FROM FB WHERE Date = '{date}'
UNION ALL
SELECT * FROM TSLA WHERE Date = '{date}'
UNION ALL
SELECT * FROM JPM WHERE Date = '{date}'
UNION ALL
SELECT * FROM PG WHERE Date = '{date}'
UNION ALL
SELECT * FROM V WHERE Date = '{date}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    data = df.to_dict(orient='records')
    return jsonify(data)


@app.route('/stock_data_by_company_date/<company>/<string:date>', methods=['GET'])
def stock_data_by_company_date(company, date):
    conn = sqlite3.connect('finance_database.db')
    query = f"""SELECT * FROM '{company}' WHERE Date = '{date}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    data = df.to_dict(orient='records')
    return jsonify(data)


@app.route('/stock_data_by_company_all_dates/<company>/', methods=['GET'])
def stock_data_by_company_all_dates(company):
    conn = sqlite3.connect('financial_data.db')
    query = f"""SELECT * FROM '{company}'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    return jsonify(data)


@app.route('/update_aapl/<company>', methods=['POST'])
def update_aapl(company):
    print('company = ', company)
    data = request.get_json()
    date = data['Date']
    new_high = data['High']
    print("date = ", date, "new_high = ", new_high)

    conn = sqlite3.connect('financial_data.db')
    print('connection established')
    query = f"UPDATE '{company}' SET High = {new_high} WHERE Date = '{date}'"
    conn.execute(query)
    print('executed')
    conn.commit()
    print('commited ')
    conn.close()

    return jsonify({'message': 'AAPL Open updated successfully'})


if __name__ == '__main__':
    app.run(debug=True)
