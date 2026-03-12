import React from "react";
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import AnimatedMatchRing from "../../components/AnimatedMatchRing";

describe("AnimatedMatchRing", () => {
  describe("Normal (non-waiting) state", () => {
    it("renders the match label", () => {
      render(<AnimatedMatchRing matchScore={75} />);
      expect(screen.getByText(/match/i)).toBeInTheDocument();
    });

    it("renders 'Match' label when not waiting", () => {
      render(<AnimatedMatchRing matchScore={80} />);
      expect(screen.getByText("Match")).toBeInTheDocument();
    });

    it("does not render dash when isWaiting is false", () => {
      render(<AnimatedMatchRing matchScore={50} isWaiting={false} />);
      expect(screen.queryByText("—")).not.toBeInTheDocument();
    });
  });

  describe("Waiting state (isWaiting=true)", () => {
    it("renders em-dash instead of score when waiting", () => {
      render(<AnimatedMatchRing matchScore={0} isWaiting={true} />);
      expect(screen.getByText("—")).toBeInTheDocument();
    });

    it("renders 'Pending' label when isWaiting is true", () => {
      render(<AnimatedMatchRing matchScore={0} isWaiting={true} />);
      expect(screen.getByText("Pending")).toBeInTheDocument();
    });

    it("does not render 'Match' label when waiting", () => {
      render(<AnimatedMatchRing matchScore={0} isWaiting={true} />);
      expect(screen.queryByText("Match")).not.toBeInTheDocument();
    });
  });

  describe("Ring color logic (getRingColor)", () => {
    it("renders SVG ring element", () => {
      const { container } = render(<AnimatedMatchRing matchScore={80} />);
      const svg = container.querySelector("svg");
      expect(svg).toBeInTheDocument();
    });

    it("renders two circles (background + progress)", () => {
      const { container } = render(<AnimatedMatchRing matchScore={60} />);
      const circles = container.querySelectorAll("circle");
      expect(circles.length).toBeGreaterThanOrEqual(2);
    });
  });

  describe("Score boundary cases", () => {
    it("renders without crashing at score=0", () => {
      expect(() => render(<AnimatedMatchRing matchScore={0} />)).not.toThrow();
    });

    it("renders without crashing at score=100", () => {
      expect(() => render(<AnimatedMatchRing matchScore={100} />)).not.toThrow();
    });

    it("uses default isWaiting=false when omitted", () => {
      render(<AnimatedMatchRing matchScore={42} />);
      // 'Pending' should not appear if isWaiting defaults to false
      expect(screen.queryByText("Pending")).not.toBeInTheDocument();
    });
  });
});
