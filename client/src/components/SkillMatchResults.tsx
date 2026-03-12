import React from "react";
import { motion, Variants } from "framer-motion";
import AnimatedMatchRing from "./AnimatedMatchRing";
import { cn } from "../lib/utils";

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
  const matchPercentage = totalRequired > 0 ? Math.round((have.length / totalRequired) * 100) : 0;

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants: Variants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring" as const,
        stiffness: 100,
        damping: 12
      }
    }
  };

  const SkillPill: React.FC<{ skill: string; variant: "have" | "missing" | "bonus" }> = ({
    skill,
    variant,
  }) => {
    const styles = {
      have: "bg-green-500/10 text-green-400 border-green-500/20 shadow-[0_0_15px_rgba(34,197,94,0.05)]",
      missing: "bg-red-500/10 text-red-400 border-red-500/20",
      bonus: "bg-purple-500/10 text-purple-400 border-purple-500/20 shadow-[0_0_15px_rgba(168,85,247,0.05)]",
    };
    const dotColors = {
      have: "bg-green-400",
      missing: "bg-red-400",
      bonus: "bg-purple-400",
    };
    const icons = {
      have: (
        <svg
          className="w-3.5 h-3.5 text-green-400 ml-auto flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
        </svg>
      ),
      missing: null,
      bonus: (
        <svg
          className="w-3.5 h-3.5 text-purple-400 ml-auto flex-shrink-0"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2.5"
            d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
          />
        </svg>
      ),
    };

    return (
      <motion.div
        variants={itemVariants}
        whileHover={{ 
          scale: 1.02, 
          y: -2,
          backgroundColor: "rgba(255, 255, 255, 0.05)",
          borderColor: "rgba(255, 255, 255, 0.2)"
        }}
        className={cn(
          "flex items-center gap-2 px-3 py-2 rounded-lg border text-sm font-medium transition-colors duration-200",
          styles[variant]
        )}
      >
        <span className={cn("w-2 h-2 rounded-full flex-shrink-0 animate-pulse", dotColors[variant])} />
        <span className="truncate">{skill}</span>
        {icons[variant]}
      </motion.div>
    );
  };

  return (
    <div className="glass-card-accent p-6">
      {/* Section Header */}
      <div className="flex items-center gap-2 mb-5">
        <svg
          className="w-4 h-4 text-[#38e5b1]"
          fill="currentColor"
          viewBox="0 0 20 20"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
        <h2 className="text-lg font-semibold text-white">Skill Match Score</h2>
      </div>

      {/* Ring + Three-Column Layout */}
      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* Animated Ring */}
        <div className="flex-shrink-0 flex flex-col items-center justify-center pt-2">
          <AnimatedMatchRing matchScore={matchPercentage} isWaiting={!hasResults} />
        </div>

        {/* Three-Column Skill Grid */}
        <motion.div 
          className="flex-grow grid grid-cols-1 md:grid-cols-3 gap-6 w-full"
          variants={containerVariants}
          initial="hidden"
          animate={hasResults ? "visible" : "hidden"}
        >
          {/* Existing / Have */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-[#9aa0ac] uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
              Existing
            </h3>
            <div className="space-y-2">
              {hasResults ? (
                have.length > 0 ? (
                  have.map((skill) => <SkillPill key={skill} skill={skill} variant="have" />)
                ) : (
                  <p className="text-xs text-[#5f6573] italic py-4">None found</p>
                )
              ) : (
                <p className="text-xs text-[#5f6573] italic py-4">
                  Paste a JD to begin
                </p>
              )}
            </div>
          </div>

          {/* Missing */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-[#9aa0ac] uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
              Missing
            </h3>
            <div className="space-y-2">
              {hasResults ? (
                missing.length > 0 ? (
                  missing.map((skill) => <SkillPill key={skill} skill={skill} variant="missing" />)
                ) : (
                  <p className="text-xs text-[#5f6573] italic py-4">
                    Perfect match! 🎉
                  </p>
                )
              ) : (
                <p className="text-xs text-[#5f6573] italic py-4">—</p>
              )}
            </div>
          </div>

          {/* Bonus */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold text-[#9aa0ac] uppercase tracking-[0.2em] mb-4 flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-purple-500" />
              Bonus
            </h3>
            <div className="space-y-2">
              {hasResults ? (
                bonus.length > 0 ? (
                  bonus.map((skill) => <SkillPill key={skill} skill={skill} variant="bonus" />)
                ) : (
                  <p className="text-xs text-[#5f6573] italic py-4">—</p>
                )
              ) : (
                <p className="text-xs text-[#5f6573] italic py-4">—</p>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SkillMatchResults;
