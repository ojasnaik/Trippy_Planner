import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import Message from "../components/message";
import "./chatPage.css";

const ChatPage = () => {
  const [messages, setMessages] = useState([
    { text: "What's on your mind?", sender: "agent" },
  ]);
  const [input, setInput] = useState("");
  const messageEndRef = useRef(null);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      const userMessage = { text: input, sender: "user" };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInput("");

      // Call the backend API with the user's message
      try {
        const response = await axios.post(
          "http://localhost:8005/submit",
          {
            message: input,
            type: "final"
          }
        );
        console.log(response);
        if (response?.data) {
          const botMessage = { text: response?.data?.response, sender: "agent" };
          const followupMessage = { text: "\nSo what's on your mind (next)? Need any suggestions on which city to visit? Want to know about flights? Need to know about hotels? Curious about activities or attractions? If you are satisified by the current itenary then enter 'yes', else lets continue chatting. \n", sender: "agent" };
          setMessages((prevMessages) => [...prevMessages, botMessage, followupMessage]);
        }
      } catch (error) {
        console.error("Failed to fetch agent response:", error);
        const errorMessage = {
          text: "Error: Could not fetch response from agent.",
          sender: "agent",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    }
  };

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div>
      <div className="background-image"></div>
      <div className="chat-container">
        <div className="message-container">
          {messages.map((msg, index) => (
            <Message key={index} text={msg.text} sender={msg.sender} />
          ))}
          <div ref={messageEndRef} />
        </div>
        <form onSubmit={sendMessage} className="message-form">
          <input
            type="text"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="message-input"
          />
          <button type="submit" className="send-button">
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatPage;
