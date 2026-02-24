import React, { useState } from 'react';

interface JDInputProps {
    onAnalyze: (text: string) => void;
    isLoading: boolean;
}

const JDInput: React.FC<JDInputProps> = ({ onAnalyze, isLoading }) => {
    const [text, setText] = useState('');

    const handleSubmit = () => {
        if (text.trim().length === 0) return;
        onAnalyze(text.trim());
    };

    return (
        <div className="glass-card-accent p-6 flex flex-col h-full">
            {/* Section Header */}
            <div className="flex items-center gap-2 mb-4">
                <svg className="w-4 h-4 text-[#38e5b1]" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                <h2 className="text-lg font-semibold text-white">Job Description</h2>
            </div>

            {/* Textarea */}
            <textarea
                id="jd-input-textarea"
                className="jd-textarea w-full flex-grow p-4 text-sm leading-relaxed min-h-[320px]"
                placeholder="Paste Job Description Here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                disabled={isLoading}
            />

            {/* Analyze Button */}
            <button
                id="analyze-button"
                className="btn-glow w-full mt-5 py-3.5 text-base flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={handleSubmit}
                disabled={isLoading || text.trim().length === 0}
            >
                {isLoading ? (
                    <>
                        <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                        </svg>
                        Analyzing...
                    </>
                ) : (
                    <>
                        Analyze
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 5l7 7-7 7" />
                        </svg>
                    </>
                )}
            </button>
        </div>
    );
};

export default JDInput;
