// pages/Login.jsx
// ─────────────────────────────────────────────
// Full-screen login/signup page with dark card and mode toggle

import { useState } from "react";
import { loginUser, signupUser } from "../services/api";
import "../styles/login.css";

export default function Login({ onLogin }) {
  const [mode, setMode]         = useState("login"); // "login" | "signup"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirm,  setConfirm]  = useState("");       // signup only
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState("");
  const [success,  setSuccess]  = useState("");

  // Switch modes and reset form state
  const switchMode = (newMode) => {
    setMode(newMode);
    setError("");
    setSuccess("");
    setPassword("");
    setConfirm("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!username.trim() || !password.trim()) {
      setError("Please fill in all fields.");
      return;
    }

    // ── SIGNUP ──
    if (mode === "signup") {
      if (password !== confirm) {
        setError("Passwords do not match.");
        return;
      }
      if (password.length < 4) {
        setError("Password must be at least 4 characters.");
        return;
      }

      setLoading(true);
      try {
        const data = await signupUser(username.trim(), password);

        if (data.message === "User created") {
          setSuccess("Account created! You can now sign in.");
          setPassword("");
          setConfirm("");
          // Auto-switch to login after short delay
          setTimeout(() => switchMode("login"), 1500);
        } else if (data.message === "User already exists") {
          setError("That username is already taken. Try another.");
        } else {
          setError("Signup failed. Please try again.");
        }
      } catch {
        setError("Unable to connect to the server. Is the backend running?");
      } finally {
        setLoading(false);
      }
      return;
    }

    // ── LOGIN ──
    setLoading(true);
    try {
      const data = await loginUser(username.trim(), password);

      if (data.access_token) {
        localStorage.setItem("token",    data.access_token);
        localStorage.setItem("username", username.trim());
        onLogin(data.access_token);
      } else if (data.message === "User not found") {
        setError("No account found. Please sign up first.");
      } else if (data.message === "Incorrect password") {
        setError("Incorrect password. Please try again.");
      } else {
        setError(data.message || "Login failed. Please try again.");
      }
    } catch {
      setError("Unable to connect to the server. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const isSignup = mode === "signup";

  return (
    <div className="login-page">
      <div className="login-card">

        {/* ── Header ── */}
        <div className="login-header">
          <div className="login-logo">🌱</div>
          <h1 className="login-title">Farmer AI</h1>
          <p className="login-subtitle">Your intelligent agriculture assistant</p>
        </div>

        {/* ── Mode Toggle Tabs ── */}
        <div className="auth-tabs">
          <button
            type="button"
            className={`auth-tab ${mode === "login" ? "active" : ""}`}
            onClick={() => switchMode("login")}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`auth-tab ${mode === "signup" ? "active" : ""}`}
            onClick={() => switchMode("signup")}
          >
            Create Account
          </button>
        </div>

        {/* ── Form ── */}
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label className="input-label" htmlFor="login-username">Username</label>
            <input
              id="login-username"
              type="text"
              className="login-input"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              autoFocus
            />
          </div>

          <div className="input-group">
            <label className="input-label" htmlFor="login-password">Password</label>
            <input
              id="login-password"
              type="password"
              className="login-input"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete={isSignup ? "new-password" : "current-password"}
            />
          </div>

          {/* Confirm password — signup only */}
          {isSignup && (
            <div className="input-group" style={{ animation: "fadeIn 0.2s ease" }}>
              <label className="input-label" htmlFor="login-confirm">Confirm Password</label>
              <input
                id="login-confirm"
                type="password"
                className="login-input"
                placeholder="Re-enter your password"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="new-password"
              />
            </div>
          )}

          {/* Messages */}
          {error   && <p className="login-error">{error}</p>}
          {success && <p className="login-success">{success}</p>}

          <button type="submit" className="login-btn" disabled={loading}>
            {loading
              ? (isSignup ? "Creating account…" : "Signing in…")
              : (isSignup ? "Create Account" : "Sign In")}
          </button>
        </form>

        {/* ── Footer switch ── */}
        <p className="login-footer">
          {isSignup
            ? <>Already have an account?{" "}
                <span className="login-link" onClick={() => switchMode("login")}>Sign in</span>
              </>
            : <>Don't have an account?{" "}
                <span className="login-link" onClick={() => switchMode("signup")}>Create one</span>
              </>
          }
        </p>
      </div>
    </div>
  );
}
