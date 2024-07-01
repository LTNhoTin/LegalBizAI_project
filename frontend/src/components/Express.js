const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/ask/legalbizai', (req, res) => {
    // Gọi model LegalBizAI và trả về kết quả
    const result = callLegalBizAI(req.body.question);
    res.json({ answer: result.answer, source_documents: result.source_documents });
});

app.post('/ask/legalbizai_gpt', (req, res) => {
    // Gọi model LegalBizAI_gpt và trả về kết quả
    const result = callLegalBizAIGPT(req.body.question);
    res.json({ answer: result.answer, source_documents: result.source_documents });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

function callLegalBizAI(question) {
    return { answer: "Đây là câu trả lời từ LegalBizAI", source_documents: [] };
}

function callLegalBizAIGPT(question) {
    return { answer: "Đây là câu trả lời từ LegalBizAI_gpt", source_documents: [] };
}
