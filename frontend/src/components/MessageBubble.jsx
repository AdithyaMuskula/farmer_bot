// components/MessageBubble.jsx
// ─────────────────────────────────────────────
// Renders a single message (user or bot) with avatar

export default function MessageBubble({ role, text, isTyping = false }) {
  const isUser = role === "user";

  return (
    <div className={`message-row ${isUser ? "user" : "bot"}`}>
      {/* Meta row: avatar + sender name */}
      <div className="message-meta">
        <div className={`message-avatar ${isUser ? "user-avatar-msg" : "bot-avatar-msg"}`}>
          {isUser ? "U" : "🌱"}
        </div>
        <span>{isUser ? "You" : "Farmer AI"}</span>
      </div>

      {/* Bubble content */}
      <div className="message-bubble">
        {isTyping ? (
          <div className="typing-bubble">
            <span className="typing-dot" />
            <span className="typing-dot" />
            <span className="typing-dot" />
          </div>
        ) : (
          text
        )}
      </div>
    </div>
  );
}
