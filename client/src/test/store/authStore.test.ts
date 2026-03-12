import { describe, it, expect, vi, beforeEach } from "vitest";

// ── Mock localStorage ─────────────────────────────────────────────────────────
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] ?? null,
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(globalThis, "localStorage", {
  value: localStorageMock,
  writable: true,
});

// ── Mock external API dependencies ────────────────────────────────────────────
vi.mock("../../api/auth", () => ({
  authApi: {
    me: vi.fn(),
  },
  default: { post: vi.fn(), get: vi.fn() },
}));

vi.mock("../../store/profileStore", () => ({
  useProfileStore: {
    getState: () => ({
      loadSkills: vi.fn(),
    }),
  },
}));

describe("useAuthStore", () => {
  beforeEach(() => {
    localStorageMock.clear();
    vi.resetModules();
  });

  it("initialises token from localStorage", async () => {
    localStorageMock.setItem("token", "my-jwt-token");
    const { useAuthStore } = await import("../../store/authStore");
    expect(useAuthStore.getState().token).toBe("my-jwt-token");
  });

  it("initialises token as null when localStorage is empty", async () => {
    const { useAuthStore } = await import("../../store/authStore");
    expect(useAuthStore.getState().token).toBeNull();
  });

  it("setUser updates the user in state", async () => {
    const { useAuthStore } = await import("../../store/authStore");
    const testUser = {
      id: 1,
      email: "test@example.com",
      is_active: true,
      skills: ["React"],
      roadmap: null,
    };
    useAuthStore.getState().setUser(testUser);
    expect(useAuthStore.getState().user).toEqual(testUser);
  });

  it("setUser(null) clears the user", async () => {
    const { useAuthStore } = await import("../../store/authStore");
    useAuthStore.getState().setUser({
      id: 1,
      email: "a@b.com",
      is_active: true,
      skills: [],
      roadmap: null,
    });
    useAuthStore.getState().setUser(null);
    expect(useAuthStore.getState().user).toBeNull();
  });

  it("logout clears token from localStorage", async () => {
    localStorageMock.setItem("token", "some-token");
    const { useAuthStore } = await import("../../store/authStore");
    useAuthStore.getState().logout();
    expect(localStorageMock.getItem("token")).toBeNull();
  });

  it("logout clears token and user from state", async () => {
    const { useAuthStore } = await import("../../store/authStore");
    useAuthStore.getState().logout();
    expect(useAuthStore.getState().token).toBeNull();
    expect(useAuthStore.getState().user).toBeNull();
  });
});
