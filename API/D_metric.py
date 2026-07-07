import os
import re
import csv
import requests

BASE_PATH = "Dados/VSMTest"

# =========================
# Cultural profiles
# =========================

cultural_profile = {
    "Ranger": {
        "time": "future",
        "wealth": "moderate",
        "dignity": "high",
        "politeness": "high",
        "rationality": "high",
        "collectivism": "high"
    },
    "Downside": {
        "time": "present",
        "wealth": "high",
        "dignity": "low",
        "politeness": "low",
        "rationality": "moderate",
        "collectivism": "low"
    }
}

probe_trait_map = {
    1: "time",
    2: "dignity",
    3: "dignity",
    4: "wealth",
    5: "politeness",
    6: "wealth",
    7: "dignity",
    8: "wealth",
    9: "wealth",
    10: "wealth",
    11: "rationality",
    12: "rationality",
    13: "politeness",
    14: "wealth",
    15: "rationality",
    16: "rationality",
    17: "collectivism",
    18: "dignity",
    19: "collectivism",
    20: "politeness",
    21: "dignity",
    22: "time",
    23: "collectivism",
    24: "dignity",
}

# probe_trait_map = { 1: "collectivism", 2: "collectivism", 3: "time", 4: "time", 5: "wealth", 6: "wealth", 7: "dignity", 8: "dignity", 9: "politeness", 10: "politeness", 11: "rationality", 12: "rationality", 13: "collectivism", 14: "collectivism", 15: "rationality", 16: "rationality", 17: "rationality", 18: "rationality", 19: "collectivism", 20: "dignity", 21: "rationality", 22: "rationality", 23: "rationality", 24: "rationality", }

def evaluate_alignment_llm(response, trait, expected):
    prompt = f"""
You are evaluating whether a dialogue response reflects a specific cultural trait.

Trait: {trait}
Expected behavior: {expected}

Evaluate the response below.

Response:
"{response}"

Scoring rules:
0 = contradicts the expected behavior
1 = does not explicitly express the trait but is not inconsistent
2 = clearly expresses the expected trait

IMPORTANT:
- Focus ONLY on the specified trait
- Ignore other aspects
- Output ONLY: 0, 1, or 2
- If the trait is not explicitly mentioned but culturally consistent, prefer score 1.

Answer:
"""

    try:
        res = requests.post(
            "http://localhost:11434/modelapi/classification",
            json={"prompt": prompt}
        )
        return int(res.json().get("result", "").strip())
    except:
        return 1

def infer_rating_llm(response, trait, expected):
    prompt = f"""
You are evaluating how important something is.

Cultural trait: {trait}
Expected orientation: {expected}

Scale:
1 = very important
2 = important
3 = moderate
4 = low importance
5 = no importance

Response:
"{response}"

Instructions:
- Infer importance from meaning
- "irrelevant", "pointless" → 5
- "secondary" → 3 or 4
- valued → 1 or 2
- Output ONLY one number (1–5)

Answer:
"""

    try:
        res = requests.post(
            "http://localhost:11434/modelapi/classification",
            json={"prompt": prompt}
        )
        return int(res.json().get("result", "").strip())
    except:
        return None
    

# =========================
# Helpers
# =========================

# def extract_rating(text):
#     nums = re.findall(r"\b([1-5])\b", text)
#     if nums:
#         return int(nums[-1])
#     return None


def extract_scored_sentences(text):
    sentences = []

    for match in re.finditer(r'\b([1-5])\b', text):
        start = match.start()
        end = match.end()

        prev = max(
            text.rfind('.', 0, start),
            text.rfind('?', 0, start),
            text.rfind('!', 0, start)
        )

        next_candidates = [
            text.find('.', end),
            text.find('?', end),
            text.find('!', end)
        ]

        next_candidates = [i for i in next_candidates if i != -1]
        next_ = min(next_candidates) if next_candidates else len(text)

        sentence = text[prev + 1:next_ + 1].strip()
        sentences.append(sentence)

    return sentences


def detect_culture(filename):
    name = filename.lower()
    if "ranger" in name:
        return "Ranger"
    elif "downside" in name:
        return "Downside"
    return None

def extract_rating(text):
    nums = re.findall(r"\b([1-5])\b", text)
    if nums:
        return int(nums[-1])
    return None


# def detect_culture(filename):
#     name = filename.lower()
#     if "ranger" in name:
#         return "Ranger"
#     elif "downside" in name:
#         return "Downside"
#     return None


# =========================
# FIX PRINCIPAL AQUI
# =========================
def extract_all_responses(text):
    # NÃO filtra agressivamente
    lines = text.split("\n")

    # mantém ordem e conteúdo
    responses = [line.strip() for line in lines]

    # remove apenas linhas realmente vazias
    responses = [r for r in responses if r != ""]

    return responses


# =========================
# MAIN PIPELINE
# =========================
def process_all(output_csv="results_full.csv"):
    results = []

    total_files = 0

    # =========================
    # COUNT FILES
    # =========================
    for condition in ["Baseline", "Scaffold"]:
        condition_path = os.path.join(BASE_PATH, condition)

        if not os.path.exists(condition_path):
            continue

        for run_folder in os.listdir(condition_path):
            run_path = os.path.join(condition_path, run_folder, "NPCResume")

            if not os.path.exists(run_path):
                continue

            total_files += len([f for f in os.listdir(run_path) if f.endswith(".txt")])

    print(f"\n📁 Total files to process: {total_files}\n")

    file_counter = 0

    # =========================
    # MAIN LOOP
    # =========================
    for condition in ["Baseline", "Scaffold"]:
        condition_path = os.path.join(BASE_PATH, condition)

        if not os.path.exists(condition_path):
            continue

        for run_folder in os.listdir(condition_path):
            run_path = os.path.join(condition_path, run_folder, "NPCResume")

            if not os.path.exists(run_path):
                continue

            for file in os.listdir(run_path):

                if not file.endswith(".txt"):
                    continue

                file_counter += 1

                print(f"\n📄 [{file_counter}/{total_files}] Processing:")
                print(f"   Condition: {condition}")
                print(f"   Run: {run_folder}")
                print(f"   File: {file}")

                file_path = os.path.join(run_path, file)

                culture = detect_culture(file)
                if culture is None:
                    print("   ⚠ Skipped (no culture detected)\n")
                    continue

                profile = cultural_profile[culture]

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                # 🔥 leitura simples e correta
                responses = extract_all_responses(text)

                print(f"   🔍 Total responses found: {len(responses)}")

                # 🔥 segurança
                if len(responses) != 24:
                    print(f"   ⚠ WARNING: Expected 24 responses, got {len(responses)}")

                for i, response in enumerate(responses):

                    if response.strip() == "":
                        continue

                    probe_id = i + 1

                    if probe_id not in probe_trait_map:
                        print(f"   ⚠ Skipping probe {probe_id}")
                        continue

                    trait = probe_trait_map[probe_id]
                    expected = profile[trait]

                    print(f"   ↳ Probe {probe_id} ({trait})")

                    # =========================
                    # RATING
                    # =========================
                    rating = extract_rating(response)

                    if rating is None:
                        print("      ⚠ No explicit rating → inferring...")
                        rating = infer_rating_llm(response, trait, expected)
                        inferred = True
                    else:
                        inferred = False

                    if rating is None:
                        print("      ❌ Failed to infer rating")
                        rating_norm = None
                    else:
                        rating_norm = (rating - 1) / 4

                    # =========================
                    # ALIGNMENT
                    # =========================
                    alignment = evaluate_alignment_llm(response, trait, expected)
                    alignment_norm = alignment / 2

                    print(f"      ✅ rating={rating} | inferred={inferred} | alignment={alignment}")

                    # =========================
                    # SAVE
                    # =========================
                    results.append({
                        "condition": condition,
                        "run": run_folder,
                        "file": file,
                        "npc": file.split("_")[2] if "_" in file else "unknown",
                        "culture": culture,
                        "probe_id": probe_id,
                        "trait": trait,
                        "expected": expected,
                        "rating": rating,
                        "rating_norm": rating_norm,
                        "inferred_rating": inferred,
                        "alignment": alignment,
                        "alignment_norm": alignment_norm,
                        "response": response
                    })

                print("   ✔ File done\n")

    # =========================
    # SAVE CSV
    # =========================
    if results:
        with open(output_csv, "w", newline="", encoding="utf-8") as out:
            writer = csv.DictWriter(out, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print(f"\n🎉 Saved {len(results)} rows → {output_csv}")
    else:
        print("No data found.")

# def extract_all_responses(text):
#     return [line.strip() for line in text.split("\n") if line.strip()]


def process_test_run(run_id, output_csv="results_test_final.csv"):
    results = []

    print(f"\n🧪 TEST RUN: {run_id}\n")

    file_counter = 0
    total_files = 0

    # =========================
    # CONTAR ARQUIVOS
    # =========================
    for condition in ["Baseline", "Scaffold"]:
        path = os.path.join(BASE_PATH, condition, run_id, "NPCResume")
        if os.path.exists(path):
            total_files += len([f for f in os.listdir(path) if f.endswith(".txt")])

    print(f"📁 Total files: {total_files}\n")

    # =========================
    # LOOP PRINCIPAL
    # =========================
    for condition in ["Baseline", "Scaffold"]:

        path = os.path.join(BASE_PATH, condition, run_id, "NPCResume")

        if not os.path.exists(path):
            print(f"⚠ Missing: {path}")
            continue

        for file in os.listdir(path):

            if not file.endswith(".txt"):
                continue

            file_counter += 1
            print(f"\n📄 [{file_counter}/{total_files}] {file} ({condition})")

            culture = detect_culture(file)
            if culture is None:
                print("   ⚠ No culture detected")
                continue

            profile = cultural_profile[culture]

            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                text = f.read()

            # =========================
            # 🔥 LEITURA SIMPLES E SEGURA
            # =========================
            responses = text.split("\n")

            # mantém ordem, remove espaços
            responses = [r.strip() for r in responses]

            # remove só linhas vazias (sem bagunçar índice antes)
            responses = [r for r in responses if r != ""]

            print(f"   🔍 Responses found: {len(responses)}")

            # ⚠️ sanity check
            if len(responses) != 24:
                print(f"   ⚠ WARNING: Expected 24, got {len(responses)}")

            # =========================
            # PROCESSAMENTO
            # =========================
            for i, response in enumerate(responses):

                probe_id = i + 1

                if probe_id not in probe_trait_map:
                    print(f"   ⚠ Skipping probe {probe_id}")
                    continue

                trait = probe_trait_map[probe_id]
                expected = profile[trait]

                print(f"   ↳ Probe {probe_id} ({trait})")

                # =========================
                # RATING
                # =========================
                rating = extract_rating(response)

                if rating is None:
                    print("      ⚠ No explicit rating → inferring...")
                    rating = infer_rating_llm(response, trait, expected)
                    inferred = True
                else:
                    inferred = False

                if rating is None:
                    print("      ❌ Failed to infer rating")
                    rating_norm = None
                else:
                    rating_norm = (rating - 1) / 4

                # =========================
                # ALIGNMENT
                # =========================
                alignment = evaluate_alignment_llm(response, trait, expected)
                alignment_norm = alignment / 2

                print(f"      ✅ rating={rating} | inferred={inferred} | alignment={alignment}")

                # =========================
                # SAVE
                # =========================
                results.append({
                    "condition": condition,
                    "run": run_id,
                    "file": file,
                    "npc": file.split("_")[2] if "_" in file else "unknown",
                    "culture": culture,
                    "probe_id": probe_id,
                    "trait": trait,
                    "expected": expected,
                    "rating": rating,
                    "rating_norm": rating_norm,
                    "inferred_rating": inferred,
                    "alignment": alignment,
                    "alignment_norm": alignment_norm,
                    "response": response
                })

    # =========================
    # SAVE CSV
    # =========================
    if results:
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

        print(f"\n🎉 Saved → {output_csv}")
    else:
        print("No data.")
if __name__ == "__main__":
    # process_test_run("20260413_195552")
    # process_test_run("20260413_164218")
    process_all()