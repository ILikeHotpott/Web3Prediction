import Navigation from "@/components/Navigation"
import MarketChart from "@/components/MarketChart"
import Comments from "@/components/Comments"

export default function MarketDetail({ params }) {
  return (
    <div className="min-h-screen bg-[#0f172a]">
      <Navigation />
      <div className="max-w-[1400px] mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Chart Area */}
          <div className="lg:col-span-2 space-y-6">
            <MarketChart />
            <Comments />
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Trade Panel */}
            <div className="bg-[#1e293b] dark:bg-[#0f172a] rounded-lg border border-gray-700 p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-full bg-gray-700 flex items-center justify-center text-2xl">
                  👨‍💼
                </div>
                <div>
                  <h3 className="text-white font-semibold">Zohran Mamdani</h3>
                </div>
              </div>

              {/* Buy/Sell Tabs */}
              <div className="flex gap-2 mb-6">
                <button className="flex-1 py-2 bg-green-600 text-white rounded-lg font-semibold">
                  Buy
                </button>
                <button className="flex-1 py-2 bg-gray-700 text-gray-400 rounded-lg font-semibold hover:bg-gray-600 hover:text-white transition-colors">
                  Sell
                </button>
              </div>

              {/* Market Selector */}
              <div className="mb-4">
                <select className="w-full bg-[#334155] dark:bg-[#1e293b] text-white px-4 py-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Market</option>
                </select>
              </div>

              {/* Yes/No Buttons */}
              <div className="grid grid-cols-2 gap-2 mb-6">
                <button className="py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold transition-colors">
                  Yes 92.8¢
                </button>
                <button className="py-3 bg-gray-700 hover:bg-gray-600 text-gray-300 rounded-lg font-semibold transition-colors">
                  No 7.3¢
                </button>
              </div>

              {/* Amount */}
              <div className="mb-6">
                <label className="text-white font-semibold mb-2 block">Amount</label>
                <div className="text-gray-400 text-sm mb-2">Balance $0.00</div>
                <div className="flex gap-2 mb-3">
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
                    +$1
                  </button>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
                    +$20
                  </button>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
                    +$100
                  </button>
                  <button className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors">
                    Max
                  </button>
                </div>
                <input
                  type="text"
                  placeholder="$0"
                  className="w-full bg-[#334155] dark:bg-[#1e293b] text-white px-4 py-3 rounded-lg border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-2xl font-bold"
                />
              </div>

              {/* Deposit Button */}
              <button className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors">
                Deposit
              </button>

              <div className="text-center text-xs text-gray-400 mt-4">
                By trading, you agree to the Terms of Use.
              </div>
            </div>

            {/* Related Markets */}
            <div className="bg-[#1e293b] dark:bg-[#0f172a] rounded-lg border border-gray-700 p-6">
              <div className="flex gap-4 border-b border-gray-700 mb-4">
                <button className="pb-2 border-b-2 border-white text-white font-semibold text-sm">
                  All
                </button>
                <button className="pb-2 text-gray-400 hover:text-white text-sm transition-colors">
                  Politics
                </button>
                <button className="pb-2 text-gray-400 hover:text-white text-sm transition-colors">
                  Elections
                </button>
                <button className="pb-2 text-gray-400 hover:text-white text-sm transition-colors">
                  NYC Mayor
                </button>
              </div>
              <div className="space-y-3">
                <RelatedMarket
                  title="Will Andrew Cuomo win second place in the 2025 NYC mayoral..."
                  probability={90}
                />
                <RelatedMarket
                  title="Will the Democratic candidate win the 2025 NYC mayoral..."
                  probability={90}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function RelatedMarket({ title, probability }) {
  return (
    <div className="p-3 bg-[#334155]/30 hover:bg-[#334155]/50 dark:bg-[#1e293b]/30 dark:hover:bg-[#1e293b]/50 rounded-lg cursor-pointer transition-colors">
      <div className="flex gap-2 mb-2">
        <div className="w-8 h-8 rounded bg-gray-700 flex items-center justify-center text-sm">
          🗳️
        </div>
        <p className="text-white text-sm flex-1">{title}</p>
      </div>
      <div className="text-right">
        <span className="text-white font-semibold">{probability}%</span>
      </div>
    </div>
  )
}

