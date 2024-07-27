import React, { useState } from 'react';
import { OpenAIAPIKey } from './config.js'; 

const ChatbotComponent = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    setMessages([...messages, { text: input, user: 'user' }]);
    const response = await fetchMessage(input);
    setMessages([...messages, { text: response, user: 'bot' }]);
    setInput('');
  };

  const fetchMessage = async (input) => {
    const response = await fetch('https://api.openai.com/v1/engines/davinci/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${OpenAIAPIKey}`
      },
      body: JSON.stringify({
        prompt: `You: ${input}\nAI:`,
        max_tokens: 150
      })
    });
    const data = await response.json();
    return data.choices[0].text.trim();
  };

  return (
    <div>
      <div className="message-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.user}`}>
            {message.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Type a message..."
      />
    </div>
  );
};

export default ChatbotComponent;