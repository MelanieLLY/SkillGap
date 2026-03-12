import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import JDInput from "../../components/JDInput";

describe("JDInput Component", () => {
  it("renders correctly", () => {
    render(<JDInput onAnalyze={vi.fn()} isLoading={false} />);
    expect(screen.getByText("Job Description")).toBeDefined();
    expect(screen.getByPlaceholderText(/Paste Job Description Here/i)).toBeDefined();
  });

  it("calls onAnalyze when form is filled and button clicked", () => {
    const onAnalyze = vi.fn();
    render(<JDInput onAnalyze={onAnalyze} isLoading={false} />);

    fireEvent.change(screen.getByPlaceholderText(/Paste Job Description Here/i), {
      target: { value: "We need a React dev." },
    });
    fireEvent.change(screen.getByPlaceholderText(/Company Name/i), {
      target: { value: "Google" },
    });
    fireEvent.change(screen.getByPlaceholderText(/Position\/Role/i), {
      target: { value: "Engineer" },
    });

    fireEvent.click(screen.getByRole("button", { name: /Analyze/i }));

    expect(onAnalyze).toHaveBeenCalledWith("We need a React dev.", "Google", "Engineer");
  });

  it("shows loading state", () => {
    render(<JDInput onAnalyze={vi.fn()} isLoading={true} />);
    expect(screen.getByText(/Analyzing/i)).toBeDefined();
  });
});
