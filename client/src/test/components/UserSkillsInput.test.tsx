import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import UserSkillsInput from "../../components/UserSkillsInput";

describe("UserSkillsInput Component", () => {
  it("renders skills correctly", () => {
    const skills = ["React", "TypeScript"];
    render(<UserSkillsInput skills={skills} onSkillsChange={vi.fn()} />);

    expect(screen.getByText("React")).toBeDefined();
    expect(screen.getByText("TypeScript")).toBeDefined();
  });

  it("calls onSkillsChange when adding a new skill", () => {
    const onSkillsChange = vi.fn();
    const skills = ["React"];
    render(<UserSkillsInput skills={skills} onSkillsChange={onSkillsChange} />);

    const input = screen.getByPlaceholderText(/Add a skill/i);
    fireEvent.change(input, { target: { value: "Python" } });
    fireEvent.keyDown(input, { key: "Enter", code: "Enter" });

    expect(onSkillsChange).toHaveBeenCalledWith(["React", "python"]);
  });

  it("calls onSkillsChange when removing a skill", () => {
    const onSkillsChange = vi.fn();
    const skills = ["React"];
    render(<UserSkillsInput skills={skills} onSkillsChange={onSkillsChange} />);

    const removeButton = screen.getByRole("button", { name: /Remove React/i });
    fireEvent.click(removeButton);

    expect(onSkillsChange).toHaveBeenCalledWith([]);
  });

  it("shows empty state when no skills provided", () => {
    render(<UserSkillsInput skills={[]} onSkillsChange={vi.fn()} />);
    expect(screen.getByText(/No skills added yet/i)).toBeDefined();
  });
});
