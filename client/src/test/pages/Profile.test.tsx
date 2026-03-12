import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Profile from "../../pages/Profile";
import { useAuthStore } from "../../store/authStore";
import { useProfileStore } from "../../store/profileStore";

// Mock child components
vi.mock("../../components/Navbar", () => ({ default: () => <div data-testid="navbar" /> }));

describe("Profile Page", () => {
  const mockUser = {
    id: 1,
    email: "test@example.com",
    is_active: true,
    skills: ["React"],
    roadmap: null,
  };

  beforeEach(() => {
    vi.clearAllMocks();

    // Set up store state directly
    useAuthStore.setState({ user: mockUser });
    useProfileStore.setState({
      skills: ["React", "TypeScript"],
      isLoading: false,
      error: null,
    });

    // Mock loadSkills to prevent it from resetting isLoading to true on mount
    vi.spyOn(useProfileStore.getState(), "loadSkills").mockImplementation(() => Promise.resolve());
  });

  it("renders profile page correctly", () => {
    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>,
    );

    expect(screen.getByText("Skill Profile Setup")).toBeDefined();
    expect(screen.getByText("React")).toBeDefined();
    expect(screen.getByText("TypeScript")).toBeDefined();
  });

  it("handles adding a skill manually", async () => {
    const spy = vi
      .spyOn(useProfileStore.getState(), "addSkill")
      .mockImplementation(() => Promise.resolve());

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>,
    );

    const input = screen.getByPlaceholderText(/e.g. React/i);
    const addButton = screen.getByRole("button", { name: /add/i });

    fireEvent.change(input, { target: { value: "Python" } });
    fireEvent.click(addButton);

    expect(spy).toHaveBeenCalledWith("Python");
  });

  it("handles removing a skill", async () => {
    const spy = vi
      .spyOn(useProfileStore.getState(), "removeSkill")
      .mockImplementation(() => Promise.resolve());

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>,
    );

    const removeButtons = screen.getAllByLabelText(/remove React/i);
    fireEvent.click(removeButtons[0]);

    expect(spy).toHaveBeenCalledWith("React");
  });

  it("handles resume extraction", async () => {
    const spy = vi
      .spyOn(useProfileStore.getState(), "extractFromResume")
      .mockImplementation(() => Promise.resolve());

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>,
    );

    const textarea = screen.getByPlaceholderText(/paste your resume text/i);
    const extractButton = screen.getByRole("button", { name: /extract skills/i });

    fireEvent.change(textarea, { target: { value: "My experience in Java and SQL." } });
    fireEvent.click(extractButton);

    expect(spy).toHaveBeenCalledWith("My experience in Java and SQL.");
  });

  it("displays loading state when fetching skills", () => {
    useProfileStore.setState({
      skills: [],
      isLoading: true,
      error: null,
    });

    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>,
    );

    expect(screen.getByText("Loading skills...")).toBeDefined();
  });
});
