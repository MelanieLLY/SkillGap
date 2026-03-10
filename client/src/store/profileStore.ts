import { create } from 'zustand';
import { profileApi } from '../api/profile';

interface ProfileState {
    skills: string[];
    isLoading: boolean;
    error: string | null;
    fetchSkills: () => Promise<void>;
    addSkill: (skill: string) => Promise<void>;
    removeSkill: (skill: string) => Promise<void>;
    extractFromResume: (resumeText: string) => Promise<void>;
}

export const useProfileStore = create<ProfileState>((set) => ({
    skills: [],
    isLoading: false,
    error: null,

    fetchSkills: async () => {
        set({ isLoading: true, error: null });
        try {
            const skills = await profileApi.getSkills();
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error.response?.data?.detail || 'Failed to fetch skills', isLoading: false });
        }
    },

    addSkill: async (skill: string) => {
        set({ isLoading: true, error: null });
        try {
            const skills = await profileApi.addSkill(skill);
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error.response?.data?.detail || 'Failed to add skill', isLoading: false });
        }
    },

    removeSkill: async (skill: string) => {
        set({ isLoading: true, error: null });
        try {
            const skills = await profileApi.removeSkill(skill);
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error.response?.data?.detail || 'Failed to remove skill', isLoading: false });
        }
    },

    extractFromResume: async (resumeText: string) => {
        set({ isLoading: true, error: null });
        try {
            const skills = await profileApi.extractFromResume(resumeText);
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error.response?.data?.detail || 'Failed to extract skills', isLoading: false });
        }
    },
}));
