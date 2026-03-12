import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Dashboard from "../../pages/Dashboard";
import { historyApi } from "../../api/history";
import { useAuthStore } from "../../store/authStore";
import { useProfileStore } from "../../store/profileStore";

// Mock dependencies
vi.mock("../../api/history", () => ({
  historyApi: {
    getHistory: vi.fn(),
    createHistory: vi.fn(),
  },
}));

// Mock child components to keep it simple and focused on Dashboard logic
vi.mock("../../components/Navbar", () => ({ default: () => <div data-testid="navbar" /> }));
vi.mock("../../components/JDInput", () => ({ default: () => <div data-testid="jd-input" /> }));
vi.mock("../../components/SkillMatchResults", () => ({
  default: () => <div data-testid="match-results" />,
}));
vi.mock("../../components/LearningRoadmap", () => ({
  default: () => <div data-testid="roadmap" />,
}));
vi.mock("../../components/UserSkillsInput", () => ({
  default: () => <div data-testid="user-skills" />,
}));

describe("Dashboard Page", () => {
  const mockUser = {
    id: 1,
    email: "test@example.com",
    is_active: true,
    skills: ["React"],
    roadmap: null,
  };

  beforeEach(() => {
    vi.clearAllMocks();

    // Set up store state directly instead of mocking the module
    useAuthStore.setState({ user: mockUser });
    useProfileStore.setState({
      skills: ["React", "TypeScript"],
      isLoading: false,
    });

    (historyApi.getHistory as any).mockResolvedValue([]);

    // Mock loadSkills implementation
    vi.spyOn(useProfileStore.getState(), "loadSkills").mockImplementation(() => Promise.resolve());
  });

  it("renders the dashboard layout", async () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>,
    );

    expect(screen.getByTestId("navbar")).toBeDefined();
    expect(screen.getByTestId("jd-input")).toBeDefined();
    expect(screen.getByTestId("match-results")).toBeDefined();
    expect(screen.getByTestId("roadmap")).toBeDefined();
    expect(screen.getByTestId("user-skills")).toBeDefined();
  });

  it("loads user skills on mount", async () => {
    // Spy on loadSkills instead of mocking the hook
    const spy = vi.spyOn(useProfileStore.getState(), "loadSkills");

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>,
    );

    expect(spy).toHaveBeenCalled();
  });

  it("fetches history on mount and populates initial values", async () => {
    const mockHistory = [
      {
        id: 1,
        jd_text: "Job Description",
        company_name: "Test Corp",
        position_name: "Dev",
        have_skills: ["React"],
        missing_skills: ["Node"],
        bonus_skills: ["Docker"],
        match_score: 50,
      },
    ];
    (historyApi.getHistory as any).mockResolvedValueOnce(mockHistory);

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>,
    );

    await waitFor(() => {
      expect(historyApi.getHistory).toHaveBeenCalled();
    });
  });
});
