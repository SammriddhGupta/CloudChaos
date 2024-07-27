/* eslint-disable no-unused-vars */
import React from 'react';
import { MessageParser } from 'react-simple-chatbot';

//import axios from 'axios';

class MyMessageParser extends MessageParser {
    parse(message) {
      // Optional processing of user input (e.g., trimming, lowercase)
      const cleanMessage = message.trim().toLowerCase();
      return cleanMessage;
    }
  }

export default MyMessageParser;
