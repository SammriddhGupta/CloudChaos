import React from "react";
import backgroundImage from "./background.jpg";
import { Link } from "react-router-dom";
import { Button } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import BarChartIcon from "@mui/icons-material/BarChart";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";
import pricingImage from "../PaymentModel.png";
import paymentImage from "../Payment.png";

const LandingPage = () => {
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
        <br /> <br />
        <p style={{ fontSize: "1.5rem", marginBottom: "-2rem" }}>Welcome to</p>
        <h1 style={{ fontSize: "4rem", marginBottom: "1rem" }}>CloudChaos</h1>
        <p style={{ fontSize: "1.2rem", fontWeight: "bold" }}>
          Effortlessly analyse and make informed investment decisions!
        </p>
        <br />
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            width: "70%",
            margin: "2rem auto",
          }}
        >
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

        <Link to="https://cloudchaos.auth.ap-southeast-2.amazoncognito.com/login?client_id=1gqsqb0d5vh6osuuc2950ub8v9&response_type=token&scope=email+openid+phone&redirect_uri=https://main.d332b7vcir4cg5.amplifyapp.com/redirect" className="signup-button">
          <Button variant="contained" color="secondary"   type="button" className="form-button">Sign Up</Button>
        </Link>
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
      </div>
    </div>
  );
};

export default LandingPage;
