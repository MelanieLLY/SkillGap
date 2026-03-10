import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useProfileStore } from '../store/profileStore';

const Profile: React.FC = () => {
    const { logout } = useAuthStore();
    const { skills, isLoading, error, fetchSkills, addSkill, removeSkill, extractFromResume } = useProfileStore();
    const navigate = useNavigate();

    const [newSkill, setNewSkill] = useState('');
    const [resumeText, setResumeText] = useState('');

    useEffect(() => {
        fetchSkills();
    }, [fetchSkills]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const handleAddSkill = async (e: React.FormEvent) => {
        e.preventDefault();
        if (newSkill.trim()) {
            await addSkill(newSkill.trim());
            setNewSkill('');
        }
    };

    const handleExtractResume = async () => {
        if (resumeText.trim()) {
            await extractFromResume(resumeText.trim());
            setResumeText('');
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            {/* Navigation Bar */}
            <nav className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <div className="flex-shrink-0 flex items-center cursor-pointer" onClick={() => navigate('/')}>
                            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
                                SkillGap
                            </span>
                        </div>
                        <div className="flex items-center space-x-4">
                            <button
                                onClick={() => navigate('/profile')}
                                className="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                disabled={isLoading}
                            >
                                My Profile
                            </button>
                            <button
                                onClick={handleLogout}
                                className="text-gray-600 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                                title="Logout"
                                disabled={isLoading}
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="bg-white shadow rounded-lg p-6 sm:p-8">
                    <h1 className="text-2xl font-bold text-gray-900 mb-6">My Skills Profile</h1>

                    {error && (
                        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
                            <span className="block sm:inline">{error}</span>
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        {/* Left Column: Input Methods */}
                        <div className="space-y-6">
                            {/* Manual Entry */}
                            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                <h2 className="text-lg font-semibold text-gray-800 mb-3">Add Skill Manually</h2>
                                <form onSubmit={handleAddSkill} className="flex gap-2">
                                    <input
                                        type="text"
                                        value={newSkill}
                                        onChange={(e) => setNewSkill(e.target.value)}
                                        placeholder="e.g. React, Python"
                                        className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 px-4 py-2 border"
                                        disabled={isLoading}
                                    />
                                    <button
                                        type="submit"
                                        disabled={isLoading || !newSkill.trim()}
                                        className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                                    >
                                        Add
                                    </button>
                                </form>
                            </div>

                            {/* Resume Extraction */}
                            <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                                <h2 className="text-lg font-semibold text-gray-800 mb-3">Extract from Resume</h2>
                                <textarea
                                    value={resumeText}
                                    onChange={(e) => setResumeText(e.target.value)}
                                    placeholder="Paste your resume text here to automatically extract your skills..."
                                    rows={6}
                                    className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 p-3 border mb-3 resize-none"
                                    disabled={isLoading}
                                />
                                <button
                                    onClick={handleExtractResume}
                                    disabled={isLoading || !resumeText.trim()}
                                    className="w-full inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                                >
                                    {isLoading ? 'Extracting...' : 'Extract Skills'}
                                </button>
                            </div>
                        </div>

                        {/* Right Column: Display Skills */}
                        <div className="bg-white border border-gray-200 rounded-lg p-6 flex flex-col h-full">
                            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center justify-between">
                                <span>Your Saved Skills</span>
                                <span className="text-sm font-normal text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{skills.length} Total</span>
                            </h2>

                            <div className="flex-1 bg-gray-50 border border-gray-100 rounded p-4 min-h-[300px]">
                                {isLoading && skills.length === 0 ? (
                                    <div className="flex items-center justify-center h-full text-gray-400">Loading skills...</div>
                                ) : skills.length === 0 ? (
                                    <div className="flex flex-col items-center justify-center h-full text-gray-500 text-center">
                                        <p>No skills added yet.</p>
                                        <p className="text-sm mt-1">Add them manually or extract from your resume.</p>
                                    </div>
                                ) : (
                                    <div className="flex flex-wrap gap-2">
                                        {skills.map((skill, index) => (
                                            <span
                                                key={index}
                                                className="inline-flex items-center py-1.5 px-3 rounded-full text-sm font-medium bg-blue-100 text-blue-800 border border-blue-200 shadow-sm transition-transform hover:scale-105 group"
                                            >
                                                {skill}
                                                <button
                                                    type="button"
                                                    onClick={() => removeSkill(skill)}
                                                    className="ml-2 flex-shrink-0 inline-flex items-center justify-center h-4 w-4 rounded-full text-blue-400 hover:bg-blue-200 hover:text-blue-900 focus:outline-none focus:bg-blue-500 focus:text-white transition-colors"
                                                    aria-label={`Remove ${skill}`}
                                                    disabled={isLoading}
                                                >
                                                    <svg className="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
                                                        <path strokeLinecap="round" strokeWidth="1.5" d="M1 1l6 6m0-6L1 7" />
                                                    </svg>
                                                </button>
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Profile;
