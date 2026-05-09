// pages/ChatPage.jsx
// ─────────────────────────────────────────────
// Main chat layout — owns all state, assembles
// Sidebar + ChatWindow + ChatInput

import { useState, useEffect, useCallback } from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import { getHistory, askQuestion, askWithImage } from "../services/api";
import "../styles/chat.css";

// Hamburger SVG icon
const MenuIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="3" y1="6" x2="21" y2="6" />
    <line x1="3" y1="12" x2="21" y2="12" />
    <line x1="3" y1="18" x2="21" y2="18" />
  </svg>
);

export default function ChatPage({ onLogout }) {
  // ── Auth ──
  const token    = localStorage.getItem("token") || "";
  const username = localStorage.getItem("username") || "User";

  // ── State ──
  const [messages,   setMessages]   = useState([]);   // { role, text }[]
  const [history,    setHistory]    = useState([]);   // { id, question, answer }[]
  const [activeId,   setActiveId]   = useState(null); // selected history item
  const [loading,    setLoading]    = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // ── Load history on mount ──
  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = useCallback(async () => {
    try {
      const data = await getHistory(token);
      if (Array.isArray(data)) {
        // Reverse so newest is at top
        setHistory([...data].reverse());
      }
    } catch (err) {
      console.error("Failed to load history:", err);
    }
  }, [token]);

  // ── New Chat ──
  const handleNewChat = () => {
    setMessages([]);
    setActiveId(null);
    setSidebarOpen(false);
  };

  // ── Click a history item → load its Q&A as a conversation ──
  const handleSelectChat = (item) => {
    setActiveId(item.id);
    setMessages([
      { role: "user", text: item.question },
      { role: "bot",  text: item.answer   },
    ]);
  };

  // ── Send a message ──
  const handleSend = async (text, imageFile) => {
    // Immediately show user message
    setMessages((prev) => [...prev, { role: "user", text }]);
    setLoading(true);

    try {
      let data;

      if (imageFile) {
        data = await askWithImage(text, imageFile, token);
      } else {
        data = await askQuestion(text, token);
      }

      const answer = data.answer || "Sorry, I could not generate a response.";

      // Show bot answer
      setMessages((prev) => [...prev, { role: "bot", text: answer }]);

      // Refresh sidebar history (new entry was saved by backend)
      await loadHistory();

    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ── Logout ──
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    onLogout();
  };

  // ── Welcome chip quick-send ──
  const handleChipClick = (prompt) => {
    handleSend(prompt, null);
  };

  return (
    <div className="chat-page">
      {/* Mobile hamburger */}
      <button
        className="hamburger-btn"
        onClick={() => setSidebarOpen(true)}
        aria-label="Open sidebar"
      >
        <MenuIcon />
      </button>

      {/* Left Sidebar */}
      <Sidebar
        history={history}
        activeId={activeId}
        onSelectChat={handleSelectChat}
        onNewChat={handleNewChat}
        onLogout={handleLogout}
        username={username}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Right Chat Area */}
      <main className="chat-main">
        <ChatWindow
          messages={messages}
          loading={loading}
          onChipClick={handleChipClick}
        />
        <ChatInput onSend={handleSend} loading={loading} />
      </main>
    </div>
  );
}
