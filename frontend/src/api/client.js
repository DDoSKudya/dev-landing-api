const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export async function submitContact(payload) {
  const response = await fetch(`${API_BASE}/contact`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  let body = {};
  try {
    body = await response.json();
  } catch {
    body = {};
  }

  if (!response.ok) {
    const error = new Error(body.message || "Request failed");
    error.status = response.status;
    error.body = body;
    error.retryAfter = response.headers.get("Retry-After");
    throw error;
  }

  return body;
}
