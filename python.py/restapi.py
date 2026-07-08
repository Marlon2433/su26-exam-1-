import flask
from flask import jsonify
from flask import request

from sql import DBConnection
from sql import execute_query
from sql import execute_read_query

import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # show errors in the browser


def get_connection():
    """Open a fresh database connection using the shared credentials."""
    mycreds = creds.creds()
    return DBConnection(
        mycreds.connectionstring,
        mycreds.username,
        mycreds.password,
        mycreds.database
    )


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cryptocurrency API</h1>"


# ---------- CREATE ----------
# POST /api/cryptocurrency
# JSON body: { "cryptoname": "Bitcoin", "cryptocode": "BTC",
#              "coinprice": 62000, "totalcoins": 100 }
@app.route('/api/cryptocurrency', methods=['POST'])
def add_cryptocurrency():
    userinput = request.get_json()

    cryptoname = userinput['cryptoname']
    cryptocode = userinput['cryptocode']
    coinprice = userinput['coinprice']
    totalcoins = userinput['totalcoins']

    con = get_connection()
    sql = """insert into cryptocurrency (cryptoname, cryptocode, coinprice, totalcoins)
             values (%s, %s, %s, %s)"""
    execute_query(con, sql, (cryptoname, cryptocode, coinprice, totalcoins))

    return "A new cryptocurrency was added to the database"


# ---------- DELETE ----------
# DELETE /api/cryptocurrency
# JSON body: { "cryptocode": "BTC" }
@app.route('/api/cryptocurrency', methods=['DELETE'])
def delete_cryptocurrency():
    userinput = request.get_json()
    cryptocode = userinput['cryptocode']

    con = get_connection()
    sql = "delete from cryptocurrency where cryptocode = %s"
    execute_query(con, sql, (cryptocode,))

    return "Cryptocurrency with code %s was deleted from the database" % cryptocode


# ---------- READ / CALCULATE TOTAL AMOUNT SPENT ----------
# GET /api/cryptocurrency?cryptocode=BTC
# Returns totalamt = coinprice * totalcoins, or 0.00 if the code is not found.
@app.route('/api/cryptocurrency', methods=['GET'])
def total_amount_spent():
    if 'cryptocode' in request.args:
        cryptocode = request.args['cryptocode']
    else:
        return jsonify({"error": "No cryptocode provided"})

    con = get_connection()
    sql = "select coinprice, totalcoins from cryptocurrency where cryptocode = %s"
    rows = execute_read_query(con, sql, (cryptocode,))

    if not rows:
        totalamt = 0.00
    else:
        record = rows[0]
        totalamt = float(record['coinprice']) * float(record['totalcoins'])

    return jsonify({"cryptocode": cryptocode, "totalamt": round(totalamt, 2)})


app.run()

