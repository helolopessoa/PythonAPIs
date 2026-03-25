import os
import pandas as pd

assertive_terms = [
    "must", "will", "cannot", "stand firm",
    "at all costs", "we must", "we cannot",
    "fight", "survival", "protect"
    ]

concession_terms = [
    "perhaps", "compromise", "cooperation",
    "shared", "dialogue", "understand",
    "empathy", "together", "peace"
]

emotion_terms = ["angry", "frustrated", "offended",
                    "unfair", "disrespect", "outrage", "!", "disappointed","hostile", "aggressive",
                "betrayal", "threat", "aggression",
                "dominate", "undermine", "erase",
                "destroy"
                ]


# ==========================
# 2. FUNÇÃO PARA CALCULAR MÉTRICAS
# ==========================

def compute_metrics(text):
    text_lower = text.lower()
    words = len(text_lower.split())
    
    if words == 0:
        return 0, 0, 0
    
    assertive_count = sum(text_lower.count(term) for term in assertive_terms)
    concession_count = sum(text_lower.count(term) for term in concession_terms)
    emotion_count = sum(text_lower.count(term) for term in emotion_terms)
    
    return (
        assertive_count / words,
        concession_count / words,
        emotion_count / words
    )


# ==========================
# 3. FUNÇÃO PARA LER PASTA
# ==========================

def process_folder(folder_path, condition_label):
    results = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            assertiveness, concession, emotion = compute_metrics(text)
            
            results.append({
                "file": filename,
                "condition": condition_label,
                "assertiveness": assertiveness,
                "concession": concession,
                "emotion": emotion
            })
    
    return results


# ==========================
# 4. EXECUTAR ANÁLISE
# ==========================

baseline_results = process_folder("DATA_CLEAN_NPC/Baseline", "baseline")
scaffolded_results = process_folder("DATA_CLEAN_NPC/Scaffolded", "scaffolded")

all_results = baseline_results + scaffolded_results

df = pd.DataFrame(all_results)

print(df)

# Salvar CSV final
df.to_csv("npc_metrics.csv", index=False)

print("\nArquivo 'npc_metrics.csv' salvo com sucesso.")