import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from huggingface_hub import login
from LegalBizAI_project.backend.constants import PATHS

hf_token = "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"
login(hf_token)

torch.cuda.empty_cache()


def path_or_model(path, model_id):
    return path if os.path.exists(path) else model_id


bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model_id = "Viet-Mistral/Vistral-7B-Chat"
model_path = path_or_model(PATHS["VISTRAL_7B_MODEL"] + "/config.json", model_id)

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    use_cache=True,
)
# if model_path == model_id:
#     model.config.save_pretrained(PATHS["VISTRAL_7B_MODEL"])
#     tokenizer.save_pretrained(PATHS["VISTRAL_7B_MODEL"])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# system_prompt = """
# Chào bạn, tôi là LegalBizAI, AI tư vấn Luật Doanh Nghiệp Việt Nam từ Team 3. Đặt câu hỏi về Luật Doanh Nghiệp để tôi giải đáp. 😊😊
# Hướng dẫn trả lời:
# •	Về bản thân và người sáng tạo: Trả lời như trên, không cần cú pháp Trích dẫn luật, Trả lời.
# •	Câu hỏi không liên quan: Từ chối trả lời, nêu lý do LegalBizAI chỉ hỗ trợ Luật Doanh Nghiệp.
# •	Câu hỏi liên quan: Trả lời dựa trên Căn cứ luật dưới đây. Câu trả lời gồm 2 phần trong 2 heading "Trích dẫn luật:" và "Trả lời:". Phần trích dẫn luật in ra đầy đủ nội dung luật cần thiết để trả lời câu hỏi Xuống dòng phân cách rõ ràng. Giải thích chi tiết lý do từ căn cứ luật, in đậm chi tiết quan trọng."""

oneshot_example = """
Ví dụ về format của câu trả lời:
\"\"\"
**Trích dẫn luật:**

Luật Doanh Nghiệp 2020

*Điều 188. Doanh nghiệp tư nhân*

*Khoản 3. Mỗi cá nhân chỉ được quyền thành lập một doanh nghiệp tư nhân. Chủ doanh nghiệp tư nhân không được đồng thời là chủ hộ kinh doanh, thành viên hợp danh của công ty hợp danh.*

**Trả lời:**

Theo Khoản 3, Điều 188 Luật Doanh Nghiệp 2020, mỗi cá nhân chỉ được quyền thành lập một doanh nghiệp tư nhân. Do đó, một cá nhân chỉ được phép thành lập tối đa một doanh nghiệp tư nhân.
\"\"\"
"""


def generate_response(input_text: str, max_length: int = 2000) -> str:
    # conversation = [{"role": "system", "content": system_prompt}]
    conversation = [{"role": "user", "content": input_text + oneshot_example}]
    input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt", add_generation_prompt=True).to(device)
    print("Input token count=", input_ids.size(1))
    out_ids = model.generate(
        input_ids=input_ids,
        max_new_tokens=3000,
    )
    text = tokenizer.batch_decode(out_ids[:, input_ids.size(1) :], skip_special_tokens=True)[0].strip()
    return text
