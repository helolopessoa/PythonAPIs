# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# # Modelo DialogRPT (updown é o mais usado)
# model_name = "microsoft/DialogRPT-updown"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# def score_dialogue(context, response):
#     input_text = context + " [SEP] " + response

#     inputs = tokenizer(input_text, return_tensors="pt", truncation=True)
    
#     with torch.no_grad():
#         outputs = model(**inputs)
#         score = torch.sigmoid(outputs.logits).item()
    
#     return score

# context = "We cannot trust them. They have betrayed us before."
# response = "I understand your fear, but perhaps cooperation could lead to a better future."

# score = score_dialogue(context, response)

# print("DialogRPT score:", score)

import os
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ==========================
# 1. LOAD MODEL
# ==========================

model_name = "microsoft/DialogRPT-updown"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


def score_dialogue(context, response):
    input_text = context + " [SEP] " + response

    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        score = torch.sigmoid(outputs.logits).item()

    return score


# ==========================
# 2. PARSE DIALOGUE
# ==========================

def extract_turns(text):
    lines = text.split("\n")
    turns = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # aceita Player, Npc, user, assistant (case insensitive)
        if line.lower().startswith(("player:", "npc:", "assistant:", "user:")):
            turns.append(line)

    return turns


def process_dialogue(text):
    turns = extract_turns(text)
    scores = []

    for i in range(len(turns) - 1):

        # detecta pares Player → NPC
        if turns[i].lower().startswith(("player:", "user:")) and \
           turns[i+1].lower().startswith(("npc:", "assistant:")):

            # remove label automaticamente
            context = turns[i].split(":", 1)[1].strip()
            response = turns[i+1].split(":", 1)[1].strip()

            if context and response:
                score = score_dialogue(context, response)
                scores.append(score)

    if len(scores) == 0:
        return None

    return sum(scores) / len(scores)


# ==========================
# 3. WALK DIRECTORIES
# ==========================

def process_root(root_path, mode):
    results = []

    for condition in ["Baseline", "Scaffold"]:
        condition_path = os.path.join(root_path, condition)

        if not os.path.exists(condition_path):
            continue

        for subdir, _, files in os.walk(condition_path):
            if "TaggedConversationResume" in subdir:

                for file in files:
                    if file.endswith(".txt"):
                        file_path = os.path.join(subdir, file)

                        with open(file_path, "r", encoding="utf-8") as f:
                            text = f.read()

                        score = process_dialogue(text)

                        if score is not None:
                            results.append({
                                "file": file,
                                "mode": mode,
                                "condition": condition.lower(),
                                "dialogrpt": score
                            })

    return results


# ==========================
# 4. RUN
# ==========================

script_data = process_root("../Dados/ScriptsFED", "script")
free_data = process_root("../Dados/LLMAsPlayer", "free")

all_data = script_data + free_data

df = pd.DataFrame(all_data)

print("\n=== RESULTS ===")
print(df)

df.to_csv("dialogrpt_full_results.csv", index=False)

print("\nSaved to dialogrpt_full_results.csv")