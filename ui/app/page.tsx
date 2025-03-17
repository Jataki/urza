// app/page.tsx
"use client";

import { useState, useRef, useEffect } from "react";

export default function Home() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Add welcome message on first load
  useEffect(() => {
    setMessages([
      { 
        role: "assistant", 
        content: "Welcome to the MTG Strategist! Ask me about deck building, card synergies, or strategy tips for Magic: The Gathering." 
      }
    ]);
  }, []);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    // Simulated response for now
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "This is a simulated response. I'll help you with your MTG strategy." }
      ]);
      setIsLoading(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-gray-900 to-black text-white">
      {/* Header */}
      <header className="p-4 border-b border-gray-800 bg-gray-900 shadow-md">
        <h1 className="text-2xl font-bold text-center text-blue-400">MTG Strategist</h1>
      </header>

      {/* Chat container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-w-3xl mx-auto w-full">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div 
              className={`p-3 rounded-lg max-w-[80%] ${
                message.role === "user" 
                  ? "bg-blue-600 text-white rounded-br-none" 
                  : "bg-gray-800 text-gray-100 rounded-bl-none"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 p-3 rounded-lg rounded-bl-none text-gray-100">
              <div className="flex space-x-1">
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce" style={{ animationDelay: "0.4s" }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <div className="p-4 border-t border-gray-800 bg-gray-900">
        <form onSubmit={handleSubmit} className="flex gap-2 max-w-3xl mx-auto">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about MTG strategies..."
            className="flex-1 p-3 rounded-lg bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-700 disabled:opacity-50"
            disabled={isLoading}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}