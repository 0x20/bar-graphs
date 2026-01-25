const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface Debtor {
  username: string;
  balance: number;
}

class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
    this.name = "ApiError";
  }
}

async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("bar_dashboard_token");

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Token is invalid or expired, clear storage and redirect to login
    localStorage.removeItem("bar_dashboard_token");
    localStorage.removeItem("bar_dashboard_username");
    window.location.href = "/login";
    throw new ApiError(401, "Unauthorized");
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      response.status,
      errorData.detail || `HTTP error ${response.status}`
    );
  }

  return response.json();
}

export const api = {
  getDebtors: () => fetchWithAuth<Debtor[]>("/api/debtors"),

  getLoginUrl: () => `${API_BASE_URL}/auth/login`,
};
