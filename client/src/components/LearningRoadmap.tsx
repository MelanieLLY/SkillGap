import React, { useState } from "react";
import { roadmapApi } from "../api/roadmap";
import { useAuthStore } from "../store/authStore";

interface LearningRoadmapProps {
  /** Skills the user is missing — drives the "Generate" call. */
  missingSkills: string[];
  /** Optional raw JD text for extra context. */
  jdText?: string;
}

const LearningRoadmap: React.FC<LearningRoadmapProps> = ({ missingSkills, jdText }) => {
  const { user, setUser } = useAuthStore();
  const roadmap = user?.roadmap || null;

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  /** Track which timeline phases are expanded */
  const [expandedPhases, setExpandedPhases] = useState<Set<number>>(new Set());

  const canGenerate = missingSkills.length > 0;

  const handleGenerate = async () => {
    if (!canGenerate) return;
    setIsLoading(true);
    setError(null);

    try {
      const response = await roadmapApi.generate({
        missing_skills: missingSkills,
        jd_text: jdText ?? null,
      });

      // Update global user state with the new roadmap
      if (user) {
        setUser({
          ...user,
          roadmap: response.roadmap,
        });
      }

      // Auto-expand the first phase
      setExpandedPhases(new Set([1]));
    } catch (err: unknown) {
      const axiosErr = err as { response?: { status?: number; data?: { detail?: string } } };
      if (axiosErr.response?.status === 504) {
        setError("Claude AI took too long to respond. Please try again.");
      } else if (axiosErr.response?.status === 502) {
        setError("Failed to get a valid response from Claude AI. Please try again.");
      } else {
        setError("Failed to generate roadmap. Please ensure the backend is running.");
      }
      console.error("Roadmap generation failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePhase = (phase: number) => {
    setExpandedPhases((prev) => {
      const next = new Set(prev);
      if (next.has(phase)) {
        next.delete(phase);
      } else {
        next.add(phase);
      }
      return next;
    });
  };

  return (
    <div className="glass-card-accent p-6">
      {/* ── Section Header ── */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <svg
            className="w-4 h-4 text-[#38e5b1]"
            fill="currentColor"
            viewBox="0 0 20 20"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.828a1 1 0 101.415-1.414L11 9.586V6z"
              clipRule="evenodd"
            />
          </svg>
          <h2 className="text-lg font-semibold text-white">Learning Roadmap</h2>
        </div>

        {/* Generate Button */}
        <button
          id="generate-roadmap-btn"
          onClick={handleGenerate}
          disabled={!canGenerate || isLoading}
          aria-label="Generate Learning Roadmap"
          className={`
                        px-4 py-2 rounded-xl text-sm font-bold transition-all duration-300
                        flex items-center gap-2
                        ${
                          canGenerate && !isLoading
                            ? "btn-glow"
                            : "bg-[#2a2f3e] text-[#5f6573] cursor-not-allowed"
                        }
                    `}
        >
          {isLoading ? (
            <>
              <svg
                className="animate-spin w-4 h-4"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
              Generating…
            </>
          ) : (
            <>
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              Generate Roadmap
            </>
          )}
        </button>
      </div>

      {/* ── Error Banner ── */}
      {error && (
        <div className="mb-4 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-2">
          <svg
            className="w-5 h-5 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          {error}
        </div>
      )}

      {/* ── Loading Skeleton ── */}
      {isLoading && (
        <div className="space-y-3 animate-pulse" aria-label="Loading roadmap">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="flex items-center gap-4">
              <div className="w-9 h-9 rounded-full bg-[#2a2f3e] flex-shrink-0" />
              <div className="flex-grow bg-[#1a1f2e] border border-white/5 rounded-xl px-5 py-4">
                <div className="h-3 bg-[#2a2f3e] rounded w-1/3 mb-2" />
                <div className="h-2 bg-[#2a2f3e] rounded w-2/3" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ── Empty state (before generation) ── */}
      {!isLoading && !roadmap && !error && (
        <div className="text-center py-8 text-[#5f6573]">
          <svg
            className="w-10 h-10 mx-auto mb-3 opacity-40"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="1.5"
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
          <p className="text-sm">
            {canGenerate
              ? 'Click "Generate Roadmap" to create your personalised learning plan.'
              : "Analyze a job description first to see your missing skills."}
          </p>
        </div>
      )}

      {/* ── Roadmap Content ── */}
      {!isLoading && roadmap && (
        <div className="space-y-6">
          {/* Summary bar */}
          <div className="flex flex-wrap gap-3 text-xs">
            <SummaryBadge icon="📅" label={`${roadmap.total_estimated_duration_weeks} weeks`} />
            <SummaryBadge icon="📚" label={`${roadmap.summary.total_courses} courses`} />
            <SummaryBadge icon="🛠" label={`${roadmap.summary.total_projects} projects`} />
            <SummaryBadge icon="⏱" label={`${roadmap.summary.total_learning_hours}h total`} />
            <SummaryBadge icon="🎯" label={roadmap.summary.recommended_weekly_pace} />
          </div>

          {/* Timeline */}
          <div className="relative">
            {/* Vertical connector line */}
            <div className="absolute left-[18px] top-3 bottom-3 w-0.5 bg-gradient-to-b from-[#38e5b1] via-[#22c55e] to-[#5f6573]" />

            <div className="space-y-3">
              {roadmap.timeline.map((phase) => {
                const isExpanded = expandedPhases.has(phase.phase);
                return (
                  <div key={phase.phase} className="relative">
                    {/* Phase header row */}
                    <button
                      type="button"
                      onClick={() => togglePhase(phase.phase)}
                      aria-expanded={isExpanded}
                      aria-label={`Phase ${phase.phase}: ${phase.title}`}
                      className="w-full flex items-center gap-4 group text-left"
                    >
                      {/* Number circle */}
                      <div className="z-10 w-9 h-9 rounded-full bg-[#1a1f2e] border-2 border-[#38e5b1]/40 flex items-center justify-center flex-shrink-0 group-hover:border-[#38e5b1] transition-colors">
                        <span className="text-xs font-bold text-[#38e5b1]">{phase.phase}</span>
                      </div>

                      {/* Phase card */}
                      <div className="flex-grow flex items-center justify-between bg-[#1a1f2e] hover:bg-[#1f2538] border border-white/5 rounded-xl px-5 py-3.5 transition-all group-hover:border-[#38e5b1]/20">
                        <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
                          <span className="text-sm font-bold text-white">{phase.title}</span>
                          <span className="text-xs text-[#9aa0ac]">
                            Weeks {phase.start_week}–{phase.end_week} ·{" "}
                            {phase.weekly_commitment_hours}h/week
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          {/* Skill pills (compact) */}
                          <div className="hidden sm:flex gap-1">
                            {phase.focus_skills.map((skill) => (
                              <span
                                key={skill}
                                className="text-[10px] px-2 py-0.5 rounded-full bg-[#38e5b1]/10 text-[#38e5b1] font-medium"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                          {/* Chevron */}
                          <svg
                            className={`w-4 h-4 text-[#5f6573] group-hover:text-[#38e5b1] transition-transform duration-200 ${isExpanded ? "rotate-180" : ""}`}
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="2"
                              d="M19 9l-7 7-7-7"
                            />
                          </svg>
                        </div>
                      </div>
                    </button>

                    {/* Expanded detail */}
                    {isExpanded && (
                      <div className="ml-[52px] mt-2 space-y-3 animate-fadeIn">
                        {/* Milestones */}
                        <div className="bg-[#161a25] border border-white/5 rounded-xl p-4">
                          <h4 className="text-xs font-semibold text-[#9aa0ac] uppercase tracking-wider mb-2">
                            Milestones
                          </h4>
                          <ul className="space-y-1.5">
                            {phase.milestones.map((m, i) => (
                              <li key={i} className="flex items-start gap-2 text-sm text-[#e8eaed]">
                                <span className="w-1.5 h-1.5 rounded-full bg-[#38e5b1] mt-1.5 flex-shrink-0" />
                                {m}
                              </li>
                            ))}
                          </ul>
                        </div>

                        {/* Courses for this phase's skills */}
                        {roadmap.course_recommendations
                          .filter((cr) =>
                            phase.focus_skills.some(
                              (fs) => fs.toLowerCase() === cr.skill.toLowerCase(),
                            ),
                          )
                          .map((cr) => (
                            <div
                              key={cr.skill}
                              className="bg-[#161a25] border border-white/5 rounded-xl p-4"
                            >
                              <h4 className="text-xs font-semibold text-[#9aa0ac] uppercase tracking-wider mb-2">
                                📚 Courses — {cr.skill}
                              </h4>
                              <div className="space-y-2">
                                {cr.courses.map((course, ci) => (
                                  <a
                                    key={ci}
                                    href={course.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block bg-[#1a1f2e] hover:bg-[#1f2538] border border-white/5 hover:border-[#38e5b1]/20 rounded-lg p-3 transition-all"
                                  >
                                    <div className="flex items-center justify-between">
                                      <span className="text-sm font-medium text-white">
                                        {course.title}
                                      </span>
                                      <span
                                        className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                                          course.priority === "primary"
                                            ? "bg-[#38e5b1]/15 text-[#38e5b1]"
                                            : "bg-[#a78bfa]/15 text-[#a78bfa]"
                                        }`}
                                      >
                                        {course.priority}
                                      </span>
                                    </div>
                                    <div className="flex items-center gap-3 mt-1 text-xs text-[#9aa0ac]">
                                      <span>{course.platform}</span>
                                      <span>·</span>
                                      <span>{course.instructor}</span>
                                      <span>·</span>
                                      <span>{course.duration_hours}h</span>
                                      <span>·</span>
                                      <span>{course.level}</span>
                                    </div>
                                  </a>
                                ))}
                              </div>
                            </div>
                          ))}

                        {/* Project ideas for this phase */}
                        {roadmap.project_ideas
                          .filter((p) => p.phase === phase.phase)
                          .map((project) => (
                            <div
                              key={project.id}
                              className="bg-[#161a25] border border-white/5 rounded-xl p-4"
                            >
                              <h4 className="text-xs font-semibold text-[#9aa0ac] uppercase tracking-wider mb-2">
                                🛠 Project — {project.title}
                              </h4>
                              <p className="text-sm text-[#e8eaed] mb-2">{project.description}</p>
                              <div className="flex flex-wrap gap-2 mb-2">
                                <span
                                  className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                                    project.difficulty === "Beginner"
                                      ? "bg-green-500/10 text-green-400"
                                      : project.difficulty === "Intermediate"
                                        ? "bg-yellow-500/10 text-yellow-400"
                                        : "bg-red-500/10 text-red-400"
                                  }`}
                                >
                                  {project.difficulty}
                                </span>
                                <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#60a5fa]/10 text-[#60a5fa] font-semibold">
                                  ~{project.estimated_hours}h
                                </span>
                              </div>
                              <ul className="space-y-1">
                                {project.deliverables.map((d, di) => (
                                  <li
                                    key={di}
                                    className="flex items-start gap-2 text-xs text-[#9aa0ac]"
                                  >
                                    <span className="text-[#38e5b1]">✓</span>
                                    {d}
                                  </li>
                                ))}
                              </ul>
                            </div>
                          ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

/** Small summary badge for the top bar. */
const SummaryBadge: React.FC<{ icon: string; label: string }> = ({ icon, label }) => (
  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#1a1f2e] border border-white/5 text-[#9aa0ac] font-medium">
    <span>{icon}</span>
    {label}
  </span>
);

export default LearningRoadmap;
