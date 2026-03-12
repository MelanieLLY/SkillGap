import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return {
    headers: { Authorization: `Bearer ${token}` },
  };
};

export const getSkills = async (): Promise<string[]> => {
  const response = await axios.get(`${API_URL}/profile/skills`, getAuthHeaders());
  return response.data;
};

export const addSkill = async (skill: string): Promise<string[]> => {
  const response = await axios.post(`${API_URL}/profile/skills`, { skill }, getAuthHeaders());
  return response.data;
};

export const removeSkill = async (skillName: string): Promise<string[]> => {
  const response = await axios.delete(
    `${API_URL}/profile/skills/${encodeURIComponent(skillName)}`,
    getAuthHeaders(),
  );
  return response.data;
};

export const extractFromResume = async (resumeText: string): Promise<string[]> => {
  const response = await axios.post(
    `${API_URL}/profile/extract-resume`,
    { resume_text: resumeText },
    getAuthHeaders(),
  );
  return response.data;
};
