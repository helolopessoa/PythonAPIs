# # import fed

# # # Load model
# # model, tokenizer = fed.load_models("microsoft/DialoGPT-large")

# # # Evaluate

# # import os

# # from pathlib import Path
# # import fed

# # model, tokenizer = fed.load_models("microsoft/DialoGPT-large")

# # folder_path = Path("Baseline/")

# # b_results = []

# # for file_path in folder_path.glob("*.txt"):
# #     with open(file_path, "r", encoding="utf-8") as f:
# #         conversation = f.read()
    
# #     scores = fed.evaluate(conversation, model, tokenizer)
    
# #     b_results.append({
# #         "file": file_path.name,
# #         "scores": scores
# #     })

# # print("Baseline", b_results)



# # folder_path = Path("Scaffolded/")

# # s_results = []

# # for file_path in folder_path.glob("*.txt"):
# #     with open(file_path, "r", encoding="utf-8") as f:
# #         conversation = f.read()
    
# #     scores = fed.evaluate(conversation, model, tokenizer)
    
# #     s_results.append({
# #         "file": file_path.name,
# #         "scores": scores
# #     })

# # print("Baseline", s_results)

# from pathlib import Path
# import sys
# import os

# sys.path.append(os.path.abspath("fed/fed"))
# from fed import evaluate, load_models
# import csv
# import statistics

# # Load FED model
# # model, tokenizer = load_models("microsoftLocal/DialoGPT-large")
# model, tokenizer = load_models("microsoftSmallLocal/DialoGPT-small")

# def evaluate_folder(folder_name):
#     # folder_path = Path(folder_name)
#     # results = []

#     # for file_path in folder_path.glob("*.txt"):
#     folder_path = Path(folder_name)
#     results = []

#     print("\n📂 Base:", folder_path)
#     print("Existe?", folder_path.exists())

#     files = list(folder_path.glob("**/ConversationResume/*.txt"))
#     print(f"Arquivos encontrados: {len(files)}")

#     for file_path in files:  
#         print(f"Arquivo: {file_path}")  
#         with open(file_path, "r", encoding="utf-8") as f:
#             conversation = f.read()
        
#         scores = evaluate(conversation, model, tokenizer)
#         print(scores)
#         print(type(scores))
#         # results.append({
#         #     "file": file_path.name,
#         #     "condition": folder_name,
#         #     "coherence": scores["coherence"],
#         #     "fluency": scores["fluency"],
#         #     "engagingness": scores["engagingness"],
#         #     "overall": sum(scores.values()) / len(scores)
#         # })

#     return results


# # Evaluate both folders
# # b_results = evaluate_folder("DATA_CLEAN_NPC/Baseline")
# # s_results = evaluate_folder("DATA_CLEAN_NPC/Scaffolded")
# b_results = evaluate_folder("LLMAsPlayer/Baseline")
# s_results = evaluate_folder("LLMAsPlayer/Scaffold")


# all_results = b_results + s_results


# # 🔥 Save everything to CSV
# with open("fed_results.csv", "w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=all_results[0].keys())
#     writer.writeheader()
#     writer.writerows(all_results)


# # 📊 Print summary statistics
# def summarize(results, label):
#     overall_scores = [r["overall"] for r in results]
#     print(f"\n{label} Summary:")
#     print("Mean:", round(statistics.mean(overall_scores), 4))
#     print("Std Dev:", round(statistics.stdev(overall_scores), 4))


# summarize(b_results, "Baseline")
# summarize(s_results, "Scaffolded")

from pathlib import Path
import sys
import os
import csv
import statistics

sys.path.append(os.path.abspath("fed/fed"))
from fed import evaluate, load_models

# Load FED model
model, tokenizer = load_models("microsoftSmallLocal/DialoGPT-small")


# 🔹 Função para dividir texto em chunks
# def split_into_chunks(text, tokenizer, max_tokens=900):
#     # tokens = tokenizer.encode(text)
#     tokens = tokenizer.encode(text, add_special_tokens=False)
    
#     chunks = []
#     for i in range(0, len(tokens), max_tokens):
#         chunk_tokens = tokens[i:i+max_tokens]
#         chunk_text = tokenizer.decode(chunk_tokens)
#         chunks.append(chunk_text)
    
#     return chunks
def split_into_chunks(text, tokenizer, max_tokens=900, overlap=100):
    tokens = tokenizer.encode(text, add_special_tokens=False)
    
    chunks = []
    step = max_tokens - overlap
    
    for i in range(0, len(tokens), step):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks

def evaluate_folder(folder_name):
    folder_path = Path(folder_name)
    results = []

    print("\n Base:", folder_path)
    print("Existe?", folder_path.exists())

    files = list(folder_path.glob("**/TaggedConversationResume/*.txt"))
    print(f"Arquivos encontrados: {len(files)}")

    for file_path in files:
        print(f"\n📄 Arquivo: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            conversation = f.read()

        # Divide em chunks
            chunks = split_into_chunks(conversation, tokenizer)

            chunk_scores_list = []

            for i, chunk in enumerate(chunks):
                try:
                    print(f"\n--- CHUNK {i} ---")
                    print(chunk[:200])  # só o começo do texto
                    scores = evaluate(chunk, model, tokenizer)
                    if scores:
                        chunk_scores_list.append(scores)
                    print("\n RAW SCORES:")
                    print(scores)
                    print("Keys:", scores.keys())
                    print("Type:", type(scores))
                except Exception as e:
                    print(f"Erro no chunk {i}: {e}")

            # Se nenhum chunk funcionou, pula
            if not chunk_scores_list:
                print("Nenhum score válido")
                continue
            # Média dos scores
            all_keys = set().union(*chunk_scores_list)
            print("Chunk scores:", chunk_scores_list[:1])
            avg_scores = {}
            for key in all_keys:
                values = [d[key] for d in chunk_scores_list if key in d]
                avg_scores[key] = sum(values) / len(values)

            # Definição das métricas
            high_keys = [
                'coherent', 'consistent', 'correct', 'relevant',
                'error recovery', 'depth', 'diverse', 'understand'
            ]

            low_keys = [
                'engaging', 'interesting', 'likeable',
                'flexible', 'inquisitive'
            ]

            # Seleção correta
            high_scale = [avg_scores[k] for k in high_keys if k in avg_scores]
            low_scale = [avg_scores[k] for k in low_keys if k in avg_scores]

            result_entry = {
                "file": file_path.name,
                "condition": folder_name,
            }

            result_entry.update(avg_scores)

            # Agora sim correto
            result_entry["overall_high"] = statistics.mean(high_scale) if high_scale else None
            result_entry["overall_low"] = statistics.mean(low_scale) if low_scale else None

            results.append(result_entry)
    return results


# Evaluate both folders
b_results = evaluate_folder("LLMAsPlayer/Baseline")
print("b_results:", type(b_results))

s_results = evaluate_folder("LLMAsPlayer/Scaffold")
print("s_results:", type(s_results))

all_results = b_results + s_results


# Save everything to CSV
if all_results:
    #  coleta todas as keys possíveis
    all_keys = set().union(*(r.keys() for r in all_results))

    with open("fed_results.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=sorted(all_keys))
        writer.writeheader()
        writer.writerows(all_results)
#     with open("fed_results.csv", "w", newline="", encoding="utf-8") as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=all_results[0].keys())
#         writer.writeheader()
#         writer.writerows(all_results)
else:
    print(" Nenhum resultado para salvar")


#  Print summary statistics
def summarize(results, label):
    if not results:
        print(f"\n{label}: sem dados")
        return

    # overall_scores = [r["overall"] for r in results if r["overall"] is not None]
    overall_scores = [
        r.get("overall_high") 
        for r in results 
        if isinstance(r.get("overall_high"), (int, float))
    ]

    print(f"\n{label} Summary:")
    print("Mean:", round(statistics.mean(overall_scores), 4))

    if len(overall_scores) > 1:
        print("Std Dev:", round(statistics.stdev(overall_scores), 4))


summarize(b_results, "Baseline")
summarize(s_results, "Scaffolded")