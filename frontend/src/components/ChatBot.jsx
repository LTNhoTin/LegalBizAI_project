import robot_img from "../assets/robot_image.png";
import { useState, useRef, useEffect } from "react";
import ScaleLoader from "react-spinners/ScaleLoader";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMessage } from "@fortawesome/free-regular-svg-icons";
import { sendMessageChatService } from './chatbotService';

function ChatBot(props) {
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const [timeOfRequest, setTimeOfRequest] = useState(0);
  const [promptInput, setPromptInput] = useState("");
  const [model, setModel] = useState("LegalbizAI");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoad] = useState(false);
  const [isGen, setIsGen] = useState(false);
  const [dataChat, setDataChat] = useState([
    [
      "start",
      [
        "Xin chào! Đây là LegalBizAI, trợ lý đắc lực về luật doanh nghiệp của bạn! Bạn muốn tìm kiếm thông tin về điều gì? Đừng quên chọn mô hình phù hợp để mình có thể giúp bạn tìm kiếm thông tin chính xác nhất nha. 😄",
        null,
      ],
    ],
  ]);

  const commonQuestions = [
    "Điều kiện để thành lập công ty?",
    "Quy trình đăng ký kinh doanh là gì?",
    "Những yêu cầu pháp lý đối với vốn điều lệ?",
    "Các loại hình doanh nghiệp hiện nay?",
    "Các bước giải thể công ty?",
    "Quy định về thuế đối với doanh nghiệp?",
    "Trách nhiệm pháp lý của giám đốc công ty?",
    "Thủ tục thay đổi đăng ký kinh doanh?",
    "Quy định về lao động trong doanh nghiệp?",
    "Cách xử lý khi công ty bị kiện?",
    "Điều kiện để hợp nhất doanh nghiệp?",
    "Quy định về bảo vệ thông tin doanh nghiệp?"
  ];

  useEffect(() => {
    scrollToEndChat();
    inputRef.current.focus();
  }, [isLoading]);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeOfRequest((timeOfRequest) => timeOfRequest + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const scrollToEndChat = () => {
    messagesEndRef.current.scrollIntoView({ behavior: "auto" });
  };

  const onChangeHandler = (event) => {
    setPromptInput(event.target.value);
  };

  const sendMessageChat = async () => {
    if (promptInput !== "" && isLoading === false) {
      setTimeOfRequest(0);
      setIsGen(true);
      setPromptInput("");
      setIsLoad(true);
      setDataChat((prev) => [...prev, ["end", [promptInput, model]]]);
      setChatHistory((prev) => [promptInput, ...prev]);

      try {
        const result = await sendMessageChatService(promptInput, model);
        setDataChat((prev) => [
          ...prev,
          ["start", [result.answer, result.source_documents, model]],
        ]);
      } catch (error) {
        setDataChat((prev) => [
          ...prev,
          ["start", ["Lỗi, không thể kết nối với server", null]],
        ]);
      } finally {
        setIsLoad(false);
        setIsGen(false);
        inputRef.current.focus();
      }
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendMessageChat();
    }
  };

  const [reference, setReference] = useState({
    title: "",
    source: "",
    url: "",
    text: ``,
  });

  const handleReferenceClick = (source, modelType) => {
    setReference({
      title: source.metadata.title,
      source: modelType,
      url: source.metadata.url,
      text: source.page_content,
    });
  };

  return (
    <div className="bg-gradient-to-r from-orange-50 to-orange-100 flex flex-col" style={{ height: '87vh' }}>
      {/* Dropdown for model selection on mobile */}
      <div className="lg:hidden p-2 flex justify-center bg-gradient-to-r from-orange-50 to-orange-100">
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="w-3/4 p-2 border rounded-lg shadow-md bg-white"
        >
          <option value="LegalbizAI">LegalbizAI</option>
          <option value="LegalbizAI_gpt">LegalbizAI_gpt</option>
        </select>
      </div>

      <div className="hidden lg:block drawer-side absolute w-64 h-[20vh] left-3 mt-2 drop-shadow-md z-10">
        <div className="menu p-2 w-full min-h-full bg-gray-50 text-base-content rounded-2xl mt-3 overflow-auto scroll-y-auto max-h-[80vh]">
          <ul className="menu text-sm">
            <h2 className="font-bold mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
              Lịch sử trò chuyện
            </h2>
            {chatHistory.length === 0 ? (
              <p className="text-sm text-gray-500">
                Hiện chưa có cuộc hội thoại nào
              </p>
            ) : (
              chatHistory.map((mess, i) => (
                <li key={i}>
                  <p>
                    <FontAwesomeIcon icon={faMessage} />
                    {mess.length < 20 ? mess : mess.slice(0, 20) + "..."}
                  </p>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>

      <div className="hidden lg:block drawer-side absolute w-64 h-[20vh] mt-2 right-3 drop-shadow-md z-10">
        <div className="menu p-2 w-full min-h-full bg-gray-50 text-base-content rounded-2xl mt-3">
          <h2 className="font-bold text-sm mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
            Chọn Mô hình
          </h2>
          <ul className="menu">
            <li>
              <label className="label cursor-pointer">
                <span className="label-text font-medium">LegalbizAI</span>
                <input
                  type="radio"
                  name="radio-10"
                  value="LegalbizAI"
                  checked={model === "LegalbizAI"}
                  onChange={(e) => setModel(e.target.value)}
                  className="radio checked:bg-blue-500"
                />
              </label>
            </li>
            <li>
              <label className="label cursor-pointer">
                <span className="label-text font-medium">LegalbizAI_gpt</span>
                <input
                  type="radio"
                  name="radio-10"
                  value="LegalbizAI_gpt"
                  checked={model === "LegalbizAI_gpt"}
                  onChange={(e) => setModel(e.target.value)}
                  className="radio checked:bg-blue-500"
                />
              </label>
            </li>
          </ul>
        </div>
        <div
          className="menu p-2 w-full min-h-full bg-gray-50 text-base-content 
        rounded-2xl mt-3 overflow-auto scroll-y-auto max-h-[43vh]
        scrollbar-thin scrollbar-thumb-gray-300 
          scrollbar-thumb-rounded-full scrollbar-track-rounded-full"
        >
          <ul className="menu text-sm">
            <h2 className="font-bold mb-2 bg-[linear-gradient(90deg,hsl(var(--s))_0%,hsl(var(--sf))_9%,hsl(var(--pf))_42%,hsl(var(--p))_47%,hsl(var(--a))_100%)] bg-clip-text will-change-auto [-webkit-text-fill-color:transparent] [transform:translate3d(0,0,0)] motion-reduce:!tracking-normal max-[1280px]:!tracking-normal [@supports(color:oklch(0_0_0))]:bg-[linear-gradient(90deg,hsl(var(--s))_4%,color-mix(in_oklch,hsl(var(--sf)),hsl(var(--pf)))_22%,hsl(var(--p))_45%,color-mix(in_oklch,hsl(var(--p)),hsl(var(--a)))_67%,hsl(var(--a))_100.2%)]">
              Những câu hỏi phổ biến
            </h2>

            {commonQuestions.map((mess, i) => (
              <li key={i} onClick={() => setPromptInput(mess)}>
                <p className="max-w-64">
                  <FontAwesomeIcon icon={faMessage} />
                  {mess}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="flex flex-col h-full items-center relative z-0 flex-grow">
        <div
          id="chat-area"
          className="
          mt-2 lg:mt-5 text-xs lg:text-sm 
          scrollbar-thin scrollbar-thumb-gray-300 bg-white  
          scrollbar-thumb-rounded-full scrollbar-track-rounded-full
          rounded-3xl border-2 md:w-[50%] md:p-3 p-1 w-full overflow-auto scroll-y-auto flex-grow"
          style={{ maxHeight: 'calc(74vh - 91px)' }} // Adjust this value based on the footer height
        >
          {dataChat.map((dataMessages, i) =>
            dataMessages[0] === "start" ? (
              <div className="chat chat-start drop-shadow-md" key={i}>
                <div className="chat-image avatar">
                  <div className="w-8 lg:w-10 rounded-full border-2 border-blue-500">
                    <img className="scale-150" src={robot_img} alt="avatar" />
                  </div>
                </div>
                <div className="chat-bubble chat-bubble-info break-words">
                  <p style={{ whiteSpace: 'pre-line' }}>
                    {dataMessages[1][0]}
                  </p>
                  {dataMessages[1][1] === null || dataMessages[1][1].length === 0 ? (
                    ""
                  ) : (
                    <>
                      <div className="divider m-0"></div>
                      <p className="font-semibold text-xs">
                        Tham khảo:{" "}
                        {dataMessages[1][1].map((source, j) => (
                          <label
                            htmlFor="my_modal_6"
                            className="kbd kbd-xs mr-1 hover:bg-sky-300 cursor-pointer"
                            onClick={() =>
                              handleReferenceClick(source, dataMessages[1][2])
                            }
                            key={j}
                          >
                            {source.metadata.title}
                          </label>
                        ))}
                      </p>
                    </>
                  )}
                </div>
              </div>
            ) : (
              <div className="chat chat-end" key={i}>
                <div className="chat-bubble shadow-xl chat-bubble-primary bg-gradient-to-r from-purple-500 to-blue-500 text-white">
                  {dataMessages[1][0]}
                  
                  <>
                    <div className="divider m-0"></div>
                    <p className="font-light text-xs text-cyan-50">
                      Mô hình: {dataMessages[1][1]}
                    </p>
                  </>
                </div>
              </div>
            )
          )}
          {isLoading && (
            <div className="chat chat-start">
              <div className="chat-image avatar">
                <div className="w-8 lg:w-10 rounded-full border-2 border-blue-500">
                  <img src={robot_img} alt="avatar" />
                </div>
              </div>
              <div className="chat-bubble chat-bubble-info">
                <ScaleLoader
                  color="#000000"
                  loading={true}
                  height={10}
                  width={10}
                  aria-label="Loading Spinner"
                  data-testid="loader"
                />
                <p className="text-xs font-medium">{timeOfRequest + "/30s"}</p>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="grid md:w-[50%] bg-gradient-to-r from-orange-50 to-orange-100 p-1 rounded-t-lg hide-on-small-screen" style={{ zIndex: 10 }}>
          <input
            type="text"
            placeholder="Nhập câu hỏi tại đây..."
            className="mr-1 shadow-xl border-2 focus:outline-none px-2 rounded-2xl input-primary col-start-1 md:col-end-12 col-end-11"
            onChange={onChangeHandler}
            onKeyDown={handleKeyDown}
            disabled={isGen}
            value={promptInput}
            ref={inputRef}
          />

          <button
            disabled={isGen}
            onClick={sendMessageChat}
            className={
              "drop-shadow-md md:col-start-12 rounded-2xl col-start-11 col-end-12 md:col-end-13 btn btn-active btn-primary btn-square bg-gradient-to-tl from-transparent via-blue-600 to-indigo-500"
            }
          >
            <svg
              stroke="currentColor"
              fill="none"
              strokeWidth="2"
              viewBox="0 0 24 24"
              color="white"
              height="15px"
              width="15px"
              xmlns="http://www.w3.org/2000/svg"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
          <p className="text-xs col-start-1 col-end-12 text-justify p-1">
            <b>Lưu ý: </b>LegalBizAI có thể mắc lỗi. Hãy kiểm tra các thông tin quan trọng!
          </p>
        </div>
      </div>
    </div>
  );
}

export default ChatBot;
