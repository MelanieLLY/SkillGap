import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, vi, beforeEach } from "vitest";
import History from "../../pages/History";
import { historyApi } from "../../api/history";

// Mock dependencies
vi.mock("../../api/history", () => ({
  historyApi: {
    getHistory: vi.fn(),
  },
}));

vi.mock("../../components/Navbar", () => ({ default: () => <div data-testid="navbar" /> }));

describe("History Page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders history page and displays loading state", () => {
    (historyApi.getHistory as any).mockReturnValue(new Promise(() => {})); // Never resolves
    render(
      <BrowserRouter>
        <History />
      </BrowserRouter>
    );
    expect(screen.getByText("Analysis History")).toBeDefined();
    // Check for spinner - it's a div with animate-spin
    const mainElement = screen.getByRole("main");
    expect(mainElement.querySelector(".animate-spin")).not.toBeNull();
  });

  it("displays empty state when no history is found", async () => {
    (historyApi.getHistory as any).mockResolvedValueOnce([]);

    render(
      <BrowserRouter>
        <History />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText("No History Yet")).toBeDefined();
    });
  });

  it("displays history records when data is loaded", async () => {
    const mockHistory = [
      {
        id: 1,
        position_name: "Software Engineer",
        company_name: "Google",
        match_score: 85,
        have_skills: ["React", "TypeScript"],
        missing_skills: ["Go"],
        bonus_skills: ["GCP"],
        date_analyzed: "2023-10-27T10:00:00Z",
      },
    ];
    (historyApi.getHistory as any).mockResolvedValueOnce(mockHistory);

    render(
      <BrowserRouter>
        <History />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText("Software Engineer")).toBeDefined();
      expect(screen.getByText("Google")).toBeDefined();
      expect(screen.getByText("85%")).toBeDefined();
      expect(screen.getByText("React, TypeScript")).toBeDefined();
      expect(screen.getByText("Go")).toBeDefined();
      expect(screen.getByText("GCP")).toBeDefined();
    });
  });

  it("displays error message when API fails", async () => {
    (historyApi.getHistory as any).mockRejectedValueOnce(new Error("API Error"));

    render(
      <BrowserRouter>
        <History />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/failed to load history/i)).toBeDefined();
    });
  });
});
