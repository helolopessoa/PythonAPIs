import os

def parse_dialogue(file_path):
    """
    Lê um arquivo de diálogo e transforma em lista estruturada.
    Espera linhas no formato:
    Player: ...
    Npc: ...
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    dialogue = []

    for line in lines:
        line = line.strip()

        if line.startswith("Player:"):
            dialogue.append({
                "speaker": "Player",
                "text": line.replace("Player:", "").strip()
            })

        elif line.startswith("Npc:"):
            dialogue.append({
                "speaker": "NPC",
                "text": line.replace("Npc:", "").strip()
            })

    return dialogue


def build_turns(dialogue, window=3):
    """
    Constrói pares (contexto → resposta) apenas para falas do NPC.
    """
    turns = []

    for i in range(len(dialogue)):
        if dialogue[i]["speaker"] == "NPC":

            # pega janela de contexto anterior
            context_window = dialogue[max(0, i - window):i]

            # monta contexto com speaker tags
            context = "\n".join(
                f'{t["speaker"]}: {t["text"]}'
                for t in context_window
            )

            # resposta atual do NPC
            response = f'NPC: {dialogue[i]["text"]}'

            # evita contexto vazio
            if context.strip():
                turns.append((context, response))

    return turns


def load_dataset(folder_path, window=3):
    """
    Percorre todas as subpastas e carrega os diálogos.
    Retorna lista de diálogos com seus turnos.
    """
    dataset = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):

                path = os.path.join(root, file)

                dialogue = parse_dialogue(path)
                turns = build_turns(dialogue, window)

                if turns:
                    dataset.append({
                        "file": file,
                        "turns": turns
                    })

    return dataset