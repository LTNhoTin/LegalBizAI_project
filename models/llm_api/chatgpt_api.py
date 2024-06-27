import openai

# Thiết lập API key
openai.api_key = "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"

def get_chatgpt_answer(question, context):
    prompt = f"Question: {question}\n\nContext: {context}\n\nAnswer:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Lỗi khi gửi yêu cầu tới ChatGPT: {e}")
        return ""

if __name__ == "__main__":
    # Giả sử câu hỏi và ngữ cảnh liên quan đến luật doanh nghiệp đã có sẵn
    question = "Các yêu cầu pháp lý để thành lập một công ty tại Việt Nam là gì?"
    context = """
    Theo Luật Doanh nghiệp Việt Nam, các yêu cầu pháp lý để thành lập một công ty bao gồm:
    1. Đăng ký kinh doanh tại Sở Kế hoạch và Đầu tư.
    2. Có tên công ty phù hợp với quy định của pháp luật.
    3. Có trụ sở chính hợp pháp tại Việt Nam.
    4. Có vốn điều lệ theo quy định.
    5. Đăng ký mã số thuế và tài khoản ngân hàng.
    6. Tuân thủ các quy định về ngành nghề kinh doanh có điều kiện.
    """

    # Lấy câu trả lời từ ChatGPT
    answer = get_chatgpt_answer(question, context)
    print(f"Q: {question}\nA: {answer}")
