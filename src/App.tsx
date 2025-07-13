import React, { useState } from 'react';
import ChatBox from './ChatBox';

const App: React.FC = () => {
  const [botReply, setBotReply] = useState("");

  const sendMessage = async (message: string) => {
    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setBotReply(data.reply);
    } catch (error) {
      console.error("Error:", error);
      setBotReply("Sorry, something went wrong.");
    }
  };

  return <ChatBox onSend={sendMessage} response={botReply} />;
};

export default App;
