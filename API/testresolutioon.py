from PIL import Image
import os

# pasta raiz que contém os projetos
root_folder = r"C:\Users\helopessoa\Desktop"

# resolução alvo
MAX_WIDTH = 3072
MAX_HEIGHT = 1536

# qualidade JPG
JPEG_QUALITY = 90


for folder_name in os.listdir(root_folder):

    # pega apenas pastas SGM_LAY_PR_
    if not folder_name.startswith("SGM_LAY_PR_020"):
        continue

    project_folder = os.path.join(root_folder, folder_name)

    if not os.path.isdir(project_folder):
        continue

    print(f"\nPROCESSANDO: {folder_name}")

    output_folder = os.path.join(project_folder, "resized_3072")
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(project_folder):

        if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        input_path = os.path.join(project_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        try:
            with Image.open(input_path) as img:

                original_width, original_height = img.size

                scale = min(
                    MAX_WIDTH / original_width,
                    MAX_HEIGHT / original_height
                )

                # impede upscale
                scale = min(scale, 1.0)

                new_width = int(original_width * scale)
                new_height = int(original_height * scale)

                resized = img.resize(
                    (new_width, new_height),
                    Image.LANCZOS
                )

# converte RGBA -> RGB se necessário
                if resized.mode in ("RGBA", "LA", "P"):
                    resized = resized.convert("RGB")

                resized.save(
                    output_path,
                    quality=JPEG_QUALITY,
                    optimize=True
                )

                print(
                    f"OK: {file_name} | "
                    f"{original_width}x{original_height} "
                    f"-> {new_width}x{new_height}"
                )

        except Exception as e:
            print(f"ERRO em {file_name}: {e}")

print("\nFINALIZADO.")