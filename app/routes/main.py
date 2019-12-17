from app import app, mongo, request, analysis
import pandas as pd

@app.route('/', methods=["GET"])
def getContracts():
    contracts = {}
    for contract in mongo.db.cfts.find().distinct('CONTRACTNUMBER'):
        contracts[contract] = contract
    return contracts

@app.route('/worknumbers', methods=['GET'])
def worknumbers():
    contract = request.args.get('contract')

    cfts = list(mongo.db.cfts.find({"CONTRACTNUMBER": contract}))
    ledger = list(mongo.db.ledger.find({"CONTRACT_NBR": contract}))
    b370 = list(mongo.db.b370.find({"CONTRACT_NBR": contract}))

    df_cfts = pd.DataFrame(cfts)
    df_ledger = pd.DataFrame(ledger)
    df_b370 = pd.DataFrame(b370)

    if df_b370.empty or df_ledger.empty:
        return "0"

    result = analysis(df_cfts, df_b370, df_ledger)
    
    return result

@app.route('/uploads', methods=['POST'])
def uploads(): 

    data = request.get_json()
    
    if data['cfts']:
        mongo.db.cfts.insert_many(data['cfts'])

    if data['ledger']:
        mongo.db.ledger.insert_many(data['ledger'])

    if data['b370']:
        mongo.db.b370.insert_many(data['b370']) 

    return "OK"

