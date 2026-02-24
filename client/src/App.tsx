import { useState } from 'react'
import axios from 'axios'
import Navbar from './components/Navbar'
import JDInput from './components/JDInput'
import SkillMatchResults from './components/SkillMatchResults'
import LearningRoadmap from './components/LearningRoadmap'

// TODO(#2): Replace with real user profile skills from the database
const MOCK_USER_SKILLS = [
    'python', 'react', 'typescript', 'javascript', 'html', 'css',
    'tailwind', 'git', 'sql', 'node.js'
];

interface SkillResults {
    have: string[];
    missing: string[];
    bonus: string[];
}

function App() {
    const [results, setResults] = useState<SkillResults | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleAnalyze = async (jobDescription: string) => {
        setIsLoading(true);
        setError(null);

        try {
            const response = await axios.post<SkillResults>(
                'http://localhost:8000/api/extract',
                {
                    job_description: jobDescription,
                    user_skills: MOCK_USER_SKILLS,
                }
            );
            setResults(response.data);
        } catch (err) {
            console.error('Extraction failed:', err);
            setError('Failed to analyze the job description. Please ensure the backend server is running.');
        } finally {
            setIsLoading(false);
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
                    {/* Left Column — JD Input */}
                    <JDInput onAnalyze={handleAnalyze} isLoading={isLoading} />

                    {/* Right Column — Results + Roadmap */}
                    <div className="flex flex-col gap-6">
                        <SkillMatchResults skills={results} />
                        <LearningRoadmap />
                    </div>
                </div>
            </main>
        </div>
    )
}

export default App
