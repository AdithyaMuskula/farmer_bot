// components/Sidebar.jsx
// ─────────────────────────────────────────────
// Left sidebar: new chat, history list, user info + logout

// SVG Icons (inline)
const PlusIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const ChatIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
  </svg>
);

const LogoutIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
    <polyline points="16 17 21 12 16 7" />
    <line x1="21" y1="12" x2="9" y2="12" />
  </svg>
);

export default function Sidebar({
  history,        // array of { id, question, answer }
  activeId,       // currently selected history item id
  onSelectChat,   // fn(item) → loads that conversation
  onNewChat,      // fn() → clears chat
  onLogout,       // fn() → clears token
  username,       // string
  isOpen,         // boolean (mobile)
  onClose,        // fn() → close sidebar on mobile
}) {
  const initials = username ? username.charAt(0).toUpperCase() : "U";

  return (
    <>
      {/* Mobile overlay */}
      <div
        className={`sidebar-overlay ${isOpen ? "visible" : ""}`}
        onClick={onClose}
      />

      <aside className={`sidebar ${isOpen ? "open" : ""}`}>
        {/* ── Top: New Chat ── */}
        <div className="sidebar-top">
          <button className="new-chat-btn" onClick={onNewChat}>
            <PlusIcon />
            New Chat
          </button>
        </div>

        {/* ── History List ── */}
        <div className="sidebar-history">
          {history.length > 0 && (
            <span className="history-label">Recent</span>
          )}

          {history.length === 0 ? (
            <p className="sidebar-empty">No conversations yet.</p>
          ) : (
            history.map((item) => (
              <button
                key={item.id}
                className={`history-item ${activeId === item.id ? "active" : ""}`}
                onClick={() => {
                  onSelectChat(item);
                  onClose?.();
                }}
                title={item.question}
              >
                <ChatIcon />
                <span className="history-item-text">
                  {item.question.slice(0, 32)}{item.question.length > 32 ? "…" : ""}
                </span>
              </button>
            ))
          )}
        </div>

        {/* ── Bottom: User + Logout ── */}
        <div className="sidebar-bottom">
          <div className="user-info">
            <div className="user-avatar">{initials}</div>
            <span className="user-name">{username || "User"}</span>
            <button
              className="logout-btn"
              onClick={onLogout}
              title="Sign out"
            >
              <LogoutIcon />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
