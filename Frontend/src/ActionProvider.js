
/* eslint-disable no-unused-vars */
import React from 'react';
import { ActionProvider } from 'react-simple-chatbot';

import axios from 'axios';

const OPENAI_API_KEY = 'key'; 

class MyActionProvider extends ActionProvider {
  async handle(message, retrievedState) {
    const response = await axios.post(
      'https://api.openai.com/v1/completions',
      {
        model: 'text-davinci-003', // Choose a suitable OpenAI model
        prompt: message,
        max_tokens: 1024,
        n: 1,
        stop: null, // Or provide a stop sequence if desired
        temperature: 0.7, // Adjust temperature for response creativity
      },
      {
        headers: {
          Authorization: `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const botResponse = response.data.choices[0].text.trim();
    return this.chatbot.appendBotResponse(botResponse);
  }
  catch (error) {
    console.error('OpenAI API error:', error);
    return this.chatbot.appendBotResponse('Oops, something went wrong. Please try again later.');
  }
}

export default MyActionProvider;
