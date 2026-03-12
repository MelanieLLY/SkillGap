const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();

const normalizedApiBaseUrl = (
  configuredApiBaseUrl && configuredApiBaseUrl.length > 0
    ? configuredApiBaseUrl
    : "http://127.0.0.1:8000"
).replace(/\/+$/, "");

export const API_BASE_URL = `${normalizedApiBaseUrl}/api`;
