import axios from 'axios';

const TIMEOUT = 3 * 60 * 1000;

const timeoutPromise = (ms) =>
    new Promise((_, reject) => {
        setTimeout(
            () =>
                reject(
                    new Error(
                        'Thời gian chờ đã hết, không thể kết nối với server'
                    )
                ),
            ms
        );
    });

export const sendMessageChatService = async (promptInput, model) => {
    const endpoint = 'http://localhost:8000/stream';

    const response = await Promise.race([
        axios.post(endpoint, { message: promptInput, model }),
        timeoutPromise(TIMEOUT),
    ]);

    return response.data; // Đảm bảo trả về toàn bộ phản hồi từ backend
};
