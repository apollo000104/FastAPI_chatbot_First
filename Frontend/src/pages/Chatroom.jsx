import React, { useState } from "react";
import './Chatroom.css'
import { useRef, useEffect } from "react";
import FileUpload from "../components/FileUpload";
import Headbar from "../components/Headbar";

const Chatroom = () => {
    const [chatText, setChatText] = useState('');
    const [context, setContext] = useState([])
    const [responses, setResponses] = useState([])
    const [isLoading, setIsLoading] = useState(false);

    const handleQuery = (e) => {
        setChatText(e.target.value);
    };
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    const handleSend = async () => {
        setIsLoading(true);
        console.log("ENTER KEY")
        setChatText("")
        const res = await fetch("http://localhost:8000/chatroom",
            {
                method: 'Post',
                headers: {
                    "Content-type": "application/json"
                },
                body: JSON.stringify({ chatText, context })
            }
        );
        setIsLoading(false);
        let returned_data = await res.json()
        setResponses(returned_data.responses)
        setContext(returned_data.context)
        console.log(responses)// console.log(context)
    }

    const chatBoxRef = useRef(null);

    // Function to scroll the chat box to the bottom
    const scrollToBottom = () => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    };

    // Scroll to the bottom when messages change
    useEffect(() => {
        scrollToBottom();
    }, [responses]);

    return (
        <>
            <h1>__________________The most Slowest Chatbot 😂😂😂_________________________</h1>
            <div className="Chat-wrapper" ref={chatBoxRef}>
                {
                    responses.map((item, key) => (
                        <div className="chat-record">
                            <p className="User_input">{item[0]}</p>
                            <p className="Bot_output">{item[1]}</p>
                        </div>
                    ))
                }
            </div>
            <div className="Chatroom">
                <input
                    className="Chatroom-input"
                    type="text"
                    value={chatText}
                    onChange={handleQuery}
                    onKeyDown={handleKeyPress}
                />
                <button className="Chatroom-button" onClick={handleSend} disabled={isLoading}>Send</button>
                <FileUpload />
            </div>

        </>
    )

}

export default Chatroom;