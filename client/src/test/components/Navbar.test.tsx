import React from "react";
import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, it, expect, beforeEach } from "vitest";
import Navbar from "../../components/Navbar";
import { useAuthStore } from "../../store/authStore";
import { useProfileStore } from "../../store/profileStore";

describe("Navbar Component", () => {
  beforeEach(() => {
    useAuthStore.setState({ 
      user: { 
        id: 1, 
        email: "test@example.com", 
        is_active: true, 
        skills: ["React"],
        roadmap: null 
      } 
    });
    useProfileStore.setState({ skills: ["React"] });
  });

  it("renders logo and links", () => {
    render(
      <BrowserRouter>
        <Navbar />
      </BrowserRouter>
    );

    expect(screen.getByText("SkillGap")).toBeDefined();
    expect(screen.getByText("Dashboard")).toBeDefined();
    expect(screen.getByText("History")).toBeDefined();
    expect(screen.getByText("1 Skills")).toBeDefined();
  });
});
