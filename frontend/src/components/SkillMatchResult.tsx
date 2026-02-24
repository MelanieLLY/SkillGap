import React from 'react';

export interface SkillMatchProps {
    matchResult: {
        have: string[];
        missing: string[];
        bonus: string[];
    };
}

const SkillMatchResult: React.FC<SkillMatchProps> = ({ matchResult }) => {
    const { have, missing, bonus } = matchResult;

    const containerStyle: React.CSSProperties = {
        fontFamily: 'system-ui, -apple-system, sans-serif',
        padding: '24px',
        backgroundColor: '#ffffff',
        borderRadius: '12px',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        maxWidth: '650px',
        margin: '0 auto',
    };

    const titleStyle: React.CSSProperties = {
        fontSize: '24px',
        fontWeight: 700,
        marginBottom: '24px',
        color: '#111827',
        textAlign: 'center'
    };

    const sectionStyle = (borderColor: string): React.CSSProperties => ({
        marginBottom: '20px',
        borderLeft: `4px solid ${borderColor}`,
        padding: '16px',
        backgroundColor: '#f9fafb',
        borderRadius: '0 8px 8px 0',
    });

    const headerStyle = (color: string): React.CSSProperties => ({
        margin: '0 0 12px 0',
        fontSize: '18px',
        fontWeight: 600,
        color: color,
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
    });

    const badgeContainerStyle: React.CSSProperties = {
        display: 'flex',
        flexWrap: 'wrap',
        gap: '8px',
    };

    const baseBadgeStyle: React.CSSProperties = {
        padding: '6px 14px',
        borderRadius: '20px',
        fontSize: '14px',
        fontWeight: 500,
        display: 'inline-block',
    };

    const colors = {
        have: { bg: '#dcfce7', text: '#166534', border: '#22c55e' },
        missing: { bg: '#fee2e2', text: '#991b1b', border: '#ef4444' },
        bonus: { bg: '#dbeafe', text: '#1e40af', border: '#3b82f6' }
    };

    const renderSection = (title: string, skills: string[], category: keyof typeof colors) => {
        if (skills.length === 0) return null;

        return (
            <div style={sectionStyle(colors[category].border)}>
                <h3 style={headerStyle(colors[category].text)}>{title}</h3>
                <div style={badgeContainerStyle}>
                    {skills.map((skill) => (
                        <span
                            key={skill}
                            style={{
                                ...baseBadgeStyle,
                                backgroundColor: colors[category].bg,
                                color: colors[category].text,
                                border: `1px solid ${colors[category].border}40`
                            }}
                        >
                            {skill}
                        </span>
                    ))}
                </div>
            </div>
        );
    };

    return (
        <div style={containerStyle}>
            <h2 style={titleStyle}>
                Skill Match Analysis
            </h2>

            {have.length === 0 && missing.length === 0 && bonus.length === 0 ? (
                <p style={{ color: '#6b7280', fontStyle: 'italic', textAlign: 'center' }}>
                    No skills data to display. Add some skills or a job description to see results.
                </p>
            ) : (
                <>
                    {renderSection('✅ Skills You Have', have, 'have')}
                    {renderSection('❌ Missing Skills', missing, 'missing')}
                    {renderSection('⭐ Bonus Skills', bonus, 'bonus')}
                </>
            )}
        </div>
    );
};

export default SkillMatchResult;
