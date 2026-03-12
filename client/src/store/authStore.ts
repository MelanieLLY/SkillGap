import { create } from "zustand";
import { authApi } from "../api/auth";
import { useProfileStore } from "./profileStore";

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  skills: string[];
}

interface AuthState {
  token: string | null;
  user: User | null;
  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  token: localStorage.getItem("token"),
  user: null,
  setToken: (token) => {
    if (token) {
      localStorage.setItem("token", token);
      // After successful login / token set, fetch user + skills profile
      get()
        .fetchUser()
        .then(() => {
          useProfileStore.getState().loadSkills();
        });
    } else {
      localStorage.removeItem("token");
    }
    set({ token });
  },
  setUser: (user) => set({ user }),
  logout: () => {
    localStorage.removeItem("token");
    set({ token: null, user: null });
  },
  fetchUser: async () => {
    const { token, user } = get();
    if (token && !user) {
      try {
        const userData = await authApi.me();
        // We use any cast here because API UserOut might not match exactly,
        // but we know it does have skills after the recent changes.
        set({ user: userData as User });
      } catch (error) {
        console.error("Failed to fetch user profile:", error);
        localStorage.removeItem("token");
        set({ token: null, user: null });
      }
    }
  },
}));
