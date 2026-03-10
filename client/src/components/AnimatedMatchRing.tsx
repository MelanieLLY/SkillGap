import React, { useEffect, useState } from 'react';

export interface AnimatedMatchRingProps {
    matchScore: number;
    isWaiting?: boolean;
}

const AnimatedMatchRing: React.FC<AnimatedMatchRingProps> = ({ matchScore, isWaiting = false }) => {
    const [displayScore, setDisplayScore] = useState(0);
    const [isAnimating, setIsAnimating] = useState(false);

    useEffect(() => {
        if (isWaiting) {
            setDisplayScore(0);
            setIsAnimating(false);
            return;
        }

        const timer = setTimeout(() => {
            setIsAnimating(true);

            let startTimestamp: number | null = null;
            const duration = 1000;
            const step = (timestamp: number) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const easeProgress = 1 - Math.pow(1 - progress, 4);
                setDisplayScore(Math.round(easeProgress * matchScore));

                if (progress < 1) {
                    window.requestAnimationFrame(step);
                }
            };
            window.requestAnimationFrame(step);
        }, 50);

        return () => clearTimeout(timer);
    }, [matchScore, isWaiting]);

    // Ring geometry
    const radius = 62;
    const circumference = 2 * Math.PI * radius;
    const targetOffset = circumference - (matchScore / 100) * circumference;

    // Color calculation based on actual matchScore
    const getRingColor = (score: number, waiting: boolean): string => {
        if (waiting) return '#38e5b1';
        if (score >= 70) return '#38e5b1';
        if (score >= 40) return '#eab308';
        return '#ef4444';
    };

    const ringColor = getRingColor(matchScore, isWaiting);

    return (
        <div className="relative w-40 h-40 flex items-center justify-center ring-glow">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
                <circle
                    cx="80" cy="80" r={radius}
                    stroke="#2a2f3e"
                    strokeWidth="10"
                    fill="transparent"
                />
                <circle
                    cx="80" cy="80" r={radius}
                    stroke={ringColor}
                    strokeWidth="10"
                    fill="transparent"
                    strokeDasharray={circumference}
                    strokeDashoffset={isWaiting || !isAnimating ? circumference : targetOffset}
                    strokeLinecap="round"
                    className="transition-all duration-1000 ease-out"
                />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
                <span className="text-4xl font-extrabold text-white">
                    {isWaiting ? '—' : `${displayScore}%`}
                </span>
                <span className="text-xs font-medium tracking-widest uppercase" style={{ color: ringColor, marginTop: '4px' }}>
                    {isWaiting ? 'Waiting' : 'Match'}
                </span>
            </div>
        </div>
    );
};

export default AnimatedMatchRing;
