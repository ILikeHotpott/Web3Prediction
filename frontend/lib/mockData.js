export const mockMarkets = [
  {
    id: 1,
    title: "When will the Government shutdown end?",
    image: "🏛️",
    deadline: "Nov 4, 2025",
    volume: "$1m",
  },
  {
    id: 2,
    title: "New York City Mayoral Election",
    image: "🗽",
    deadline: "Nov 4, 2025",
    volume: "$209m",
    outcomes: [
      { name: "Zohran Mamdani", probability: 93, change: 1 },
      { name: "Andrew Cuomo", probability: 6, change: null },
    ],
  },
  {
    id: 3,
    title: "Fed decision in October?",
    image: "💵",
    deadline: "Nov 7, 2025",
    volume: "$99m",
    outcomes: [
      { name: "60+ bps decrease", probability: 3, change: null },
      { name: "25 bps decrease", probability: 96, change: null },
    ],
  },
  {
    id: 4,
    title: "What will Trump say during Australia PM events on October...",
    image: "🇺🇸",
    deadline: "Oct 31, 2025",
    volume: "$92k",
    outcomes: [
      { name: "Trillion / Million / Billion...", probability: 66, change: null },
      { name: "China 3+ times", probability: 86, change: null },
    ],
  },
  {
    id: 5,
    title: "Israel x Hamas ceasefire cancelled by...?",
    image: "🇮🇱",
    deadline: "Dec 31, 2025",
    volume: "$858k",
    outcomes: [
      { name: "October 31", probability: 10, change: null },
      { name: "December 31", probability: 37, change: null },
    ],
  },
  {
    id: 6,
    title: "Will any Louvre heist robbers be arrested by...?",
    image: "🎨",
    deadline: "Oct 24, 2025",
    volume: "$37k",
    outcomes: [
      { name: "October 20", probability: 5, change: null },
      { name: "October 24", probability: 23, change: null },
    ],
  },
  {
    id: 7,
    title: "Russia x Ukraine ceasefire in 2025?",
    image: "🇷🇺",
    deadline: "Dec 31, 2025",
    volume: "$23m",
    outcomes: [
      { name: "Yes", probability: 18, change: null },
      { name: "No", probability: 82, change: null },
    ],
    chance: 18,
  },
  {
    id: 8,
    title: "Monad airdrop by...?",
    image: "💎",
    deadline: "Nov 30, 2025",
    volume: "$11m",
    outcomes: [
      { name: "November 15", probability: 24, change: null },
      { name: "November 30", probability: 87, change: null },
    ],
  },
  {
    id: 9,
    title: "#1 Searched Person on Google this year?",
    image: "🔍",
    deadline: "Dec 31, 2025",
    volume: "$3m",
    outcomes: [
      { name: "Pope Leo XIV", probability: 27, change: null },
      { name: "Donald Trump", probability: 21, change: null },
    ],
  },
  {
    id: 10,
    title: "Will Trump meet with Xi Jinping by October 31?",
    image: "🤝",
    deadline: "Oct 31, 2025",
    volume: "$2m",
    outcomes: [
      { name: "Yes", probability: 83, change: null },
      { name: "No", probability: 17, change: null },
    ],
    chance: 83,
  },
  {
    id: 11,
    title: "100% tariff on China in effect by November 1?",
    image: "🇨🇳",
    deadline: "Nov 1, 2025",
    volume: "$1.5m",
    outcomes: [
      { name: "Yes", probability: 10, change: null },
      { name: "No", probability: 90, change: null },
    ],
    chance: 10,
  },
  {
    id: 12,
    title: "World Series Champion 2025",
    image: "⚾",
    deadline: "Nov 5, 2025",
    volume: "$5m",
    outcomes: [
      { name: "Yankees", probability: 45, change: 2 },
      { name: "Dodgers", probability: 55, change: -2 },
    ],
  },
  {
    id: 13,
    title: "Will Tesla (TSLA) beat quarterly earnings?",
    image: "🚗",
    deadline: "Oct 23, 2025",
    volume: "$800k",
    outcomes: [
      { name: "Yes", probability: 75, change: 5 },
      { name: "No", probability: 25, change: -5 },
    ],
  },
  {
    id: 14,
    title: "Bolivia Presidential Election Margin of Victory",
    image: "🇧🇴",
    deadline: "Nov 1, 2025",
    volume: "$1m",
    outcomes: [
      { name: "Paz by 5-10%", probability: 52, change: null },
      { name: "Paz by 0-5%", probability: 1, change: null },
    ],
  },
  {
    id: 15,
    title: "US x Venezuela military engagement by...?",
    image: "🇻🇪",
    deadline: "Oct 31, 2025",
    volume: "$4m",
    outcomes: [
      { name: "October 31", probability: 9, change: null },
      { name: "November 30", probability: 30, change: null },
    ],
  },
];

export const mockComments = [
  {
    id: 1,
    username: "jillianhicks",
    avatar: "👩",
    holdings: "768 Curtis Sliwa",
    timeAgo: "32m ago",
    content: "free money",
    likes: 0,
  },
  {
    id: 2,
    username: "bikkon",
    avatar: "👨",
    holdings: "100 Eric Adams",
    timeAgo: "4h ago",
    content: "Eric",
    likes: 3,
  },
  {
    id: 3,
    username: "Common-Authorisa...",
    avatar: "🔵",
    holdings: "1.0K Rudy Giuliani",
    timeAgo: "8h ago",
    content: "Rudi",
    likes: 6,
  },
  {
    id: 4,
    username: "martinsituwcs",
    avatar: "🟣",
    holdings: "1 Zohran Mamdani",
    timeAgo: "12h ago",
    content: "a",
    likes: 1,
  },
];

export const mockChartData = [
  { date: "Jun", zohran: 90, andrew: 5, curtis: 3, eric: 2 },
  { date: "Jul", zohran: 85, andrew: 8, curtis: 4, eric: 3 },
  { date: "Aug", zohran: 88, andrew: 6, curtis: 3, eric: 3 },
  { date: "Sep", zohran: 91, andrew: 5, curtis: 2, eric: 2 },
  { date: "Oct", zohran: 93, andrew: 6, curtis: 1, eric: 1 },
];

