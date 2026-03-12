import axios from "axios";
import { useAuthStore } from "../store/authStore";
import { API_BASE_URL } from "../lib/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Configure interceptor to inject JWT token into requests
apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API types
export interface LoginData {
  username: string; // FastAPI OAuth2 uses 'username' for the email field
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface UserOut {
  id: number;
  email: string;
  is_active: boolean;
  skills: string[];
}

export const authApi = {
  login: async (data: LoginData) => {
    // FastAPI OAuth2PasswordRequestForm expects form-urlencoded data, not JSON
    const formData = new URLSearchParams();
    formData.append("username", data.username);
    formData.append("password", data.password);

    const response = await apiClient.post<AuthResponse>("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    return response.data;
  },

  register: async (data: RegisterData) => {
    const response = await apiClient.post<UserOut>("/auth/register", data);
    return response.data;
  },

  me: async () => {
    const response = await apiClient.get<UserOut>("/auth/me");
    return response.data;
  },
};

export default apiClient;
