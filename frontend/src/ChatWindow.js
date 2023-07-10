import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';

const ChatWindow = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    setChatHistory(prevChatHistory => [
      { message: "Hello, I am JoshGPT. I am an AI model trained to answer questions about Josh Bhattarai.\nAsk any question about Josh and I will try to answer it.", sender: 'JoshGPT' }
    ]);
  }, []);

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

  const sendMessage = () => {
    if (message.trim() !== '') {
      const messageData = {
        message: message
      };


       setChatHistory(prevChatHistory => [
         ...prevChatHistory,
         { message: message, sender: 'User' }
       ]);

      axios.post(
        'http://localhost:8000/api/messages',
        messageData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      )
        .then(response => {
          // Update chat history with user and server messages

          setChatHistory(prevChatHistory => [
            ...prevChatHistory,
            { message: response.data.response, sender: 'JoshGPT' }
          ]);

          scrollToBottom();
        })
        .catch(error => {
          console.error(error);
          setChatHistory(prevChatHistory => [
            ...prevChatHistory,
            { message: "Sorry I ran into an error:\n" + error.toString() + "\nPlease try again.", sender: 'JoshGPT' }
          ]);
        });

      setMessage('');
    }
  };

  const handleKeyDown = event => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  return (
    <div>
      <div style={{ width: '50%', marginLeft: 'auto', marginRight: 'auto' }}>
        <div
          style={{
            border: '1px solid #ccc',
            backgroundColor: '#f5f5f5',
            padding: '10px',
            height: '75vh',
            overflow: 'auto',
          }}
          ref={chatContainerRef}
        >
          {/* Render chat messages */}
          {chatHistory.map((chat, index) => (
            <React.Fragment key={index}>
              {/* Display sender above each message */}
              <div style={{ textAlign: chat.sender === 'User' ? 'left' : 'right', paddingRight: chat.sender === 'User' ? '0px' : '15px' }}>
                {chat.sender}:
              </div>
              {/* Style chat messages */}
              <div style={{ display: 'flex', flexDirection: chat.sender === 'User' ? 'row' : 'row-reverse' }}>
                <div
                  key={index}
                  style={{
                    padding: '7px',
                    margin: '5px',
                    borderRadius: '15px',
                    display: 'inline-block',
                    backgroundColor: chat.sender === 'User' ? '#cddc39' : '#87CEEB',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {chat.message}
                </div>
              </div>
            </React.Fragment>
          ))}
        </div>

        <div>
          {/* Input for sending new messages */}
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
            <input
              type="text"
              value={message}
              onChange={e => setMessage(e.target.value)}
              onKeyDown={handleKeyDown} // Added event listener for Enter key press
              placeholder="Please type a message..."
              style={{
                flex: '1',
                height: '40px',
                padding: '8px',
                border: '1px solid #ccc',
                borderRadius: '4px',
                marginRight: '10px',
                fontSize: '16px',
              }}
            />
            <button
              onClick={sendMessage}
              style={{
                height: '40px',
                padding: '8px 20px',
                backgroundColor: '#4caf50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
