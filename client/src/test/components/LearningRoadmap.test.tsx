import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import LearningRoadmap from "../../components/LearningRoadmap";

// ── Mock the roadmap API ──────────────────────────────────────────────────────
vi.mock("../../api/roadmap", () => ({
  roadmapApi: {
    generate: vi.fn(),
  },
}));

// ── Mock the authStore ────────────────────────────────────────────────────────
const mockSetUser = vi.fn();
let mockUser: {
  id: number;
  email: string;
  is_active: boolean;
  skills: string[];
  roadmap: null | object;
} | null = null;

vi.mock("../../store/authStore", () => ({
  useAuthStore: () => ({
    user: mockUser,
    setUser: mockSetUser,
  }),
}));

// ── Minimal Roadmap fixture ───────────────────────────────────────────────────
const mockRoadmap = {
  generated_for: "test@example.com",
  generated_at: "2024-01-01",
  missing_skills: ["Docker"],
  total_estimated_duration_weeks: 8,
  timeline: [
    {
      phase: 1,
      title: "Foundation",
      duration_weeks: 4,
      start_week: 1,
      end_week: 4,
      focus_skills: ["Docker"],
      weekly_commitment_hours: 10,
      milestones: ["Complete Docker basics"],
    },
  ],
  course_recommendations: [
    {
      skill: "Docker",
      courses: [
        {
          title: "Docker for Beginners",
          platform: "Udemy",
          instructor: "John Doe",
          level: "Beginner",
          duration_hours: 6,
          url: "https://example.com",
          priority: "primary",
        },
      ],
    },
  ],
  project_ideas: [
    {
      id: "proj-1",
      title: "Containerize a Web App",
      description: "Build a containerized web application",
      skills_practiced: ["Docker"],
      difficulty: "Beginner",
      estimated_hours: 5,
      phase: 1,
      deliverables: ["Dockerfile", "docker-compose.yml"],
    },
  ],
  summary: {
    total_courses: 1,
    total_projects: 1,
    total_learning_hours: 60,
    recommended_weekly_pace: "10h/week",
    completion_target: "2024-03",
  },
};

// ── Helper to import roadmapApi in tests ─────────────────────────────────────
const getRoadmapApi = async () => {
  const { roadmapApi } = await import("../../api/roadmap");
  return roadmapApi;
};

describe("LearningRoadmap", () => {
  beforeEach(() => {
    mockUser = null;
    mockSetUser.mockClear();
  });

  describe("Empty / initial state", () => {
    it("renders the 'Learning Roadmap' heading", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(screen.getByText("Learning Roadmap")).toBeInTheDocument();
    });

    it("renders 'Generate Roadmap' button", () => {
      render(<LearningRoadmap missingSkills={["Docker"]} />);
      expect(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      ).toBeInTheDocument();
    });

    it("shows prompt when no missing skills and no roadmap", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(
        screen.getByText(
          "Analyze a job description first to see your missing skills."
        )
      ).toBeInTheDocument();
    });

    it("shows generate prompt when there are missing skills but no roadmap", () => {
      render(<LearningRoadmap missingSkills={["Docker"]} />);
      expect(
        screen.getByText(
          'Click "Generate Roadmap" to create your personalised learning plan.'
        )
      ).toBeInTheDocument();
    });

    it("disables generate button when missingSkills is empty", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const btn = screen.getByRole("button", { name: /generate learning roadmap/i });
      expect(btn).toBeDisabled();
    });

    it("enables generate button when missingSkills is non-empty", () => {
      render(<LearningRoadmap missingSkills={["Docker"]} />);
      const btn = screen.getByRole("button", { name: /generate learning roadmap/i });
      expect(btn).not.toBeDisabled();
    });
  });

  describe("Loading state", () => {
    it("shows RoadmapSkeleton while generating", async () => {
      const roadmapApi = await getRoadmapApi();
      // Delay resolution to capture loading state
      let resolveGenerate!: (v: { roadmap: typeof mockRoadmap }) => void;
      vi.mocked(roadmapApi.generate).mockReturnValue(
        new Promise((res) => {
          resolveGenerate = res;
        })
      );

      render(<LearningRoadmap missingSkills={["Docker"]} />);
      const btn = screen.getByRole("button", { name: /generate learning roadmap/i });
      fireEvent.click(btn);

      // While loading, skeleton container should appear
      await waitFor(() =>
        expect(
          screen.getByLabelText("Loading learning roadmap")
        ).toBeInTheDocument()
      );

      // Clean up
      resolveGenerate({ roadmap: mockRoadmap });
    });

    it("button shows 'Generating…' text while loading", async () => {
      const roadmapApi = await getRoadmapApi();
      let resolveGenerate!: (v: { roadmap: typeof mockRoadmap }) => void;
      vi.mocked(roadmapApi.generate).mockReturnValue(
        new Promise((res) => {
          resolveGenerate = res;
        })
      );

      render(<LearningRoadmap missingSkills={["React"]} />);
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() =>
        expect(screen.getByText(/generating/i)).toBeInTheDocument()
      );
      resolveGenerate({ roadmap: mockRoadmap });
    });
  });

  describe("Successful generation", () => {
    it("calls roadmapApi.generate with correct payload", async () => {
      const roadmapApi = await getRoadmapApi();
      vi.mocked(roadmapApi.generate).mockResolvedValue({
        roadmap: mockRoadmap,
      });
      mockUser = {
        id: 1,
        email: "test@example.com",
        is_active: true,
        skills: [],
        roadmap: null,
      };

      render(
        <LearningRoadmap missingSkills={["Docker"]} jdText="We need Docker" />
      );
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() => {
        expect(roadmapApi.generate).toHaveBeenCalledWith({
          missing_skills: ["Docker"],
          jd_text: "We need Docker",
        });
      });
    });

    it("calls setUser with updated roadmap after generation", async () => {
      const roadmapApi = await getRoadmapApi();
      vi.mocked(roadmapApi.generate).mockResolvedValue({
        roadmap: mockRoadmap,
      });
      mockUser = {
        id: 1,
        email: "test@example.com",
        is_active: true,
        skills: [],
        roadmap: null,
      };

      render(<LearningRoadmap missingSkills={["Docker"]} />);
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() => {
        expect(mockSetUser).toHaveBeenCalledWith(
          expect.objectContaining({ roadmap: mockRoadmap })
        );
      });
    });
  });

  describe("Roadmap display (pre-loaded)", () => {
    beforeEach(() => {
      mockUser = {
        id: 1,
        email: "test@example.com",
        is_active: true,
        skills: [],
        roadmap: mockRoadmap,
      };
    });

    it("renders total duration weeks", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(screen.getByText("8 weeks")).toBeInTheDocument();
    });

    it("renders total courses badge", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(screen.getByText("1 courses")).toBeInTheDocument();
    });

    it("renders total projects badge", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(screen.getByText("1 projects")).toBeInTheDocument();
    });

    it("renders phase title in timeline", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(screen.getByText("Foundation")).toBeInTheDocument();
    });

    it("renders skill pill for the phase", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(screen.getByText("Docker")).toBeInTheDocument();
    });

    it("phase button is accessible", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      expect(
        screen.getByRole("button", { name: /Phase 1: Foundation/i })
      ).toBeInTheDocument();
    });

    it("phase is collapsed by default (aria-expanded=false)", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const phaseBtn = screen.getByRole("button", {
        name: /Phase 1: Foundation/i,
      });
      expect(phaseBtn).toHaveAttribute("aria-expanded", "false");
    });

    it("expands phase on click (aria-expanded=true)", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const phaseBtn = screen.getByRole("button", {
        name: /Phase 1: Foundation/i,
      });
      fireEvent.click(phaseBtn);
      expect(phaseBtn).toHaveAttribute("aria-expanded", "true");
    });

    it("collapses phase on second click", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const phaseBtn = screen.getByRole("button", {
        name: /Phase 1: Foundation/i,
      });
      fireEvent.click(phaseBtn);
      fireEvent.click(phaseBtn);
      expect(phaseBtn).toHaveAttribute("aria-expanded", "false");
    });

    it("shows milestone text when phase is expanded", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const phaseBtn = screen.getByRole("button", {
        name: /Phase 1: Foundation/i,
      });
      fireEvent.click(phaseBtn);
      expect(screen.getByText("Complete Docker basics")).toBeInTheDocument();
    });

    it("shows course recommendation when phase is expanded", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const phaseBtn = screen.getByRole("button", {
        name: /Phase 1: Foundation/i,
      });
      fireEvent.click(phaseBtn);
      expect(screen.getByText("Docker for Beginners")).toBeInTheDocument();
    });

    it("shows project idea when phase is expanded", () => {
      render(<LearningRoadmap missingSkills={[]} />);
      const phaseBtn = screen.getByRole("button", {
        name: /Phase 1: Foundation/i,
      });
      fireEvent.click(phaseBtn);
      expect(
        screen.getByText("Build a containerized web application")
      ).toBeInTheDocument();
    });
  });

  describe("Error handling", () => {
    it("displays error message on API failure", async () => {
      const roadmapApi = await getRoadmapApi();
      vi.mocked(roadmapApi.generate).mockRejectedValue(new Error("Network error"));

      render(<LearningRoadmap missingSkills={["Docker"]} />);
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() => {
        expect(
          screen.getByText(
            "Failed to generate roadmap. Please ensure the backend is running."
          )
        ).toBeInTheDocument();
      });
    });

    it("displays 504 timeout message", async () => {
      const roadmapApi = await getRoadmapApi();
      vi.mocked(roadmapApi.generate).mockRejectedValue({
        response: { status: 504 },
      });

      render(<LearningRoadmap missingSkills={["Docker"]} />);
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() => {
        expect(
          screen.getByText(
            "Claude AI took too long to respond. Please try again."
          )
        ).toBeInTheDocument();
      });
    });

    it("displays 502 bad gateway message", async () => {
      const roadmapApi = await getRoadmapApi();
      vi.mocked(roadmapApi.generate).mockRejectedValue({
        response: { status: 502 },
      });

      render(<LearningRoadmap missingSkills={["Docker"]} />);
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() => {
        expect(
          screen.getByText(
            "Failed to get a valid response from Claude AI. Please try again."
          )
        ).toBeInTheDocument();
      });
    });

    it("re-enables generate button after error", async () => {
      const roadmapApi = await getRoadmapApi();
      vi.mocked(roadmapApi.generate).mockRejectedValue(new Error("fail"));

      render(<LearningRoadmap missingSkills={["Docker"]} />);
      fireEvent.click(
        screen.getByRole("button", { name: /generate learning roadmap/i })
      );

      await waitFor(() => {
        const btn = screen.getByRole("button", { name: /generate learning roadmap/i });
        expect(btn).not.toBeDisabled();
      });
    });
  });
});
