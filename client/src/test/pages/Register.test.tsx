import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Register from "../../pages/Register";
import { authApi } from "../../api/auth";

// Mock the API
vi.mock("../../api/auth", () => ({
  authApi: {
    register: vi.fn(),
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

describe("Register Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders register form correctly", () => {
    render(
      <BrowserRouter>
        <Register />
      </BrowserRouter>
    );

    expect(screen.getByText("Create an account")).toBeDefined();
    expect(screen.getByLabelText(/email/i)).toBeDefined();
    expect(screen.getByLabelText(/^password/i)).toBeDefined();
    expect(screen.getByLabelText(/confirm password/i)).toBeDefined();
    expect(screen.getByRole("button", { name: /register/i })).toBeDefined();
  });

  it("shows error when passwords do not match", async () => {
    render(
      <BrowserRouter>
        <Register />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "test@example.com" } });
    fireEvent.change(screen.getByLabelText(/^password/i), { target: { value: "password123" } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: "mismatch" } });
    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    expect(screen.getByText("Passwords do not match")).toBeDefined();
    expect(authApi.register).not.toHaveBeenCalled();
  });

  it("handles successful registration", async () => {
    (authApi.register as any).mockResolvedValueOnce({
      id: 1,
      email: "test@example.com",
    });

    render(
      <BrowserRouter>
        <Register />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "test@example.com" } });
    fireEvent.change(screen.getByLabelText(/^password/i), { target: { value: "password123" } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: "password123" } });
    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(authApi.register).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "password123",
      });
    });

    expect(mockNavigate).toHaveBeenCalledWith("/login");
  });

  it("handles registration failure", async () => {
    const errorMessage = "Email already exists";
    (authApi.register as any).mockRejectedValueOnce({
      response: {
        data: {
          detail: errorMessage,
        },
      },
    });

    render(
      <BrowserRouter>
        <Register />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "existing@example.com" } });
    fireEvent.change(screen.getByLabelText(/^password/i), { target: { value: "password123" } });
    fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: "password123" } });
    fireEvent.click(screen.getByRole("button", { name: /register/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeDefined();
    });
  });
});
