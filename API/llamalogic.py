from llama_cpp import Llama
import os, torch

def auto_gpu_layers():
    # Automatically determine optimal gpu_layers for ctransformers based on available GPU VRAM.
    if not torch.cuda.is_available():
        # print("[Model] No GPU found → using CPU only.")
        return 0
    props = torch.cuda.get_device_properties(0)
    total_vram = props.total_memory
    total_gb = total_vram / (1024 ** 3)

    # print(f"[Model] GPU detected: {props.name}")
    # print(f"[Model] VRAM: {total_gb:.2f} GB")

    if total_gb < 4:
        layers = 0
    elif total_gb < 6:
        layers = 10
    elif total_gb < 8:
        layers = 20
    elif total_gb < 10:
        layers = 30
    elif total_gb < 12:
        layers = 40
    else:
        layers = 50

    # print(f"[Model] Auto-selecting gpu_layers={layers}")
    return layers

max_threads = os.cpu_count()
max_gpu_layers = auto_gpu_layers()
MODEL_PATH = "models/llama-pro-8b-instruct.Q6_K.gguf"

# Load model ONCE globally when this file is imported
# llm = AutoModelForCausalLM.from_pretrained(
#     MODEL_PATH,
#     model_type="Model",
#     gpu_layers= max_gpu_layers,  # increase if you have a GPU
#     threads = max_threads
# )

llm = Llama(MODEL_PATH, 
            n_ctx=4096,
            n_threads=max_threads,
            n_gpu_layers=max_gpu_layers,
            verbose=False,)

def llamaAnswer(full_prompt: str, max_new_tokens: int = 60) -> str:
    output = llm(
        full_prompt,
        max_tokens=max_new_tokens,
        temperature=0.8,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.15,
        presence_penalty=0.1,
        frequency_penalty=0.1,
        stop=["User:", "System:", "Assistant:"],
        stream=False
    )
    return output









# from ctransformers import AutoModelForCausalLM
# import os, torch

# def auto_gpu_layers():
#     # Automatically determine optimal gpu_layers for ctransformers based on available GPU VRAM.
#     if not torch.cuda.is_available():
#         # print("[Model] No GPU found → using CPU only.")
#         return 0
#     props = torch.cuda.get_device_properties(0)
#     total_vram = props.total_memory
#     total_gb = total_vram / (1024 ** 3)

#     # print(f"[Model] GPU detected: {props.name}")
#     # print(f"[Model] VRAM: {total_gb:.2f} GB")

#     if total_gb < 4:
#         layers = 0
#     elif total_gb < 6:
#         layers = 10
#     elif total_gb < 8:
#         layers = 20
#     elif total_gb < 10:
#         layers = 30
#     elif total_gb < 12:
#         layers = 40
#     else:
#         layers = 50

#     # print(f"[Model] Auto-selecting gpu_layers={layers}")
#     return layers

# max_threads = os.cpu_count()
# max_gpu_layers = auto_gpu_layers()
# MODEL_PATH = "models/Model-pro-8b-instruct.Q6_K.gguf"

# # Load model ONCE globally when this file is imported
# llm = AutoModelForCausalLM.from_pretrained(
#     MODEL_PATH,
#     model_type="Model",
#     gpu_layers= max_gpu_layers,  # increase if you have a GPU
#     threads = max_threads
# )

# def generateResponse(full_prompt: str, max_new_tokens: int = 120) -> str:
#     # response = llm(
#     #     full_prompt,
#     #     max_new_tokens=max_new_tokens,
#     #     temperature=1.0,
#     #     top_p=1.0,
#     #     repetition_penalty=1.1,
#     # )
#     response = llm(
#         full_prompt,
#         max_new_tokens=max_new_tokens,
#         temperature=0.8,
#         top_p=0.9,
#         top_k=40,
#         repetition_penalty=1.15,
#         presence_penalty=0.1,
#         frequency_penalty=0.1,
#         stop=["User:", "System:", "Assistant:"]
#     )

#     return response.strip()
