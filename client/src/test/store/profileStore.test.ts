import { describe, it, expect, vi, beforeEach } from "vitest";
import { useProfileStore } from "../../store/profileStore";
import * as profileApi from "../../api/profile";

// Mock the API
vi.mock("../../api/profile", () => ({
  getSkills: vi.fn(),
  addSkill: vi.fn(),
  removeSkill: vi.fn(),
  extractFromResume: vi.fn(),
}));

describe("useProfileStore", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Restricting zustand state between tests usually requires some setup,
    // but here we can just reset to initial values if needed.
    useProfileStore.setState({ skills: [], isLoading: false, error: null });
  });

  it("loadSkills handles success", async () => {
    const mockSkills = ["React", "TypeScript"];
    (profileApi.getSkills as any).mockResolvedValueOnce(mockSkills);

    await useProfileStore.getState().loadSkills();

    expect(useProfileStore.getState().skills).toEqual(mockSkills);
    expect(useProfileStore.getState().isLoading).toBe(false);
  });

  it("loadSkills handles error", async () => {
    (profileApi.getSkills as any).mockRejectedValueOnce({
      response: { data: { detail: "Load failed" } },
    });

    await useProfileStore.getState().loadSkills();

    expect(useProfileStore.getState().error).toBe("Load failed");
    expect(useProfileStore.getState().isLoading).toBe(false);
  });

  it("addSkill updates skills list", async () => {
    const mockSkills = ["Python"];
    (profileApi.addSkill as any).mockResolvedValueOnce(mockSkills);

    await useProfileStore.getState().addSkill("Python");

    expect(useProfileStore.getState().skills).toEqual(mockSkills);
    expect(profileApi.addSkill).toHaveBeenCalledWith("Python");
  });

  it("removeSkill updates skills list", async () => {
    const mockSkills = ["React"];
    (profileApi.removeSkill as any).mockResolvedValueOnce(mockSkills);

    await useProfileStore.getState().removeSkill("TypeScript");

    expect(useProfileStore.getState().skills).toEqual(mockSkills);
    expect(profileApi.removeSkill).toHaveBeenCalledWith("TypeScript");
  });

  it("extractFromResume updates skills list", async () => {
    const mockSkills = ["AI", "ML"];
    (profileApi.extractFromResume as any).mockResolvedValueOnce(mockSkills);

    await useProfileStore.getState().extractFromResume("Resume text here");

    expect(useProfileStore.getState().skills).toEqual(mockSkills);
    expect(profileApi.extractFromResume).toHaveBeenCalledWith("Resume text here");
  });
});
