import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

hf_token = "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"
login(hf_token)


model_name = tokenizer_name = "Viet-Mistral/Vistral-7B-Chat"
path_or_model = lambda path, model: path if os.path.exists(path) else model

tokenizer_path = path_or_model(PATHS["VISTRAL_7B_TOKENIZER"], model_name)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

model_path = path_or_model(PATHS["VISTRAL_7B_MODEL"], model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,  # change to torch.float16 if you're using V100
    device_map="auto",
    use_cache=True,
)
if model_path == model_name:
    model.save_pretraind(PATHS["VISTRAL_7B_MODEL"])

if tokenizer_path == tokenizer_name:
    tokenizer.save_pretraind(PATHS["VISTRAL_7B_TOKENIZER"])


def generate_response(input_text: str, max_length: int = 2000) -> str:
    conversation = [{"role": "user", "content": input_text}]
    input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt").to(model.device)
    out_ids = model.generate(
        input_ids=input_ids,
        max_new_tokens=max_length * 0.75,
        do_sample=True,
        top_p=0.95,
        top_k=40,
        temperature=0.1,
        repetition_penalty=1.05,
    )
    text = tokenizer.batch_decode(out_ids[:, input_ids.size(1) :], skip_special_tokens=True)[0].strip()
    return text


print(generate_response("Luật sư tư vấn về vấn đề hợp đồng lao động."))
