from pynubank import Nubank
import pandas as pd
import json
import flask
import os

nu = Nubank()
app = flask.Flask(__name__)
#app.config["DEBUG"] = True
#Variaveis de ambiente
NUUSER = os.environ.get('NUUSER')
NUPASS = os.environ.get('NUPASS')
NUCERT = os.environ.get('NUCERT')

#Autenticar com certificado
nu.authenticate_with_cert(NUUSER, NUPASS, NUCERT)

def get_bill():
    # Recupera as compras feitas no cartão
    transactions = nu.get_bills()

    # Filtra pela fatura aberta (atual)
    filter_bill = [i for i in transactions if (i.get('state') == 'open')]

    currentBillDetails = nu.get_bill_details(filter_bill[0])

    transactions = currentBillDetails.get('bill').get("line_items")
    transactions_json = json.dumps(transactions)
    
    df = pd.read_json(transactions_json)
    
    return df.to_csv()

def get_balance():
    # Saldo da nuconta
    return "balance,"+str(nu.get_account_balance()).replace(".","")

@app.route('/card', methods=['GET'])
def get_card():
    return get_bill()

@app.route('/account/balance', methods=['GET'])
def get_account_balance():
    return get_balance()
