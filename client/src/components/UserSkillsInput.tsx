import React, { useState, KeyboardEvent } from "react";

interface UserSkillsInputProps {
  skills: string[];
  onSkillsChange: (skills: string[]) => void;
}

const UserSkillsInput: React.FC<UserSkillsInputProps> = ({ skills, onSkillsChange }) => {
  const [inputValue, setInputValue] = useState("");

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      addSkill();
    }
  };

  const addSkill = () => {
    const trimmedValue = inputValue.trim().toLowerCase();
    if (trimmedValue && !skills.includes(trimmedValue)) {
      const newSkills = [...skills, trimmedValue];
      onSkillsChange(newSkills);
      setInputValue("");
    }
  };

  const removeSkill = (skillToRemove: string) => {
    const newSkills = skills.filter((skill) => skill !== skillToRemove);
    onSkillsChange(newSkills);
  };

  return (
    <div className="glass-card-accent p-6 flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <svg
          className="w-4 h-4 text-[#38e5b1]"
          fill="currentColor"
          viewBox="0 0 20 20"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
            clipRule="evenodd"
          />
        </svg>
        <h2 className="text-lg font-semibold text-white">Your Skills</h2>
      </div>

      <div className="flex flex-wrap gap-2 min-h-[40px] p-3 bg-[#161a25] rounded-xl border border-white/5">
        {skills.length === 0 && (
          <span className="text-sm text-[#5f6573] italic">No skills added yet...</span>
        )}
        {skills.map((skill) => (
          <span
            key={skill}
            className="flex items-center gap-1.5 px-3 py-1 bg-[#38e5b1]/10 border border-[#38e5b1]/20 rounded-full text-sm font-medium text-[#38e5b1]"
          >
            {skill}
            <button
              onClick={() => removeSkill(skill)}
              className="hover:text-white transition-colors"
            >
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2.5"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </span>
        ))}
      </div>

      <div className="relative group">
        <input
          type="text"
          className="jd-textarea w-full pl-4 pr-12 py-3 text-sm"
          placeholder="Add a skill (e.g. Python, React)..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={addSkill}
        />
        <button
          onClick={addSkill}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-[#38e5b1] hover:bg-[#38e5b1]/10 rounded-lg transition-all"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2.5"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
        </button>
      </div>

      <p className="text-[11px] text-[#5f6573] italic">Press Enter or comma to add a skill</p>
    </div>
  );
};

export default UserSkillsInput;
