"use client"

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { mockChartData } from "@/lib/mockData"

export default function MarketChart() {
  return (
    <div className="bg-[#1e293b] dark:bg-[#0f172a] rounded-lg border border-gray-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">New York City Mayoral Election</h2>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span>💰 $208,735,575 Vol.</span>
            <span>📅 Nov 4, 2025</span>
          </div>
        </div>
        <div className="flex gap-2">
          <button className="p-2 hover:bg-gray-700 rounded transition-colors">🔗</button>
          <button className="p-2 hover:bg-gray-700 rounded transition-colors">🔖</button>
        </div>
      </div>

      <div className="mb-4 flex gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-orange-500"></div>
          <span className="text-white">Zohran Mamdani 92.8%</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-blue-500"></div>
          <span className="text-white">Andrew Cuomo 5.9%</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-gray-500"></div>
          <span className="text-white">Curtis Sliwa &lt;1%</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
          <span className="text-white">Eric Adams &lt;1%</span>
        </div>
      </div>

      <div className="h-80 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={mockChartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="date" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1e293b",
                border: "1px solid #374151",
                borderRadius: "8px",
                color: "#fff",
              }}
            />
            <Line type="monotone" dataKey="zohran" stroke="#f97316" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="andrew" stroke="#3b82f6" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="curtis" stroke="#6b7280" strokeWidth={2} dot={false} />
            <Line type="monotone" dataKey="eric" stroke="#eab308" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex gap-2 mb-6">
        <button className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors">1H</button>
        <button className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors">6H</button>
        <button className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors">1D</button>
        <button className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors">1W</button>
        <button className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors">1M</button>
        <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-colors">ALL</button>
      </div>

      {/* Outcome Table */}
      <div className="border-t border-gray-700 pt-4">
        <div className="flex items-center justify-between mb-4 text-sm text-gray-400">
          <span>OUTCOME</span>
          <span>% CHANCE 🔄</span>
        </div>
        
        <div className="space-y-3">
          <OutcomeRow
            name="Zohran Mamdani"
            avatar="👨‍💼"
            volume="$55,371,840"
            probability={93}
            change={1}
            yesPrice="92.8¢"
            noPrice="7.3¢"
          />
          <OutcomeRow
            name="Andrew Cuomo"
            avatar="👔"
            volume="$13,722,411"
            probability={6}
            change={null}
            yesPrice="6.0¢"
            noPrice="94.1¢"
          />
          <OutcomeRow
            name="Curtis Sliwa"
            avatar="👨"
            volume="$50k"
            probability={0}
            change={null}
            yesPrice="0.5¢"
            noPrice="99.5¢"
          />
        </div>
      </div>
    </div>
  )
}

function OutcomeRow({ name, avatar, volume, probability, change, yesPrice, noPrice }) {
  return (
    <div className="flex items-center justify-between py-3 border-b border-gray-700 last:border-0">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-xl">
          {avatar}
        </div>
        <div>
          <div className="text-white font-medium">{name}</div>
          <div className="text-xs text-gray-400">{volume} Vol. ℹ️</div>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-white font-semibold text-lg">{probability}%</span>
          {change && (
            <span className="text-green-400 text-sm">▲{change}%</span>
          )}
        </div>
        <div className="flex gap-2">
          <button className="w-[180px] py-2 bg-[#3B5355] hover:bg-[#5DA96E] text-[#6BC57B] hover:text-white font-medium rounded transition-colors text-center">
            Buy Yes {yesPrice}
          </button>
          <button className="w-[180px] py-2 bg-[#4A414D] hover:bg-[#D04740] text-[#D04740] hover:text-white font-medium rounded transition-colors text-center">
            Buy No {noPrice}
          </button>
        </div>
      </div>
    </div>
  )
}

