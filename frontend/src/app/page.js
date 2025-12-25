import Navigation from "@/components/Navigation";
import FilterBar from "@/components/FilterBar";
import MarketGrid from "@/components/MarketGrid";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#202b39]">
      <Navigation />
      <FilterBar />
      <MarketGrid />
    </div>
  );
}
