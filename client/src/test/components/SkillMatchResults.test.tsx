import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import SkillMatchResults from "../../components/SkillMatchResults";

describe("SkillMatchResults Component", () => {
  it("renders match percentage and skills", () => {
    const mockSkills = {
      have: ["React"],
      missing: ["Python"],
      bonus: ["AWS"],
    };

    render(<SkillMatchResults skills={mockSkills} />);

    expect(screen.getByText("Skill Match Score")).toBeDefined();
    expect(screen.getByText("50%")).toBeDefined(); // 1 have / (1 have + 1 missing)
    expect(screen.getByText("React")).toBeDefined();
    expect(screen.getByText("Python")).toBeDefined();
    expect(screen.getByText("AWS")).toBeDefined();
  });

  it("shows empty state when skills is null", () => {
    render(<SkillMatchResults skills={null} />);
    expect(screen.getByText(/Paste a JD to begin/i)).toBeDefined();
  });
});
