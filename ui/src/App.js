import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar";
import LandingPage from "./pages/landingPage";
import ChatPage from "./pages/chatPage";

function App() {
  const [userName, setUserName] = useState("");

  return (
    <Router>
      <Navbar userName={userName} />
      <Routes>
        <Route path="/" element={<LandingPage setUserName={setUserName} />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  );
}

export default App;
