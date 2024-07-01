import axios from 'axios';

const TIMEOUT = 30000;

const timeoutPromise = (ms) => new Promise((_, reject) => {
  setTimeout(() => reject(new Error("Thời gian chờ đã hết, không thể kết nối với server")), ms);
});

export const sendMessageChatService = async (promptInput, model) => {
  try {
    const endpoint = model === 'LegalbizAI' 
      ? 'https://backend-url/ask/legalbizai' 
      : 'https://backend-url/ask/legalbizai_gpt';
    const response = await Promise.race([
      axios.post(endpoint, { question: promptInput }),
      timeoutPromise(TIMEOUT)
    ]);
    return response.data;
  } catch (error) {
    if (error.response) {
      // Lỗi từ server, như lỗi 4xx hoặc 5xx
      throw new Error(`Lỗi server: ${error.response.status} - ${error.response.statusText}`);
    } else if (error.request) {
      // Lỗi kết nối với server, nhưng không nhận được phản hồi
      throw new Error("Không thể kết nối với server, vui lòng kiểm tra kết nối mạng của bạn.");
    } else {
      // Lỗi khác
      throw new Error(`Lỗi: ${error.message}`);
    }
  }
};
