import React, { useState } from 'react';

interface ChatBoxProps {
  onSend: (msg: string) => void;
  response: string;
}

const ChatBox: React.FC<ChatBoxProps> = ({ onSend, response }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<string[]>([]);

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages(prev => [...prev, `You: ${input}`]);
    onSend(input);
    setInput('');
  };

  // Append new AI response whenever it changes
  React.useEffect(() => {
    if (response) setMessages(prev => [...prev, `AI: ${response}`]);
  }, [response]);

  return (
<div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100 flex flex-col">
  {/* 🔥 Header */}
  <header className="w-full py-4 px-6 bg-gray-950 shadow flex items-center justify-between">
    <div className="text-2xl font-bold text-blue-400 flex items-center space-x-2">
      <span>💪</span>
      <span>MindForge</span>
    </div>
    <p className="text-sm text-gray-400 italic">
      “Even the darkest night will end and the sun will rise.”
    </p>
  </header>

  {/* 💬 Main Section - Now Full Width */}
  <main className="flex flex-1 overflow-hidden px-4 md:px-16 py-6">
    <section className="flex-1 flex flex-col justify-between w-full">
      {/* 💬 Messages */}
      <div className="flex-1 overflow-y-auto bg-gray-850 shadow rounded p-6 border border-gray-700 space-y-4 text-lg">
        {messages.map((msg, i) => {
          const isUser = msg.startsWith("You:");
          const displayText = msg.replace(/^You: |^AI: /, '');

          return (
            <div key={i} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-lg px-5 py-3 rounded-xl ${
                isUser
                  ? 'bg-blue-600 text-white rounded-br-none'
                  : 'bg-gray-700 text-white rounded-bl-none'
              }`}>
                {displayText}
              </div>
            </div>
          );
        })}
      </div>

      {/* 📝 Input */}
      <div className="mt-6 flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 p-4 border border-gray-600 rounded-l-lg bg-gray-800 text-white text-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Let your thoughts out..."
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-8 text-lg rounded-r-lg hover:bg-blue-700 transition-all"
        >
          Send
        </button>
      </div>
    </section>
  </main>
</div>



  );
};

export default ChatBox;
