const dataFAQs = [
  [
    "Chatbot LegalBizAI hoạt động như thế nào?",
    "Chatbot LegalBizAI hoạt động bằng cách sử dụng kỹ thuật tìm văn bản liên quan đến câu hỏi trong bộ dữ liệu đã được vector hóa (text similarity) và lưu trữ thông qua cơ sở dữ liệu vector. Giúp lấy ra những đoạn văn bản có liên quan sau đó dùng mô hình ngôn ngữ lớn (LLM) để sinh câu trả lời."
  ],
  [
    "Cách sử dụng LegalBizAI để tra cứu thông tin",
    "Để sử dụng LegalBizAI một cách hiệu quả nhất bạn nên đặt câu hỏi một cách rõ ràng đầy đủ để mô hình có thể đưa ra câu trả lời chính xác. Tuy nhiên, ở một số trường hợp câu trả lời có thể không chính xác nên bạn phải kiểm chứng thông tin hoặc liên hệ hỗ trợ nếu cần thiết."
  ],
  [
    "Thông tin từ LegalBizAI có đáng tin cậy không?",
    "Vì là một mô hình xác suất nên thông tin LegalBizAI đưa ra có thể không chính xác ở một số trường hợp, bạn nên kiểm chứng thông tin hoặc liên hệ hỗ trợ nếu cần thiết."
  ],
  [
    "Tôi có thể liên hệ hỗ trợ như thế nào?",
    "Vui lòng vào phần Góp ý/báo lỗi hoặc liên hệ với bộ phận pháp lý của công ty bạn để được hỗ trợ thêm."
  ]
];

function FAQPage() {
  return (
    <div className="flex justify-center min-h-[85vh] h-auto bg-gradient-to-br from-orange-50 to-orange-100">
      <div className="md:w-[50%]">
        <h1 className="text-3xl text-center font-bold p-5 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
          Những câu hỏi thường gặp (FAQs)
        </h1>
        {dataFAQs.map((item, i) => (
          <div key={i} className="mt-2 collapse collapse-plus shadow-md rounded-xl bg-white">
            <input type="checkbox" />
            <div className="collapse-title text-base font-medium">
              {item[0]}
            </div>
            <div className="collapse-content">
              <p>{item[1]}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default FAQPage;
