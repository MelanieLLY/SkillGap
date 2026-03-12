import React, { useEffect, useState } from "react";
import { motion, useSpring, useTransform } from "framer-motion";

export interface AnimatedMatchRingProps {
  matchScore: number;
  isWaiting?: boolean;
}

const AnimatedMatchRing: React.FC<AnimatedMatchRingProps> = ({ matchScore, isWaiting = false }) => {
  const [displayScore, setDisplayScore] = useState(0);

  // 优化后的物理参数：更平滑的阻尼，更少的抖动
  const springScore = useSpring(0, {
    stiffness: 45, // 降低刚度，减慢初始冲力
    damping: 20, // 提高阻尼，减少余震
    restDelta: 0.01,
  });

  // 监听 spring 变化并同步更新数字，确保数字与圆环物理同步
  useEffect(() => {
    const unsubscribe = springScore.on("change", (v) => {
      setDisplayScore(Math.round(v));
    });
    return () => unsubscribe();
  }, [springScore]);

  useEffect(() => {
    if (isWaiting) {
      springScore.set(0);
    } else {
      springScore.set(matchScore);
    }
  }, [matchScore, isWaiting, springScore]);

  // 环形几何：确保计算精准
  const radius = 62;
  const circumference = 2 * Math.PI * radius;

  // 映射逻辑：0 -> 全偏移（空环），100 -> 无偏移（满环）
  const dashOffset = useTransform(springScore, [0, 100], [circumference, 0]);

  const getRingColor = (score: number, waiting: boolean): string => {
    if (waiting) return "#38e5b1";
    if (score >= 70) return "#38e5b1"; // 绿色
    if (score >= 40) return "#eab308"; // 黄色
    return "#ef4444"; // 红色
  };

  const ringColor = getRingColor(matchScore, isWaiting);

  return (
    <div className="relative w-40 h-40 flex items-center justify-center">
      {/* 优化后的背景光晕：更柔和，减少视觉干扰 */}
      <motion.div
        animate={{
          scale: [1, 1.02, 1], // 极微小的缩放
          opacity: [0.15, 0.22, 0.15],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute inset-0 rounded-full blur-3xl"
        style={{ backgroundColor: ringColor }}
      />

      <svg className="w-full h-full transform -rotate-90 z-10" viewBox="0 0 160 160">
        {/* 背景底环 */}
        <circle cx="80" cy="80" r={radius} stroke="#1e2330" strokeWidth="10" fill="transparent" />
        {/* 进度环 */}
        <motion.circle
          cx="80"
          cy="80"
          r={radius}
          stroke={ringColor}
          strokeWidth="10"
          fill="transparent"
          strokeDasharray={`${circumference} ${circumference}`}
          style={{
            strokeDashoffset: dashOffset,
            filter: `drop-shadow(0 0 8px ${ringColor}44)`,
          }}
          strokeLinecap="round"
          initial={{ strokeDashoffset: circumference }}
        />
      </svg>

      <div className="absolute flex flex-col items-center justify-center z-20">
        {/* 移除 key 动画，避免数字跳动时的视觉污染 */}
        <span className="text-4xl font-extrabold text-white tabular-nums">
          {isWaiting ? "—" : `${displayScore}%`}
        </span>
        <motion.span
          className="text-[10px] font-bold tracking-[0.2em] uppercase"
          style={{ color: ringColor, marginTop: "4px" }}
          animate={{ opacity: isWaiting ? 0.4 : 0.8 }}
        >
          {isWaiting ? "Pending" : "Match"}
        </motion.span>
      </div>
    </div>
  );
};

export default AnimatedMatchRing;
