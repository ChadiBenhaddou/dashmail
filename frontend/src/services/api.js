const BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

function getTokens() {
  try {
    const raw = localStorage.getItem("tokens");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function saveTokens(tokens) {
  localStorage.setItem("tokens", JSON.stringify(tokens));
}

export function clearTokens() {
  localStorage.removeItem("tokens");
}

export function isAuthenticated() {
  return !!getTokens()?.access;
}

async function authFetch(url, options = {}) {
  const tokens = getTokens();
  const headers = { ...options.headers, "Content-Type": "application/json" };
  if (tokens?.access) {
    headers["Authorization"] = `Bearer ${tokens.access}`;
  }
  const res = await fetch(url, { ...options, headers });
  if (res.status === 401 && tokens?.refresh) {
    const refreshRes = await fetch(`${BASE_URL}/api/auth/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: tokens.refresh }),
    });
    if (refreshRes.ok) {
      const data = await refreshRes.json();
      saveTokens({
        access: data.access,
        refresh: data.refresh || tokens.refresh,
      });
      headers["Authorization"] = `Bearer ${data.access}`;
      const retryRes = await fetch(url, { ...options, headers });
      if (!retryRes.ok) {
        const err = new Error(`Erreur ${retryRes.status}`);
        err.status = retryRes.status;
        throw err;
      }
      return retryRes.json();
    }
    clearTokens();
    window.location.href = "/login";
    const se = new Error("Session expirée");
    se.status = 401;
    throw se;
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const e = new Error(err.error || err.detail || `Erreur ${res.status}`);
    e.status = res.status;
    throw e;
  }
  return res.json();
}

export async function register(data) {
  const res = await authFetch(`${BASE_URL}/api/auth/register/`, {
    method: "POST",
    body: JSON.stringify(data),
  });
  saveTokens(res.tokens);
  return res;
}

export async function login(email, password) {
  const res = await authFetch(`${BASE_URL}/api/auth/login/`, {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  saveTokens(res.tokens);
  return res;
}

export async function getMe() {
  return authFetch(`${BASE_URL}/api/auth/me/`);
}

export async function getReport(id) {
  return authFetch(`${BASE_URL}/api/dashboard/${id}/`);
}

export async function uploadFile(file, title, prompt) {
  const tokens = getTokens();
  const formData = new FormData();
  formData.append("file", file);
  if (title) formData.append("title", title);
  if (prompt) formData.append("custom_prompt", prompt);

  const headers = {};
  if (tokens?.access) {
    headers["Authorization"] = `Bearer ${tokens.access}`;
  }

  const res = await fetch(`${BASE_URL}/api/reports/upload/`, {
    method: "POST",
    headers,
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    const e = new Error(err.error || `Erreur ${res.status}`);
    e.status = res.status;
    throw e;
  }
  return res.json();
}

export async function getReports(params = {}) {
  const query = new URLSearchParams(params).toString();
  return authFetch(`${BASE_URL}/api/reports/${query ? `?${query}` : ""}`);
}

export async function getStats() {
  return authFetch(`${BASE_URL}/api/stats/`);
}

export async function getSettings() {
  return authFetch(`${BASE_URL}/api/admin/settings/`);
}

export async function updateSettings(payload) {
  const tokens = getTokens();
  const headers = { "Content-Type": "application/json" };
  if (tokens?.access) headers["Authorization"] = `Bearer ${tokens.access}`;
  const res = await fetch(`${BASE_URL}/api/admin/settings/`, {
    method: "PUT",
    headers,
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || err.detail || `Erreur ${res.status}`);
  }
  return res.json();
}
