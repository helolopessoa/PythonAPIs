from flask import Flask, request, jsonify
import time
from llamalogic import *
from modelogic import *
from fuzzylogic import *

app = Flask(__name__)


#  [0] AngerXFear [Range(-1f, 1f)]
#  [1] DisgustXTrust [Range(-1f, 1f)]
#  [2] SadnessXJoy [Range(-1f, 1f)]
#  [3] AntecipationXSurprise [Range(-1f, 1f)]


# @app.route('/fuzzyapi', methods=['GET'])
# def get():
#     emo = getEmotion()
#     return {"emotion" : emo}

# @app.route('/fuzzyapi', methods=['POST'])
# def post():
#     emo = []
#     emo.append(request.form['axeAF'])
#     emo.append(request.form['axeDT'])
#     emo.append(request.form['axeSJ'])
#     emo.append(request.form['axeAS'])
#     for i in range(4):
#         emo[i] = emo[i].replace(",",".")
#         emo[i] = float(emo[i])
#     postEmotion(emo)
#     return '', 204 


@app.route('/modelapi/fuzzyapi', methods=['POST'])
def fuzzy():
    emo = []
    emo.append(request.form['axeAF'])
    emo.append(request.form['axeDT'])
    emo.append(request.form['axeSJ'])
    emo.append(request.form['axeAS'])
    for i in range(4):
        emo[i] = emo[i].replace(",",".")
        emo[i] = float(emo[i])
    emo = postEmotion(emo)
    return {"emotion" : emo}
# /<float:axeAF>/<float:axeDT>/<float:axeSJ>/<float:axeAS>


# ###########################
@app.route('/modelapi/answer', methods=['POST'])
def generateAnswer():
    data = request.get_json()
    # print(data)
    prompt = data.get("prompt", "")
    # Optional: allow overriding max_tokens from Unity later
    # max_tokens = data.get("max_tokens", 150)
    # output = llamaAnswer(prompt)
    output = generateOutputAnswer(prompt, "You are a non-playable character in a game. You respond only as the NPC, never as the game engine, narrator or the player. REMAIN IN CHARACTER as a non-playable character (NPC) in a game, ANSWERING ACCORDINGLY TO THE PLAYER.")
    # output = mockgenerateOutputAnswer()
    return jsonify(output)
# ##############################

###########################
@app.route('/modelapi/classification', methods=['POST'])
def generateClassification():
    data = request.get_json()
    
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' field"}), 400
    
    prompt = data["prompt"]

    try:
        result = generateOutput(prompt, "You are a strict dialogue intent classifier.")
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
##############################


@app.route("/modelapi/ping", methods=["GET"])
def ping():
    print("[FLASK] /ping called")
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(port=11434,
            debug=True,
            threaded=False,
            use_reloader=False)

    
