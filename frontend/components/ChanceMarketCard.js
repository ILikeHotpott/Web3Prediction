"use client"

import Link from "next/link"
import { Card } from "@/components/ui/card"

export default function ChanceMarketCard({ market }) {
  const outcomeNames = (market.outcomes || []).map((o) => String(o.name || "").toLowerCase())
  const yesOutcome = (market.outcomes || []).find((o) => String(o.name || "").toLowerCase() === "yes")
  const computedChance = typeof market.chance === "number" ? market.chance : (yesOutcome?.probability ?? 0)

  return (
    <Link href={`/market/${market.id}`}>
      <Card className="bg-[#323F4F] border border-[#425264] hover:bg-[#3a4a5c] transition-all cursor-pointer overflow-hidden group aspect-[1.618/1] flex flex-col">
        <div className="p-3.5 flex flex-col h-full">
          {/* Header with Image, Title and Gauge at right */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex gap-2.5 pr-2">
              <div className="w-11 h-11 rounded-lg bg-gray-700 flex items-center justify-center text-xl flex-shrink-0">
                {market.image}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-white font-medium text-[15px] leading-tight line-clamp-2 group-hover:text-blue-400 transition-colors">
                  {market.title}
                </h3>
              </div>
            </div>
            <div className="flex flex-col items-center flex-shrink-0">
              <div className="relative w-14 h-14">
                <svg className="w-14 h-14 transform -rotate-90">
                  <circle cx="28" cy="28" r="23" stroke="#374151" strokeWidth="5" fill="none" />
                  <circle
                    cx="28"
                    cy="28"
                    r="23"
                    stroke={computedChance >= 50 ? "#10b981" : "#ef4444"}
                    strokeWidth="5"
                    fill="none"
                    strokeDasharray={`${(computedChance / 100) * 144.51} 144.51`}
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-bold text-white">{computedChance}%</span>
                </div>
              </div>
              <div className="text-[9px] text-gray-400 mt-0.5">chance</div>
            </div>
          </div>

          {/* Bottom big buttons */}
          <div className="mt-auto mb-3">
            <div className="flex gap-2.5">
              <button className="flex-1 py-2.5 bg-[#3B5355] hover:bg-[#5DA96E] text-[#6BC57B] hover:text-white text-sm font-semibold rounded transition-colors text-center">
                Yes
              </button>
              <button className="flex-1 py-2.5 bg-[#4A414D] hover:bg-[#D04740] text-[#D04740] hover:text-white text-sm font-semibold rounded transition-colors text-center">
                No
              </button>
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-between text-xs text-gray-500 pt-2.5 border-t border-gray-600">
            <span>{market.volume} Vol. 🔄</span>
            <div className="flex gap-2">
              <button className="hover:text-gray-400 transition-colors">🎁</button>
              <button className="hover:text-gray-400 transition-colors">🔖</button>
            </div>
          </div>
        </div>
      </Card>
    </Link>
  )
}


