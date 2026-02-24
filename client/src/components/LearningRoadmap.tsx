import React from 'react';

const PLACEHOLDER_STEPS = [
    { step: 1, title: 'Foundations', description: 'Core Concepts' },
    { step: 2, title: 'Cloud Services', description: 'AWS & Docker' },
    { step: 3, title: 'Containers', description: 'Kubernetes Training' },
    { step: 4, title: 'DevOps Tools', description: 'Terraform & CI/CD' },
    { step: 5, title: 'Advanced Skills', description: 'Node.js & GraphQL' },
];

const LearningRoadmap: React.FC = () => {
    return (
        <div className="glass-card-accent p-6">
            {/* Section Header */}
            <div className="flex items-center gap-2 mb-5">
                <svg className="w-4 h-4 text-[#38e5b1]" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                <h2 className="text-lg font-semibold text-white">Learning Roadmap</h2>
                <span className="ml-2 text-xs text-[#5f6573] italic">(AI-powered — coming in Sprint 2)</span>
            </div>

            {/* Timeline */}
            <div className="relative">
                {/* Vertical connector line */}
                <div className="absolute left-[18px] top-3 bottom-3 w-0.5 bg-gradient-to-b from-[#38e5b1] via-[#22c55e] to-[#5f6573]" />

                <div className="space-y-3">
                    {PLACEHOLDER_STEPS.map(({ step, title, description }) => (
                        <div key={step} className="relative flex items-center gap-4 group">
                            {/* Number circle */}
                            <div className="z-10 w-9 h-9 rounded-full bg-[#1a1f2e] border-2 border-[#38e5b1]/40 flex items-center justify-center flex-shrink-0 group-hover:border-[#38e5b1] transition-colors">
                                <span className="text-xs font-bold text-[#38e5b1]">{step}</span>
                            </div>

                            {/* Step card */}
                            <div className="flex-grow flex items-center justify-between bg-[#1a1f2e] hover:bg-[#1f2538] border border-white/5 rounded-xl px-5 py-3.5 transition-all cursor-default group-hover:border-[#38e5b1]/20">
                                <div className="flex items-center gap-3">
                                    <span className="text-xs text-[#5f6573] font-medium uppercase tracking-wider">
                                        Step {step}
                                    </span>
                                    <span className="text-sm font-bold text-white">{title}</span>
                                    <span className="text-xs text-[#9aa0ac]">+ {description}</span>
                                </div>

                                {/* Progress bar placeholder */}
                                <div className="flex items-center gap-2">
                                    <div className="flex gap-0.5">
                                        {Array.from({ length: 5 }).map((_, i) => (
                                            <div
                                                key={i}
                                                className={`w-3 h-2 rounded-sm ${i < (5 - step + 1)
                                                        ? 'bg-gradient-to-r from-[#38e5b1] to-[#22c55e]'
                                                        : 'bg-[#2a2f3e]'
                                                    }`}
                                            />
                                        ))}
                                    </div>
                                    <svg className="w-4 h-4 text-[#5f6573] group-hover:text-[#38e5b1] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default LearningRoadmap;
