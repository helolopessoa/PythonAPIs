# from flask import Flask, request, jsonify
# import time
# # from flask_restful import Api,Resource
# from Model_cpp import Model
# from fuzzylogic import *

# app = Flask(__name__)
# # api = Api(app)
# llm = Model(model_path="models/Model-pro-8b-instruct.Q6_K.gguf", n_ctx=4096)

# # class FuzzyAPI(Resource):

# #  [0] AngerXFear [Range(-1f, 1f)]
# #  [1] DisgustXTrust [Range(-1f, 1f)]
# #  [2] SadnessXJoy [Range(-1f, 1f)]
# #  [3] AntecipationXSurprise [Range(-1f, 1f)]
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
#     # return request.json();
# # /<float:axeAF>/<float:axeDT>/<float:axeSJ>/<float:axeAS>

# # class ModelAPI(Resource):

# ###########################
# @app.route('/Modelapi', methods=['POST'])
# def generate():
#     data = request.get_json()
#     prompt = data.get("prompt", "")
#     max_tokens = data.get("max_tokens", 30)
    
#     output = llm(prompt, max_tokens=max_tokens)
#     return jsonify(output)
# ##############################


# # @app.route('/Modelapi', methods=['POST'])
# # def generate():
# #     start_time = time.time()
    
# #     data = request.get_json(silent=True) or {}
    
# #     prompt = data.get("prompt")
# #     if not prompt or not isinstance(prompt, str):
# #         return jsonify({"error": "Field 'prompt' is required and must be a string."}), 400

# #     # Clamp max_tokens
# #     try:
# #         max_tokens = int(data.get("max_tokens", 80))
# #     except (TypeError, ValueError):
# #         max_tokens = 80
# #     max_tokens = max(1, min(max_tokens, 512))  # don’t let it go insane

# #     # Optional sampling params with safe ranges
# #     try:
# #         temperature = float(data.get("temperature", 0.7))
# #     except (TypeError, ValueError):
# #         temperature = 0.7
# #     temperature = max(0.0, min(temperature, 1.5))

# #     try:
# #         top_p = float(data.get("top_p", 0.9))
# #     except (TypeError, ValueError):
# #         top_p = 0.9
# #     top_p = max(0.0, min(top_p, 1.0))

# #     # Now call the model with explicit parameters (if your llm wrapper supports them)
# #     try:
# #         raw_output = llm(
# #             prompt,
# #             max_tokens=max_tokens,
# #             temperature=temperature,
# #             top_p=top_p,
# #         )
# #     except Exception as e:
# #         # Log server-side, but send a clean error to the client
# #         app.logger.exception("Error calling Model model")
# #         return jsonify({"error": "Model generation failed.", "details": str(e)}), 500

# #     elapsed = time.time() - start_time

# #     # Normalize response structure: extract just the text + metadata
# #     # text = extract_text_from_llm(raw_output)

# #     return jsonify({
# #         "text": text,
# #         "elapsed_seconds": elapsed,
# #         "max_tokens": max_tokens,
# #         "temperature": temperature,
# #         "top_p": top_p,
# #     })




    

# # api.add_resource(FuzzyAPI, "/fuzzyemotionapi")
# # /<float:axeAF>/<float:axeDT>/<float:axeSJ>/<float:axeAS>

# # api.add_resource(ModelAPI, "/Modelapi")


# # /<float:axeAF>/<float:axeDT>/<float:axeSJ>/<float:axeAS>



# if __name__ == "__main__":
#     app.run(port=11434)
