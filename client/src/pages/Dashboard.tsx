import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { historyApi } from '../api/history';
import { useProfileStore } from '../store/profileStore';
import { useAuthStore } from '../store/authStore';
import Navbar from '../components/Navbar';
import JDInput from '../components/JDInput';
import SkillMatchResults from '../components/SkillMatchResults';
import LearningRoadmap from '../components/LearningRoadmap';
import UserSkillsInput from '../components/UserSkillsInput';

interface SkillResults {
    have: string[];
    missing: string[];
    bonus: string[];
    company_name?: string | null;
    position_name?: string | null;
}

export default function Dashboard() {
    const user = useAuthStore((state) => state.user);
    const {
        skills: userSkills,
        isLoading: isLoadingSkills,
        loadSkills,
        addSkill,
        removeSkill
    } = useProfileStore();

    useEffect(() => {
        if (user) {
            loadSkills();
        }
    }, [user, loadSkills]);

    const handleSkillsChange = async (newSkills: string[]) => {
        // Find added skill
        const added = newSkills.find(s => !userSkills.includes(s));
        if (added) {
            await addSkill(added);
        }

        // Find removed skill
        const removed = userSkills.find(s => !newSkills.includes(s));
        if (removed) {
            await removeSkill(removed);
        }
    };

    const [results, setResults] = useState<SkillResults | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [historyId, setHistoryId] = useState<number | null>(null);
    const saveTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);

    const handleAnalyze = async (jobDescription: string) => {
        setIsLoading(true);
        setError(null);
        setHistoryId(null);

        try {
            const response = await axios.post<SkillResults>(
                'http://localhost:8000/api/extract',
                {
                    job_description: jobDescription,
                    user_skills: userSkills,
                }
            );
            setResults(response.data);

            // Auto-save history
            const have = response.data.have || [];
            const missing = response.data.missing || [];
            const totalRequired = have.length + missing.length;
            const matchScore = totalRequired > 0 ? (have.length / totalRequired) * 100 : 0;

            try {
                const historyRecord = await historyApi.createHistory({
                    company_name: response.data.company_name,
                    position_name: response.data.position_name,
                    match_score: matchScore,
                    have_skills: response.data.have,
                    missing_skills: response.data.missing,
                    bonus_skills: response.data.bonus,
                });
                setHistoryId(historyRecord.id);
            } catch (historyErr) {
                console.error("Failed to auto-save history:", historyErr);
                // We don't block the UI for a failed save right now
            }
        } catch (err) {
            console.error('Extraction failed:', err);
            setError('Failed to analyze the job description. Please ensure the backend server is running.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleUpdateHistory = (updates: Partial<SkillResults>) => {
        if (!results) return;

        // Optimistic UI update
        const updatedResults = { ...results, ...updates };
        setResults(updatedResults);

        // Debounce actual save
        if (historyId) {
            if (saveTimeout.current) clearTimeout(saveTimeout.current);
            saveTimeout.current = setTimeout(async () => {
                try {
                    await historyApi.updateHistory(historyId, {
                        company_name: updatedResults.company_name,
                        position_name: updatedResults.position_name,
                    });
                } catch (err) {
                    console.error("Failed to update history record", err);
                }
            }, 1000);
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-[#0f1117]">
            <Navbar />

            <main className="flex-grow p-6 max-w-[1440px] mx-auto w-full">
                {/* Error Banner */}
                {error && (
                    <div className="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
                        <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {error}
                    </div>
                )}

                {/* Two-Column Dashboard Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-[380px_1fr] gap-6 items-start">
                    {/* Left Column — User Skills + JD Input */}
                    <div className="flex flex-col gap-6">
                        <UserSkillsInput
                            skills={userSkills}
                            onSkillsChange={handleSkillsChange}
                        />
                        <JDInput onAnalyze={handleAnalyze} isLoading={isLoading || isLoadingSkills} />
                    </div>

                    {/* Right Column — Results + Roadmap */}
                    <div className="flex flex-col gap-6">
                        <SkillMatchResults
                            skills={results}
                            onCompanyChange={(val) => handleUpdateHistory({ company_name: val })}
                            onPositionChange={(val) => handleUpdateHistory({ position_name: val })}
                        />
                        <LearningRoadmap />
                    </div>
                </div>
            </main>
        </div>
    );
}
