import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Login from "../../pages/Login";
import { authApi } from "../../api/auth";
import { useAuthStore } from "../../store/authStore";

// Mock the API
vi.mock("../../api/auth", () => ({
  authApi: {
    login: vi.fn(),
  },
}));

// Mock react-router-dom's useNavigate
const mockNavigate = vi.fn();
vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe("Login Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useAuthStore.getState().logout();
  });

  it("renders login form correctly", () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    expect(screen.getByText("Welcome to SkillGap")).toBeDefined();
    expect(screen.getByLabelText(/email/i)).toBeDefined();
    expect(screen.getByLabelText(/password/i)).toBeDefined();
    expect(screen.getByRole("button", { name: /sign in/i })).toBeDefined();
  });

  it("updates input fields on change", () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    const emailInput = screen.getByLabelText(/email/i) as HTMLInputElement;
    const passwordInput = screen.getByLabelText(/password/i) as HTMLInputElement;

    fireEvent.change(emailInput, { target: { value: "test@example.com" } });
    fireEvent.change(passwordInput, { target: { value: "password123" } });

    expect(emailInput.value).toBe("test@example.com");
    expect(passwordInput.value).toBe("password123");
  });

  it("handles successful login", async () => {
    const mockToken = "mock-jwt-token";
    (authApi.login as any).mockResolvedValueOnce({
      access_token: mockToken,
      token_type: "bearer",
    });

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(authApi.login).toHaveBeenCalledWith({
        username: "test@example.com",
        password: "password123",
      });
    });

    expect(useAuthStore.getState().token).toBe(mockToken);
    expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
  });

  it("handles login failure with error message", async () => {
    const errorMessage = "Invalid credentials";
    (authApi.login as any).mockRejectedValueOnce({
      response: {
        data: {
          detail: errorMessage,
        },
      },
    });

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "wrong@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "wrongpass" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeDefined();
    });
  });

  it("handles generic login failure", async () => {
    (authApi.login as any).mockRejectedValueOnce(new Error("Network Error"));

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>,
    );

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "error@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: "anypass" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/login failed/i)).toBeDefined();
    });
  });
});
