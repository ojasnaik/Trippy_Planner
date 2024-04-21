// Message.js
import React from "react";
import "./message.css"; // CSS file for styling

const Message = ({ text, sender }) => {
  const messageClass = sender === "user" ? "message user" : "message bot";
  return <div className={messageClass}>{text}</div>;
};

export default Message;
