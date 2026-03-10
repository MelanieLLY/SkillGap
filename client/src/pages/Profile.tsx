import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { useAuthStore } from '../store/authStore';
import { useProfileStore } from '../store/profileStore';

const Profile: React.FC = () => {
    const user = useAuthStore((state) => state.user);
    const {
        skills,
        isLoading,
        error,
        loadSkills,
        addSkill,
        removeSkill,
        extractFromResume
    } = useProfileStore();

    const [skillInput, setSkillInput] = useState('');
    const [resumeText, setResumeText] = useState('');

    useEffect(() => {
        if (user) {
            loadSkills();
        }
    }, [user, loadSkills]);

    const handleAddSkill = async (e: React.FormEvent) => {
        e.preventDefault();
        if (skillInput.trim()) {
            await addSkill(skillInput.trim());
            setSkillInput('');
        }
    };

    const handleExtract = async () => {
        if (resumeText.trim()) {
            await extractFromResume(resumeText.trim());
            setResumeText('');
        }
    };

    return (
        <div className="min-h-screen bg-[#0f1117] flex flex-col font-sans">
            <Navbar />
            <main className="flex-1 w-full max-w-6xl mx-auto p-6 md:p-8 flex flex-col gap-8">
                {/* Header */}
                <div className="flex flex-col gap-2">
                    <h1 className="text-3xl font-bold text-white tracking-tight">
                        Skill Profile Setup
                    </h1>
                    <p className="text-[#9aa0ac] text-lg max-w-2xl text-balance">
                        Define your expertise. Add your skills manually or paste your resume and let our engine extract them for you.
                    </p>
                </div>

                {error && (
                    <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-xl flex items-center gap-3">
                        <svg className="w-5 h-5 text-red-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-sm text-red-400 font-medium">{error}</p>
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left Column: Manual Add + Current Skills */}
                    <div className="flex flex-col gap-6">
                        <div className="p-6 rounded-2xl bg-[#161a25] border border-white/5 flex flex-col gap-5">
                            <h2 className="text-xl font-semibold text-white">Your Skills</h2>
                            <form onSubmit={handleAddSkill} className="flex gap-3">
                                <input
                                    type="text"
                                    value={skillInput}
                                    onChange={(e) => setSkillInput(e.target.value)}
                                    placeholder="e.g. React, Python, AWS..."
                                    className="flex-1 bg-[#1c2130] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-[#6b7280] focus:outline-none focus:ring-2 focus:ring-[#38e5b1] focus:border-transparent transition-all"
                                    disabled={isLoading}
                                />
                                <button
                                    type="submit"
                                    disabled={isLoading || !skillInput}
                                    className="px-6 py-3 rounded-xl bg-gradient-to-r from-[#38e5b1] to-[#22c55e] text-[#0f1117] font-semibold hover:shadow-lg hover:shadow-[#38e5b1]/20 transition-all active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-[#38e5b1] disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Add
                                </button>
                            </form>

                            <div className="flex flex-wrap gap-2 mt-2">
                                {isLoading && skills.length === 0 ? (
                                    <div className="text-[#9aa0ac] text-sm flex items-center gap-2">
                                        <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                        Loading skills...
                                    </div>
                                ) : skills.length === 0 ? (
                                    <p className="text-[#9aa0ac] text-sm">No skills added yet. Add some to get started!</p>
                                ) : (
                                    skills.map((skill, i) => (
                                        <div
                                            key={`${skill}-${i}`}
                                            className="group flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[#1c2130] border border-white/10 text-white text-sm hover:border-white/20 transition-colors"
                                        >
                                            <span>{skill}</span>
                                            <button
                                                onClick={() => removeSkill(skill)}
                                                className="text-[#6b7280] hover:text-red-400 transition-colors focus:outline-none"
                                                disabled={isLoading}
                                                aria-label={`Remove ${skill}`}
                                            >
                                                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                                </svg>
                                            </button>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Resume Pasting */}
                    <div className="flex flex-col gap-6">
                        <div className="p-6 rounded-2xl bg-[#161a25] border border-white/5 flex flex-col gap-5 h-full">
                            <h2 className="text-xl font-semibold text-white">Auto-Extract from Resume</h2>
                            <p className="text-[#9aa0ac] text-sm">
                                Paste the text from your resume or LinkedIn profile, and we'll automatically detect your technical skills.
                            </p>
                            <textarea
                                value={resumeText}
                                onChange={(e) => setResumeText(e.target.value)}
                                placeholder="Paste your resume text here..."
                                className="flex-1 min-h-[200px] bg-[#1c2130] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-[#6b7280] focus:outline-none focus:ring-2 focus:ring-[#38e5b1] focus:border-transparent transition-all resize-none"
                                disabled={isLoading}
                            />
                            <button
                                onClick={handleExtract}
                                disabled={isLoading || !resumeText}
                                className="w-full py-3 rounded-xl bg-[#1c2130] hover:bg-[#252a3b] border border-white/10 hover:border-white/20 text-white font-medium transition-all active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-[#38e5b1] disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
                            >
                                {isLoading ? (
                                    <>
                                        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                        Extracting...
                                    </>
                                ) : (
                                    <>
                                        <svg className="w-5 h-5 text-[#38e5b1]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                                        </svg>
                                        Extract Skills
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Profile;
