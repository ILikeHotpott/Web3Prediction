"use client"

import { useState, useEffect, useRef } from "react"
import MarketCard from "./MarketCard"
import ChanceMarketCard from "./ChanceMarketCard"
import LoadingSpinner from "./LoadingSpinner"
import { mockMarkets } from "@/lib/mockData"

export default function MarketGrid() {
  const [displayedMarkets, setDisplayedMarkets] = useState([])
  const [page, setPage] = useState(0)
  const [loading, setLoading] = useState(false)
  const [hasMore, setHasMore] = useState(true)
  const observerTarget = useRef(null)

  const ITEMS_PER_PAGE = 20 // 5 rows × 4 columns = 20 items

  // Initial load
  useEffect(() => {
    loadMore()
  }, [])

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          loadMore()
        }
      },
      { threshold: 0.1 }
    )

    if (observerTarget.current) {
      observer.observe(observerTarget.current)
    }

    return () => {
      if (observerTarget.current) {
        observer.unobserve(observerTarget.current)
      }
    }
  }, [hasMore, loading, page])

  const loadMore = () => {
    if (loading) return

    setLoading(true)
    
    // Simulate API delay
    setTimeout(() => {
      const startIndex = page * ITEMS_PER_PAGE
      const endIndex = startIndex + ITEMS_PER_PAGE
      
      // Create more data by cycling through mock data
      const allMarkets = []
      for (let i = 0; i < 10; i++) {
        allMarkets.push(...mockMarkets.map((m, idx) => ({
          ...m,
          id: `${i}-${m.id}`,
          title: m.title
        })))
      }
      
      const newMarkets = allMarkets.slice(startIndex, endIndex)
      
      if (newMarkets.length === 0) {
        setHasMore(false)
      } else {
        setDisplayedMarkets((prev) => [...prev, ...newMarkets])
        setPage((prev) => prev + 1)
      }
      
      setLoading(false)
    }, 800)
  }

  return (
    <div className="max-w-[1400px] mx-auto px-12">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {displayedMarkets
          .filter((market) => {
            // Only show markets that have outcomes, timeRanges, or chance
            return market.outcomes || market.timeRanges || market.chance !== undefined
          })
          .map((market, idx) => {
            // Convert timeRanges to outcomes format if needed
            let normalizedMarket = { ...market }
            if (market.timeRanges && !market.outcomes) {
              normalizedMarket.outcomes = market.timeRanges.map((range) => ({
                name: range.period,
                probability: range.probability,
                change: null,
              }))
            }

            if (
              normalizedMarket.chance !== undefined ||
              ((normalizedMarket.outcomes || []).map((o) => String(o.name || "").toLowerCase()).sort().join("-") === "no-yes")
            ) {
              // Binary Yes/No cards (with chance gauge). If chance not provided, derive from Yes probability.
              return <ChanceMarketCard key={`${market.id}-${idx}`} market={normalizedMarket} />
            } else {
              // Multi-option cards
              return <MarketCard key={`${market.id}-${idx}`} market={normalizedMarket} />
            }
          })}
      </div>
      
      {loading && <LoadingSpinner />}
      
      {/* Intersection Observer Target */}
      <div ref={observerTarget} className="h-4" />
      
      {!hasMore && (
        <div className="text-center text-gray-500 py-8">
          No more markets to load
        </div>
      )}
    </div>
  )
}

