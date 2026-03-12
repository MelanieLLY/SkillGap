import React from "react";
import { motion } from "framer-motion";
import { cn } from "../lib/utils";

interface SkeletonProps {
  className?: string;
}

const Skeleton: React.FC<SkeletonProps> = ({ className }) => {
  return (
    <div
      className={cn("relative overflow-hidden bg-[#2a2f3e] rounded-lg", className)}
      aria-hidden="true"
    >
      <motion.div
        animate={{
          x: ["-100%", "100%"],
        }}
        transition={{
          repeat: Infinity,
          duration: 1.5,
          ease: "linear",
        }}
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent"
      />
    </div>
  );
};

export default Skeleton;
