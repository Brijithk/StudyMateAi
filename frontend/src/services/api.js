const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function registerUser(userData) {
  const response = await fetch(`${API_BASE_URL}/auth/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  const data = await response.json();

  if (!response.ok) {
    const message = Object.values(data).flat().join(" ");
    throw new Error(message || "Registration failed.");
  }

  return data;
}

export async function loginUser(username, password) {
  const response = await fetch(`${API_BASE_URL}/auth/token/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Login failed.");
  }

  return data;
}