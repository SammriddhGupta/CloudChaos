/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from "react";
import axios from "axios";
import { BrowserRouter as Router, Route, Link, Routes, useLocation, useNavigate } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Avatar
} from "@mui/material";
import CollectDataPage from "./pages/CollectDataPage.js";
import PreprocessingPage from "./pages/PreprocessingPage.js";
import ComparisonPage from "./pages/ComparisonPage.js";
import PredictionPage from "./pages/PredictionPage.js";
import RedirectPage from "./pages/RedirectPage.js";
import Dashboard from "./pages/Dashboard.js";
import LandingPage from "./pages/LandingPage.js";
import PricingPage from "./pages/PricingPage.js";
import Logo from "./logo.jpg";
import LoginIcon from "./login.jpg";
import ProfileIcon from "./profile.jpg";
import "./App.css";
import { ListItemIcon, ListItemText } from '@mui/material';
import SettingsIcon from '@mui/icons-material/Settings';
import HistoryIcon from '@mui/icons-material/History';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import EditIcon from '@mui/icons-material/Edit';
import ChatBot from 'react-simple-chatbot';

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

function AppContent() {

  const location = useLocation();
  const navigate = useNavigate();

  const steps = [
    {
      id: '1',
      message: 'Welcome! How can I assist you today?',
    },

  ];

  

  const Chatbot = () => {
    const [chatHistory, setChatHistory] = useState([]);
    const [userMessage, setUserMessage] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    
  
    const sendMessage = async () => {
      const trimmedMessage = userMessage.trim();
      if (trimmedMessage) {
        setUserMessage('');
        setChatHistory([...chatHistory, { message: 'You: ' + trimmedMessage, type: 'user' }]);
  
        try {
          const OPENAI_API_KEY = 'insert-key';
          const response = await axios.post(
            'https://api.openai.com/v1/completions',
            {
              model: 'text-davinci-003', // Choose a suitable OpenAI model
              prompt: trimmedMessage,
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
          setChatHistory([...chatHistory, { message: 'Bot: ' + botResponse, type: 'bot' }]);
        } catch (error) {
          console.error('OpenAI API error:', error);
          setChatHistory([...chatHistory, { message: 'Oops, something went wrong. Please try again later.', type: 'error' }]);
        }
      }
    };

    const toggleChatbot = () => {
      setIsOpen(!isOpen);
    };

    useEffect(() => {
      // Optional: Scroll chat history to bottom on update
      const chatContainer = document.getElementById('chat-history');
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    }, [chatHistory]); // Run on chat history change



  }


  let authToken = localStorage.getItem('auth_token');
  let isLoggedIn = authToken !== null;

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('username'); 
    navigate('/landing'); 
  };

  return (
    <>
      <AppBar
        position="static"
        style={{ backgroundColor: "white", color: "black" }}
      >
        <Toolbar style={{ display: "flex", justifyContent: "space-between", margin: "0px", padding: "0px" }}>
          <Link to="/">
            <img
              src={Logo}
              alt="Logo"
              style={{ height: "70px", marginRight: "20px", marginTop: "10px" }}
            />
          </Link>
          <div style={{ display: "flex", alignItems: "center" }}>
          <Typography
              variant="h6"
              component="a"
              href="https://app.swaggerhub.com/apis-docs/SAMMRIDDHGUPTA/cloudchaos/1.0.0"
              target="_blank"
              rel="noopener noreferrer"
              className={`nav-link ${location.pathname === "/docs" ? "active" : ""}`}
            >
              Docs
            </Typography>
          <Typography
              variant="h6"
              component={Link}
              to="/pricing"
              className={`nav-link ${location.pathname === "/pricing" ? "active" : ""}`}
            >
              Subscription
            </Typography>
            <Typography
              variant="h6"
              component={Link}
              to="/collection"
              className={`nav-link ${location.pathname === "/collection" ? "active" : ""}`}
            >
              Collection
            </Typography>
            <Typography
              variant="h6"
              component={Link}
              to="/preprocessing"
              className={`nav-link ${location.pathname === "/preprocessing" ? "active" : ""}`}
            >
              Preprocessing
            </Typography>

            <Typography
              variant="h6"
              component={Link}
              to="/comparison"
              className={`nav-link ${location.pathname === "/comparison" ? "active" : ""}`}      
            >
              Comparison
            </Typography>

            <Typography
              variant="h6"
              component={Link}
              to="/prediction"
              className={`nav-link ${location.pathname === "/prediction" ? "active" : ""}`}         
            >
              Prediction
            </Typography>
            {/* Conditional rendering for login/profile button */}
            {isLoggedIn ? (
              <LoggedInMenu handleLogout={handleLogout} />
            ) : (
              <Link to="https://cloudchaos.auth.ap-southeast-2.amazoncognito.com/login?client_id=1gqsqb0d5vh6osuuc2950ub8v9&response_type=token&scope=email+openid+phone&redirect_uri=https://main.d332b7vcir4cg5.amplifyapp.com/redirect" className="signup-button">
                <IconButton style={{ padding: "20px" }}>
                  <img
                    src={LoginIcon}
                    alt="Login"
                    style={{ height: "40px", width: "auto" }}
                  />
                </IconButton>
              </Link>
            )}
          </div>
        </Toolbar>
      </AppBar>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          minHeight: "100vh",
          overflow: "auto",
          border: "none",
          padding: "0",
        }}
      >
        <Routes>
          <Route path="*" element={<Dashboard />} />
          <Route path="/collection" element={<CollectDataPage />} />
          <Route path="/preprocessing" element={<PreprocessingPage />} />
          <Route path="/comparison" element={<ComparisonPage />} />
          <Route path="/prediction" element={<PredictionPage />} />
          <Route path="/redirect" element={<RedirectPage/>} />
          <Route path="/landing" element={<LandingPage/>} />
          <Route path="/pricing" element={<PricingPage/>} />
        </Routes>
       {/*  <Chatbot/> */}
       <ChatBot steps={steps} floating={true} />
      </Box>    
    </>
  );
}

// Logged-in menu component
function LoggedInMenu({ handleLogout }) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [username, setUsername] = useState('');

  useEffect(() => {
    const username = localStorage.getItem('username');
    setUsername(username);
  }, []);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <IconButton onClick={handleClick} style={{ marginRight: '8px' }}>
        <Avatar alt="Profile" src={ProfileIcon} style={{ width: '40px', height: '40px', marginRight: '8px' }} />
      </IconButton>
      <Menu
        id="profile-menu"
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        style={{ justifyContent: 'center' }}
      >
        <MenuItem onClick={handleClose} style={{ display: 'flex', alignItems: 'center', paddingBottom: '10px' }}>
          <ListItemIcon style={{ marginRight: '16px' }}>
            <Avatar alt="Profile" src={ProfileIcon} style={{ width: '60px', height: '60px' }} />
          </ListItemIcon>
          <ListItemText primary={`${username ? `${username}  ` : 'Edit Profile'}`} />
          <EditIcon />
        </MenuItem>
        <MenuItem onClick={handleClose}>
          <ListItemIcon style={{ color: 'black' }}>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary="Settings" />
        </MenuItem>
        <MenuItem onClick={handleClose}>
          <ListItemIcon style={{ color: 'black' }}>
            <HistoryIcon />
          </ListItemIcon>
          <ListItemText primary="History" />
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon style={{ color: 'red' }}>
            <ExitToAppIcon />
          </ListItemIcon>
          <ListItemText primary={<span style={{ color: 'red' }}>Logout</span>} />
        </MenuItem>
      </Menu>
    </>
  );
}
export default App;
