import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useProfileStore } from '../store/profileStore';

const Navbar: React.FC = () => {
    const logout = useAuthStore((state) => state.logout);
    const skills = useProfileStore((state) => state.skills);
    const location = useLocation();

    const isDashboard = location.pathname === '/dashboard';
    const isHistory = location.pathname === '/history';

    return (
        <nav className="w-full px-6 py-4 flex items-center justify-between border-b border-white/5 bg-[#161a25]">
            {/* Logo */}
            <div className="flex items-center gap-3">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[#38e5b1] to-[#22c55e] flex items-center justify-center">
                    <svg className="w-5 h-5 text-[#0f1117]" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                </div>
                <span className="text-xl font-bold text-white tracking-tight">
                    SkillGap
                </span>
            </div>

            {/* Navigation Links */}
            <div className="flex items-center gap-8">
                <Link
                    to="/dashboard"
                    className={`text-sm font-medium pb-1 transition-colors ${isDashboard
                        ? 'text-white border-b-2 border-[#38e5b1]'
                        : 'text-[#9aa0ac] hover:text-white border-b-2 border-transparent'
                        }`}
                >
                    Dashboard
                </Link>
                <Link
                    to="/history"
                    className={`text-sm font-medium pb-1 transition-colors ${isHistory
                        ? 'text-white border-b-2 border-[#38e5b1]'
                        : 'text-[#9aa0ac] hover:text-white border-b-2 border-transparent'
                        }`}
                >
                    History
                </Link>
                <a
                    href="#"
                    className="text-sm font-medium text-[#9aa0ac] hover:text-white transition-colors"
                >
                    Settings
                </a>
            </div>

            {/* Profile Avatar & Actions */}
            <div className="flex items-center gap-4">
                <Link to="/profile" className="flex items-center gap-2 pl-1 pr-3 py-1 rounded-full bg-gradient-to-br from-[#1e2433] to-[#161a25] border border-white/10 hover:border-[#38e5b1]/50 transition-colors">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#a78bfa] to-[#60a5fa] flex items-center justify-center">
                        <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                    </div>
                    <span className="text-sm font-medium text-white">
                        {skills.length} Skills
                    </span>
                </Link>
                <button
                    onClick={logout}
                    className="text-sm font-medium text-red-400 hover:text-red-300 transition-colors"
                >
                    Logout
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
