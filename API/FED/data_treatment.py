from pathlib import Path
import os


# 🔹 Função para formatar diálogo
def format_conversation(text):
    lines = text.split("\n")
    
    formatted = []
    speaker = "Player"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        formatted.append(f"{speaker}: {line}")
        speaker = "Npc" if speaker == "Player" else "Player"
    
    return "\n".join(formatted)


# 🔹 Função principal
def process_folder(base_path):
    base_path = Path(base_path)

    print(f"\n📂 Processando: {base_path}")

    # encontra todas as pastas ConversationResume
    folders = list(base_path.glob("**/ConversationResume"))

    print(f"Pastas encontradas: {len(folders)}")

    for folder in folders:
        print(f"\n📁 Pasta: {folder}")

        # cria nova pasta
        new_folder = folder.parent / "TaggedConversationResume"
        new_folder.mkdir(exist_ok=True)

        files = list(folder.glob("*.txt"))

        print(f"Arquivos: {len(files)}")

        for file_path in files:
            print(f"→ {file_path.name}")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # 🔥 aplica formatação
            formatted_text = format_conversation(text)

            # salva novo arquivo
            new_file_path = new_folder / file_path.name

            with open(new_file_path, "w", encoding="utf-8") as f:
                f.write(formatted_text)

    print("\n✅ Processo concluído!")


# 🔹 Rodar para os dois casos
process_folder("LLMAsPlayer/Baseline")
process_folder("LLMAsPlayer/Scaffold")