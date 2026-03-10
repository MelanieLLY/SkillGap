import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import { historyApi, HistoryRecord } from '../api/history';

export default function History() {
    const [history, setHistory] = useState<HistoryRecord[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        try {
            const data = await historyApi.getHistory();
            setHistory(data);
        } catch (err) {
            console.error("Failed to load history", err);
            setError("Failed to load history. Please try again later.");
        } finally {
            setIsLoading(false);
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="min-h-screen flex flex-col bg-[#0f1117]">
            <Navbar />

            <main className="flex-grow p-6 max-w-[1440px] mx-auto w-full">
                <div className="mb-6">
                    <h1 className="text-2xl font-bold text-white">Analysis History</h1>
                    <p className="text-[#9aa0ac] mt-1">Review your past job description match scores.</p>
                </div>

                {error && (
                    <div className="mb-6 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
                        <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {error}
                    </div>
                )}

                {isLoading ? (
                    <div className="flex justify-center py-12">
                        <div className="w-8 h-8 border-2 border-[#38e5b1] border-t-transparent rounded-full animate-spin"></div>
                    </div>
                ) : history.length === 0 ? (
                    <div className="glass-card-accent p-12 flex flex-col items-center justify-center text-center border border-white/5 rounded-2xl">
                        <div className="w-16 h-16 rounded-full bg-[#1e2433] flex items-center justify-center border border-white/10 mb-4">
                            <svg className="w-8 h-8 text-[#5f6573]" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="text-lg font-semibold text-white mb-2">No History Yet</h3>
                        <p className="text-[#9aa0ac] max-w-sm">
                            Analyze a job description on the dashboard to start saving your match history.
                        </p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {history.map((record) => (
                            <div key={record.id} className="glass-card-accent p-6 flex flex-col rounded-2xl border border-white/5 hover:border-[#38e5b1]/30 transition-colors">
                                <div className="flex justify-between items-start mb-4">
                                    <div>
                                        <h3 className="text-lg font-bold text-white leading-tight">
                                            {record.position_name || 'Unknown Role'}
                                        </h3>
                                        <p className="text-[#38e5b1] text-sm font-medium mt-1">
                                            {record.company_name || 'Unknown Company'}
                                        </p>
                                    </div>
                                    <div className={`shrink-0 flex items-center justify-center w-12 h-12 rounded-full border-2 ${record.match_score >= 70 ? 'border-green-500/50 text-green-400 bg-green-500/10' :
                                            record.match_score >= 40 ? 'border-yellow-500/50 text-yellow-400 bg-yellow-500/10' :
                                                'border-red-500/50 text-red-400 bg-red-500/10'
                                        }`}>
                                        <span className="text-sm font-bold">{Math.round(record.match_score)}%</span>
                                    </div>
                                </div>

                                <div className="text-xs text-[#5f6573] mb-4 flex items-center gap-1.5">
                                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                    </svg>
                                    {formatDate(record.date_analyzed)}
                                </div>

                                <div className="mt-auto space-y-3 border-t border-white/5 pt-4">
                                    <div className="flex justify-between text-sm">
                                        <span className="text-[#9aa0ac]">Existing</span>
                                        <span className="text-white font-medium">{record.have_skills.length}</span>
                                    </div>
                                    <div className="flex justify-between text-sm">
                                        <span className="text-[#9aa0ac]">Missing</span>
                                        <span className="text-white font-medium">{record.missing_skills.length}</span>
                                    </div>
                                    <div className="flex justify-between text-sm">
                                        <span className="text-[#9aa0ac]">Bonus</span>
                                        <span className="text-white font-medium">{record.bonus_skills.length}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
