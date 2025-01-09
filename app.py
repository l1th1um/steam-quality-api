from flask import Flask, request, jsonify
from pyXSteam.XSteam import XSteam
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)

app = Flask(__name__)

@app.route('/dryness', methods=['POST'])
def dryness():
    result = drynessCalculation(float(request.form['pSh']),
                                float(request.form['ncg']),
                                float(request.form['pBaro']),
                                float(request.form['tCal']))

    return jsonify({'result' : result})


def drynessCalculation(pSh, ncg, pBaro, tCal):
    pshNCG = pSh * 1 - (ncg/ 100)

    numerator = steamTable.hV_p(pshNCG) - steamTable.hV_p(pBaro) - ( steamTable.CpV_p(pBaro) *  (tCal - steamTable.tsat_p(pBaro)) )
    denominator = steamTable.hV_p(pshNCG) - steamTable.hL_p(pshNCG)

    return (numerator / denominator) * 100

@app.route('/superheat', methods=['POST'])
def superheat():
    result = superheatCalculation(float(request.form['Tsh']),
                                float(request.form['TCorr']),
                                float(request.form['pSh']),
                                float(request.form['ncg']))

    return jsonify({'result' : result})


def superheatCalculation(Tsh, TCorr, pSh, ncg):
    pshNCG = pSh * 1 - (ncg/ 100)

    return (Tsh + TCorr) - steamTable.tsat_p(pshNCG)

if __name__ == '__main__':
    app.run(host='0.0.0.0')