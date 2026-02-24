import React, { useState } from 'react';
import SkillMatchResult from './components/SkillMatchResult';

function App() {
    const [jobDescription, setJobDescription] = useState('');
    const [userSkillsInput, setUserSkillsInput] = useState('');
    const [matchResult, setMatchResult] = useState<{
        have: string[];
        missing: string[];
        bonus: string[];
    } | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleMatch = async () => {
        setLoading(true);
        setError('');
        try {
            const userSkills = userSkillsInput.split(',').map(s => s.trim()).filter(s => s !== '');
            const response = await fetch('http://localhost:8000/api/match', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    job_description: jobDescription,
                    user_skills: userSkills,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch from backend. Make sure the backend server is running on localhost:8000');
            }

            const data = await response.json();
            setMatchResult(data.matchResult);
        } catch (err: any) {
            setError(err.message || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            padding: "2rem",
            backgroundColor: "#f3f4f6",
            minHeight: "100vh",
            fontFamily: "system-ui, sans-serif"
        }}>
            <div style={{ maxWidth: "800px", margin: "0 auto" }}>
                <h1 style={{ textAlign: 'center', color: '#111827', marginBottom: '2rem' }}>SkillGap Extractor</h1>

                <div style={{
                    backgroundColor: 'white',
                    padding: '2rem',
                    borderRadius: '12px',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.05)',
                    marginBottom: '2rem'
                }}>
                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Job Description</label>
                        <textarea
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                            placeholder="Paste the job description here..."
                            style={{
                                width: '100%',
                                height: '150px',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid #d1d5db',
                                fontSize: '14px'
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 600 }}>Your Skills (comma separated)</label>
                        <input
                            type="text"
                            value={userSkillsInput}
                            onChange={(e) => setUserSkillsInput(e.target.value)}
                            placeholder="e.g. Python, SQL, Git"
                            style={{
                                width: '100%',
                                padding: '12px',
                                borderRadius: '8px',
                                border: '1px solid #d1d5db',
                                fontSize: '14px'
                            }}
                        />
                    </div>

                    <button
                        onClick={handleMatch}
                        disabled={loading}
                        style={{
                            width: '100%',
                            padding: '12px',
                            backgroundColor: '#4f46e5',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            fontSize: '16px',
                            fontWeight: 600,
                            cursor: loading ? 'not-allowed' : 'pointer'
                        }}
                    >
                        {loading ? 'Analyzing...' : 'Match Skills'}
                    </button>

                    {error && (
                        <p style={{ color: '#ef4444', marginTop: '1rem', textAlign: 'center' }}>{error}</p>
                    )}
                </div>

                {matchResult && <SkillMatchResult matchResult={matchResult} />}
            </div>
        </div>
    );
}

export default App;
