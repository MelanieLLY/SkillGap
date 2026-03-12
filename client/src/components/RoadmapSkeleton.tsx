import React from "react";
import Skeleton from "./Skeleton";

const RoadmapSkeleton: React.FC = () => {
  return (
    <div className="space-y-6" aria-busy="true" aria-label="Loading learning roadmap">
      {/* Summary bar skeleton */}
      <div className="flex flex-wrap gap-3">
        {[1, 2, 3, 4, 5].map((i) => (
          <Skeleton key={i} className="h-7 w-24 rounded-lg" />
        ))}
      </div>

      {/* Timeline skeleton */}
      <div className="relative">
        {/* Vertical connector line placeholder */}
        <div className="absolute left-[18px] top-3 bottom-3 w-0.5 bg-[#2a2f3e]" />

        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="flex items-center gap-4">
              {/* Number circle skeleton */}
              <Skeleton className="w-9 h-9 rounded-full flex-shrink-0" />

              {/* Phase card skeleton */}
              <div className="flex-grow flex items-center justify-between bg-[#1a1f2e]/50 border border-white/5 rounded-xl px-5 py-4">
                <div className="space-y-2 w-full">
                  <div className="flex items-center gap-3">
                    <Skeleton className="h-4 w-32" />
                    <Skeleton className="h-3 w-40" />
                  </div>
                  <div className="flex gap-2">
                    <Skeleton className="h-4 w-16 rounded-full" />
                    <Skeleton className="h-4 w-16 rounded-full" />
                  </div>
                </div>
                <Skeleton className="w-4 h-4 ml-4" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RoadmapSkeleton;
