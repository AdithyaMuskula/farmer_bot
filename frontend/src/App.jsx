// App.jsx
// ─────────────────────────────────────────────
// Root component: decides whether to show Login or ChatPage
// based on JWT token presence in localStorage

import { useState, useEffect } from "react";
import Login    from "./pages/Login";
import ChatPage from "./pages/ChatPage";

export default function App() {
  const [token, setToken] = useState(null);
  const [hydrated, setHydrated] = useState(false);

  // Check localStorage on first render
  useEffect(() => {
    const saved = localStorage.getItem("token");
    if (saved) setToken(saved);
    setHydrated(true);
  }, []);

  // Prevent flash of wrong page on first load
  if (!hydrated) return null;

  const handleLogin = (newToken) => {
    setToken(newToken);
  };

  const handleLogout = () => {
    setToken(null);
  };

  return token
    ? <ChatPage onLogout={handleLogout} />
    : <Login    onLogin={handleLogin}  />;
}