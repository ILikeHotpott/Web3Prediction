"use client"

import { useState } from "react"
import { mockComments } from "@/lib/mockData"
import { Heart } from "lucide-react"

export default function Comments() {
  const [sortBy, setSortBy] = useState("Newest")
  const [showHoldersOnly, setShowHoldersOnly] = useState(true)

  return (
    <div className="bg-[#1e293b] dark:bg-[#0f172a] rounded-lg border border-gray-700 p-6">
      {/* Tabs */}
      <div className="flex gap-6 border-b border-gray-700 mb-6">
        <button className="pb-3 border-b-2 border-white text-white font-semibold">
          Comments ({mockComments.length.toLocaleString()})
        </button>
        <button className="pb-3 text-gray-400 hover:text-white transition-colors">
          Top Holders
        </button>
        <button className="pb-3 text-gray-400 hover:text-white transition-colors">
          Activity
        </button>
      </div>

      {/* Comment Input */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Add a comment"
          className="w-full bg-[#334155] dark:bg-[#1e293b] text-white px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-700"
        />
        <div className="flex justify-end mt-2">
          <button className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
            Post
          </button>
        </div>
      </div>

      {/* Sort Controls */}
      <div className="flex items-center gap-4 mb-6">
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-[#334155] dark:bg-[#1e293b] text-white px-3 py-1.5 rounded border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option>Newest</option>
            <option>Oldest</option>
            <option>Most Liked</option>
          </select>
        </div>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            checked={showHoldersOnly}
            onChange={(e) => setShowHoldersOnly(e.target.checked)}
            className="w-4 h-4 rounded border-gray-700 bg-[#334155] text-blue-600 focus:ring-blue-500"
          />
          <span className="text-blue-500 text-sm">✓ Holders</span>
        </label>
        <div className="ml-auto">
          <span className="text-blue-500 text-sm">⚠️ Beware of external links.</span>
        </div>
      </div>

      {/* Comments List */}
      <div className="space-y-4">
        {mockComments.map((comment) => (
          <CommentItem key={comment.id} comment={comment} />
        ))}
      </div>
    </div>
  )
}

function CommentItem({ comment }) {
  const [liked, setLiked] = useState(false)
  const [likes, setLikes] = useState(comment.likes)

  const handleLike = () => {
    if (liked) {
      setLikes(likes - 1)
      setLiked(false)
    } else {
      setLikes(likes + 1)
      setLiked(true)
    }
  }

  return (
    <div className="group hover:bg-[#334155]/30 dark:hover:bg-[#1e293b]/50 p-4 rounded-lg transition-colors">
      <div className="flex gap-3">
        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-xl flex-shrink-0">
          {comment.avatar}
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-white font-medium">{comment.username}</span>
            <span className="text-red-400 text-xs">{comment.holdings}</span>
            <span className="text-gray-500 text-xs">{comment.timeAgo}</span>
            <button className="ml-auto opacity-0 group-hover:opacity-100 transition-opacity text-gray-400 hover:text-white">
              ⋯
            </button>
          </div>
          <p className="text-white mb-2">{comment.content}</p>
          <div className="flex items-center gap-4">
            <button
              onClick={handleLike}
              className={`flex items-center gap-1 text-sm ${
                liked ? "text-red-500" : "text-gray-400 hover:text-red-400"
              } transition-colors`}
            >
              <Heart className={`w-4 h-4 ${liked ? "fill-current" : ""}`} />
              {likes > 0 && <span>{likes}</span>}
            </button>
            <button className="text-gray-400 hover:text-white text-sm transition-colors">
              Reply
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

