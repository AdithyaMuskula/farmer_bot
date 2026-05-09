// components/ChatInput.jsx
// ─────────────────────────────────────────────
// Bottom input bar: textarea + image upload + send button

import { useState, useRef } from "react";

// SVG Icons (inline to avoid dependencies)
const SendIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);

const ImageIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <circle cx="8.5" cy="8.5" r="1.5" />
    <polyline points="21 15 16 10 5 21" />
  </svg>
);

const XIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

export default function ChatInput({ onSend, loading }) {
  const [text, setText] = useState("");
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Auto-resize textarea
  const handleTextChange = (e) => {
    setText(e.target.value);
    const el = e.target;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 160) + "px";
  };

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImageFile(file);
    setImagePreview(URL.createObjectURL(file));
    // reset input so same file can be reselected
    e.target.value = "";
  };

  const removeImage = () => {
    setImageFile(null);
    setImagePreview(null);
  };

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || loading) return;

    onSend(trimmed, imageFile);

    // Reset
    setText("");
    setImageFile(null);
    setImagePreview(null);
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e) => {
    // Enter sends, Shift+Enter adds newline
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const canSend = text.trim().length > 0 && !loading;

  return (
    <div className="input-wrapper">
      {/* Image preview bar */}
      {imagePreview && (
        <div className="image-preview-bar">
          <img src={imagePreview} alt="preview" className="image-preview-thumb" />
          <span className="image-preview-name">{imageFile?.name}</span>
          <button className="image-remove-btn" onClick={removeImage} title="Remove image">
            <XIcon />
          </button>
        </div>
      )}

      {/* Input box */}
      <div className="chat-input-box">
        <textarea
          ref={textareaRef}
          className="chat-textarea"
          placeholder="Ask about crops, pests, weather, prices..."
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={loading}
        />

        <div className="input-actions">
          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            style={{ display: "none" }}
            onChange={handleImageSelect}
          />

          {/* Image upload button */}
          <button
            className="icon-btn"
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
            title="Upload crop image"
          >
            <ImageIcon />
          </button>

          {/* Send button */}
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={!canSend}
            title="Send message"
          >
            <SendIcon />
          </button>
        </div>
      </div>

      <p className="input-footer">
        Farmer AI may make mistakes. Always verify critical decisions with an expert.
      </p>
    </div>
  );
}
