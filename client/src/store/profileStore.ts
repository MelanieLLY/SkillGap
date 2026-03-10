import { create } from 'zustand';
import { getSkills as fetchSkills, addSkill as apiAddSkill, removeSkill as apiRemoveSkill, extractFromResume as apiExtract } from '../api/profile';

interface ProfileState {
    skills: string[];
    isLoading: boolean;
    error: string | null;
    loadSkills: () => Promise<void>;
    addSkill: (skill: string) => Promise<void>;
    removeSkill: (skillName: string) => Promise<void>;
    extractFromResume: (resumeText: string) => Promise<void>;
}

export const useProfileStore = create<ProfileState>((set) => ({
    skills: [],
    isLoading: false,
    error: null,

    loadSkills: async () => {
        set({ isLoading: true, error: null });
        try {
            const skills = await fetchSkills();
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error?.response?.data?.detail || 'Failed to load skills', isLoading: false });
        }
    },

    addSkill: async (skill: string) => {
        set({ isLoading: true, error: null });
        try {
            const skills = await apiAddSkill(skill);
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error?.response?.data?.detail || 'Failed to add skill', isLoading: false });
        }
    },

    removeSkill: async (skillName: string) => {
        set({ isLoading: true, error: null });
        try {
            const skills = await apiRemoveSkill(skillName);
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error?.response?.data?.detail || 'Failed to remove skill', isLoading: false });
        }
    },

    extractFromResume: async (resumeText: string) => {
        set({ isLoading: true, error: null });
        try {
            const skills = await apiExtract(resumeText);
            set({ skills, isLoading: false });
        } catch (error: any) {
            set({ error: error?.response?.data?.detail || 'Failed to extract skills', isLoading: false });
        }
    }
}));
