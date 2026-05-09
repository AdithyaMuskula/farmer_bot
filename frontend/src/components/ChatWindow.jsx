// components/ChatWindow.jsx
// ─────────────────────────────────────────────
// Displays the list of messages + typing indicator
// Receives: messages[], loading boolean

import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

const WELCOME_PROMPTS = [
  "How do I treat leaf blight?",
  "Best fertilizer for wheat?",
  "Can I spray today?",
  "Tomato price today?",
];

export default function ChatWindow({ messages, loading, onChipClick }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const showWelcome = messages.length === 0 && !loading;

  return (
    <div className="chat-window">
      {showWelcome ? (
        /* ── Welcome / Empty State ── */
        <div className="chat-welcome">
          <div className="chat-welcome-icon">🌱</div>
          <h2>Hello, Farmer!</h2>
          <p>
            Ask me anything about crops, pests, fertilizers, weather, or
            market prices. I'm here to help.
          </p>
          <div className="chat-welcome-chips">
            {WELCOME_PROMPTS.map((prompt) => (
              <button
                key={prompt}
                className="welcome-chip"
                onClick={() => onChipClick?.(prompt)}
              >
                {prompt}
              </button>
            ))}
          </div>
        </div>
      ) : (
        /* ── Message List ── */
        <>
          {messages.map((msg, i) => (
            <MessageBubble key={i} role={msg.role} text={msg.text} />
          ))}

          {/* Typing indicator */}
          {loading && <MessageBubble role="bot" text="" isTyping />}

          {/* Scroll anchor */}
          <div ref={bottomRef} />
        </>
      )}
    </div>
  );
}
