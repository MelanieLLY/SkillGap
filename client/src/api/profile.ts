import api from './axios';

export const profileApi = {
    getSkills: async () => {
        const response = await api.get<string[]>('/profile/skills');
        return response.data;
    },

    addSkill: async (skill: string) => {
        const response = await api.post<string[]>('/profile/skills', { skill });
        return response.data;
    },

    removeSkill: async (skill: string) => {
        const response = await api.delete<string[]>(`/profile/skills/${encodeURIComponent(skill)}`);
        return response.data;
    },

    extractFromResume: async (resumeText: string) => {
        const response = await api.post<string[]>('/profile/extract-resume', { resume_text: resumeText });
        return response.data;
    },
};
