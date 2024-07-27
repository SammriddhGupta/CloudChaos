// Dashboard.js
import React from "react";
import backgroundImage from "./background.jpg";
import { Button } from "@mui/material";
import LandingPage from "./LandingPage.js";
import { Route, Routes } from "react-router-dom";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import SearchIcon from "@mui/icons-material/Search";
import BarChartIcon from "@mui/icons-material/BarChart";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";
import pricingImage from "../PaymentModel_Current.png";
import paymentImage from "../Payment.png";

const Dashboard = () => {
  const navigate = useNavigate();
  let username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('username'); 
    navigate('/landing'); 
  };

  useEffect(() => {
    const token = localStorage.getItem("auth_token");
    if (!token) {
      navigate("/landing");
    }
  }, [navigate]);
  return (
    <div
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed",
        backgroundPosition: "center",
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        color: "white",
      }}
    >
      <div style={{ color: "white", textAlign: "center" }}>
        <br /><br />
        <h1 style={{ fontSize: "4rem", marginBottom: "1rem" }}> Welcome, {username} </h1>
        <div style={{ display: "flex", justifyContent: "space-between", width: "70%", margin: "2rem auto" }}>
          <div style={{ textAlign: "center" }}>
            <SearchIcon style={{ fontSize: "6rem" }} />
            <p style={{ fontSize: "1.5rem" }}>Search & Compare Stocks</p>
            <p>
              Effortlessly search, compare, and analyse stock data, all at the click of a button!
            </p>
          </div>
          <div style={{ textAlign: "center", paddingLeft: "2rem" }}>
            <BarChartIcon style={{ fontSize: "6rem" }} />
            <p style={{ fontSize: "1.5rem" }}>Visualise Stock Trends</p>
            <p>
              Utilise intuitive graphs to analyse complex data, allowing you to
              discover trends and see the bigger picture.
            </p>
          </div>
          <div style={{ textAlign: "center", paddingLeft: "2rem" }}>
            <CompareArrowsIcon style={{ fontSize: "6rem" }} />
            <p style={{ fontSize: "1.5rem" }}>Side-by-Side Comparisons</p>
            <p>
              Compare key metrics and graphs of multiple stocks to find the best
              investment option.
            </p>
          </div>
        </div>

        <br />

        <Button variant="contained" color="error" onClick={handleLogout}>
          Log Out
        </Button>
        <br />
        <div style={{ display: "flex", justifyContent: "center" }}>
          <img
            src={pricingImage}
            alt="Pricing"
            style={{
              maxWidth: "70%",
              height: "auto",
              marginRight: "2rem",
            }}
          />
        </div>
        <div style={{ display: "flex", justifyContent: "center" }}>
          <img
            src={paymentImage}
            alt="Payment"
            style={{
              maxWidth: "30%",
              height: "auto",
            }}
          />
        </div>
        <Routes>
          <Route path="/landing" element={<LandingPage/>} />
        </Routes>
      </div>
    </div>
  );
};

export default Dashboard;
