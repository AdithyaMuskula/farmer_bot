// services/api.js
// ─────────────────────────────────────────────
// Centralized API layer — all backend calls live here
// Automatically handles 401 → clears token → redirects to login
// ─────────────────────────────────────────────

const BASE_URL = "http://127.0.0.1:8000";

// Helper: build auth header
const authHeader = (token) => ({
  Authorization: `Bearer ${token}`,
});

// ─────────────────────────────────────────────
// 401 HANDLER — clears stale token and reloads
// ─────────────────────────────────────────────
function handle401() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  // Force full reload → App.jsx will see no token → show Login
  window.location.reload();
}

// Wrapper: fetch + 401 guard
async function apiFetch(url, options = {}) {
  const res = await fetch(url, options);

  if (res.status === 401) {
    handle401();
    // Return a dummy rejected-ish object so callers don't crash
    throw new Error("Session expired. Please log in again.");
  }

  return res;
}

// ─────────────────────────────────────────────
// AUTH
// ─────────────────────────────────────────────

/**
 * Login with username + password.
 * Returns { access_token, token_type } or { message } on failure.
 */
export async function loginUser(username, password) {
  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ username, password }),
  });
  return res.json();
}

/**
 * Register a new user.
 * Backend expects username + password as query params.
 * Returns { message: "User created" } or { message: "User already exists" }
 */
export async function signupUser(username, password) {
  const params = new URLSearchParams({ username, password });
  const res = await fetch(`${BASE_URL}/signup?${params.toString()}`, {
    method: "POST",
  });
  return res.json();
}

// ─────────────────────────────────────────────
// CHAT HISTORY
// ─────────────────────────────────────────────

/**
 * Fetch full chat history for authenticated user.
 * Returns array of { id, question, answer }
 */
export async function getHistory(token) {
  const res = await apiFetch(`${BASE_URL}/history`, {
    headers: {
      ...authHeader(token),
    },
  });
  return res.json();
}

// ─────────────────────────────────────────────
// ASK — TEXT ONLY
// ─────────────────────────────────────────────

/**
 * Send a plain text question to the AI.
 * Returns { answer: string }
 */
export async function askQuestion(question, token) {
  const res = await apiFetch(`${BASE_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeader(token),
    },
    body: JSON.stringify({ question }),
  });
  return res.json();
}

// ─────────────────────────────────────────────
// ASK — WITH IMAGE
// ─────────────────────────────────────────────

/**
 * Send a question + image file to the AI vision endpoint.
 * Returns { answer: string }
 */
export async function askWithImage(question, imageFile, token) {
  const formData = new FormData();
  formData.append("question", question);
  if (imageFile) {
    formData.append("file", imageFile);
  }

  const res = await apiFetch(`${BASE_URL}/image-question`, {
    method: "POST",
    headers: {
      ...authHeader(token),
      // NOTE: Do NOT set Content-Type manually when using FormData
      // The browser sets it automatically with the correct boundary
    },
    body: formData,
  });
  return res.json();
}
