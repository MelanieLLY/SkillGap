import React from "react";
import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Skeleton from "../../components/Skeleton";

describe("Skeleton", () => {
  it("renders with aria-hidden for screen readers", () => {
    const { container } = render(<Skeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el).toHaveAttribute("aria-hidden", "true");
  });

  it("applies default base classes", () => {
    const { container } = render(<Skeleton />);
    const el = container.firstChild as HTMLElement;
    expect(el).toHaveClass("relative", "overflow-hidden", "rounded-lg");
  });

  it("merges custom className with base classes", () => {
    const { container } = render(<Skeleton className="h-10 w-32" />);
    const el = container.firstChild as HTMLElement;
    expect(el).toHaveClass("h-10", "w-32");
    // Should still have base classes
    expect(el).toHaveClass("relative", "overflow-hidden");
  });

  it("renders the shimmer overlay child element", () => {
    const { container } = render(<Skeleton />);
    // The shimmer is the only child div inside the wrapper
    const shimmer = container.querySelector(".absolute");
    expect(shimmer).toBeInTheDocument();
  });

  it("renders without crashing when no props are passed", () => {
    expect(() => render(<Skeleton />)).not.toThrow();
  });
});
