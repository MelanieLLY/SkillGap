import api from './auth';

// ── Nested response types (matching backend Pydantic models) ─────────────────

export interface TimelinePhase {
    phase: number;
    title: string;
    duration_weeks: number;
    start_week: number;
    end_week: number;
    focus_skills: string[];
    weekly_commitment_hours: number;
    milestones: string[];
}

export interface Course {
    title: string;
    platform: string;
    instructor: string;
    level: string;
    duration_hours: number;
    url: string;
    priority: string;
}

export interface SkillCourses {
    skill: string;
    courses: Course[];
}

export interface ProjectIdea {
    id: string;
    title: string;
    description: string;
    skills_practiced: string[];
    difficulty: string;
    estimated_hours: number;
    phase: number;
    deliverables: string[];
}

export interface RoadmapSummary {
    total_courses: number;
    total_projects: number;
    total_learning_hours: number;
    recommended_weekly_pace: string;
    completion_target: string;
}

export interface Roadmap {
    generated_for?: string | null;
    generated_at?: string | null;
    missing_skills: string[];
    total_estimated_duration_weeks: number;
    timeline: TimelinePhase[];
    course_recommendations: SkillCourses[];
    project_ideas: ProjectIdea[];
    summary: RoadmapSummary;
}

export interface RoadmapGenerateResponse {
    roadmap: Roadmap;
}

// ── Request type ─────────────────────────────────────────────────────────────

export interface RoadmapGenerateRequest {
    missing_skills: string[];
    jd_text?: string | null;
}

// ── API functions ────────────────────────────────────────────────────────────

export const roadmapApi = {
    generate: async (data: RoadmapGenerateRequest): Promise<RoadmapGenerateResponse> => {
        const response = await api.post<RoadmapGenerateResponse>(
            '/roadmap/generate',
            data
        );
        return response.data;
    },
};
