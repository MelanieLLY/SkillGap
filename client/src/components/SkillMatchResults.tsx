import React from 'react';

export interface SkillMatchResultsProps {
  skills: {
    have: string[];
    missing: string[];
    bonus: string[];
  } | null;
}

const SkillMatchResults: React.FC<SkillMatchResultsProps> = ({ skills }) => {
  const have = skills?.have ?? [];
  const missing = skills?.missing ?? [];
  const bonus = skills?.bonus ?? [];
  const hasResults = skills !== null;

  const totalRequired = have.length + missing.length;
  const matchPercentage = totalRequired > 0
    ? Math.round((have.length / totalRequired) * 100)
    : 0;

  // Ring geometry
  const radius = 62;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (matchPercentage / 100) * circumference;

  // Color based on score
  const getRingColor = (score: number): string => {
    if (score >= 70) return '#38e5b1';
    if (score >= 40) return '#eab308';
    return '#ef4444';
  };
  const ringColor = hasResults ? getRingColor(matchPercentage) : '#38e5b1';
  const displayPercent = hasResults ? matchPercentage : 0;

  const SkillPill: React.FC<{ skill: string; variant: 'have' | 'missing' | 'bonus' }> = ({ skill, variant }) => {
    const styles = {
      have: 'bg-green-500/10 text-green-400 border-green-500/20',
      missing: 'bg-red-500/10 text-red-400 border-red-500/20',
      bonus: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    };
    const dotColors = {
      have: 'bg-green-400',
      missing: 'bg-red-400',
      bonus: 'bg-purple-400',
    };
    const icons = {
      have: (
        <svg className="w-3.5 h-3.5 text-green-400 ml-auto flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
        </svg>
      ),
      missing: null,
      bonus: (
        <svg className="w-3.5 h-3.5 text-purple-400 ml-auto flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
        </svg>
      ),
    };

    return (
      <div className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium ${styles[variant]}`}>
        <span className={`w-2 h-2 rounded-full flex-shrink-0 ${dotColors[variant]}`} />
        <span className="truncate">{skill}</span>
        {icons[variant]}
      </div>
    );
  };

  return (
    <div className="glass-card-accent p-6">
      {/* Section Header */}
      <div className="flex items-center gap-2 mb-5">
        <svg className="w-4 h-4 text-[#38e5b1]" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
          <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
        </svg>
        <h2 className="text-lg font-semibold text-white">Skill Match Score</h2>
      </div>

      {/* Ring + Three-Column Layout */}
      <div className="flex flex-col lg:flex-row gap-6 items-start">
        {/* Animated Ring */}
        <div className="flex-shrink-0 flex flex-col items-center justify-center">
          <div className="relative w-40 h-40 flex items-center justify-center ring-glow">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
              {/* Background ring */}
              <circle
                cx="80" cy="80" r={radius}
                stroke="#2a2f3e"
                strokeWidth="10"
                fill="transparent"
              />
              {/* Progress ring */}
              <circle
                cx="80" cy="80" r={radius}
                stroke={ringColor}
                strokeWidth="10"
                fill="transparent"
                strokeDasharray={circumference}
                strokeDashoffset={hasResults ? offset : circumference}
                strokeLinecap="round"
                className="transition-all duration-1000 ease-out"
                style={{
                  '--ring-circumference': circumference,
                  '--ring-offset': offset,
                } as React.CSSProperties}
              />
            </svg>
            <div className="absolute flex flex-col items-center justify-center">
              <span className="text-4xl font-extrabold text-white">
                {hasResults ? displayPercent : '—'}
              </span>
              <span className="text-xs font-medium tracking-widest uppercase" style={{ color: ringColor }}>
                {hasResults ? 'Match' : 'Waiting'}
              </span>
            </div>
          </div>
        </div>

        {/* Three-Column Skill Grid */}
        <div className="flex-grow grid grid-cols-3 gap-4 w-full">
          {/* Existing / Have */}
          <div>
            <h3 className="text-sm font-semibold text-[#9aa0ac] uppercase tracking-wider mb-3 text-center">
              Existing
            </h3>
            <div className="space-y-2">
              {hasResults ? (
                have.length > 0 ? have.map((skill, i) => (
                  <SkillPill key={i} skill={skill} variant="have" />
                )) : (
                  <p className="text-xs text-[#5f6573] italic text-center py-4">None found</p>
                )
              ) : (
                <p className="text-xs text-[#5f6573] italic text-center py-4">Paste a JD to begin</p>
              )}
            </div>
          </div>

          {/* Missing */}
          <div>
            <h3 className="text-sm font-semibold text-[#9aa0ac] uppercase tracking-wider mb-3 text-center">
              Missing
            </h3>
            <div className="space-y-2">
              {hasResults ? (
                missing.length > 0 ? missing.map((skill, i) => (
                  <SkillPill key={i} skill={skill} variant="missing" />
                )) : (
                  <p className="text-xs text-[#5f6573] italic text-center py-4">Perfect match! 🎉</p>
                )
              ) : (
                <p className="text-xs text-[#5f6573] italic text-center py-4">—</p>
              )}
            </div>
          </div>

          {/* Bonus */}
          <div>
            <h3 className="text-sm font-semibold text-[#9aa0ac] uppercase tracking-wider mb-3 text-center">
              Bonus
            </h3>
            <div className="space-y-2">
              {hasResults ? (
                bonus.length > 0 ? bonus.map((skill, i) => (
                  <SkillPill key={i} skill={skill} variant="bonus" />
                )) : (
                  <p className="text-xs text-[#5f6573] italic text-center py-4">—</p>
                )
              ) : (
                <p className="text-xs text-[#5f6573] italic text-center py-4">—</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SkillMatchResults;
