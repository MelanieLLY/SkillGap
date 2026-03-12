import api from "./auth";

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return {
    headers: { Authorization: `Bearer ${token}` },
  };
};

export const getSkills = async (): Promise<string[]> => {
  const response = await api.get("/profile/skills", getAuthHeaders());
  return response.data;
};

export const addSkill = async (skill: string): Promise<string[]> => {
  const response = await api.post("/profile/skills", { skill }, getAuthHeaders());
  return response.data;
};

export const removeSkill = async (skillName: string): Promise<string[]> => {
  const response = await api.delete(
    `/profile/skills/${encodeURIComponent(skillName)}`,
    getAuthHeaders(),
  );
  return response.data;
};

export const extractFromResume = async (resumeText: string): Promise<string[]> => {
  const response = await api.post(
    "/profile/extract-resume",
    { resume_text: resumeText },
    getAuthHeaders(),
  );
  return response.data;
};
