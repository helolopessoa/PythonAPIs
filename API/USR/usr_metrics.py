import numpy as np
from sentence_transformers import SentenceTransformer, util


class USRScorer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Inicializa o modelo SBERT
        """
        self.model = SentenceTransformer(model_name)

    def coherence(self, context, response):
        """
        Calcula similaridade semântica entre contexto e resposta
        """
        emb_context = self.model.encode(context, convert_to_tensor=True)
        emb_response = self.model.encode(response, convert_to_tensor=True)

        score = util.cos_sim(emb_context, emb_response)
        return score.item()

    def score_dialogue(self, turns):
        """
        Recebe lista de (context, response) e retorna métricas do diálogo
        """
        scores = []

        for context, response in turns:
            s = self.coherence(context, response)
            scores.append(s)

        if not scores:
            return None

        return {
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "min": float(np.min(scores)),
            "max": float(np.max(scores)),
            "n_turns": len(scores)
        }

    def score_dataset(self, dataset):
        """
        Recebe dataset do data_loader e calcula scores para todos os diálogos
        """
        results = []

        for dialogue in dataset:
            result = self.score_dialogue(dialogue["turns"])

            if result:
                result["file"] = dialogue["file"]
                results.append(result)

        return results


def summarize_results(results):
    """
    Agrega resultados de múltiplos diálogos
    """
    means = [r["mean"] for r in results]

    return {
        "overall_mean": float(np.mean(means)),
        "overall_std": float(np.std(means)),
        "n_dialogues": len(results)
    }


# from sentence_transformers import SentenceTransformer, util
# from usr_data_treatment import load_dataset

# data = load_dataset("../DataUSR/Baseline")

# print("Número de diálogos:", len(data))

# # pega um exemplo
# example = data[0]

# print("\nArquivo:", example["file"])

# # carregar modelo
# model = SentenceTransformer('all-MiniLM-L6-v2')

# for context, response in example["turns"][:2]:
#     # print("\n--- CONTEXT ---")
#     # print(context)
#     # print("\n>>> RESPONSE ---")
#     # print(response)
#     emb_context = model.encode(context, convert_to_tensor=True)
#     emb_response = model.encode(response, convert_to_tensor=True)
#     score = util.cos_sim(emb_context, emb_response)
#     print(score.item())




# # exemplo
# # context = "I love cooking Italian food."
# # response = "Pasta is my favorite dish."

# # gerar embeddings
# # emb_context = model.encode(context, convert_to_tensor=True)
# # emb_response = model.encode(response, convert_to_tensor=True)

# # # similaridade
# # score = util.cos_sim(emb_context, emb_response)

# # print(score)