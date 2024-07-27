/* eslint-disable no-unused-vars */
/* eslint-disable react-hooks/exhaustive-deps */

// PredictionPage.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import Chart from "chart.js/auto";
import backgroundImage from "./background.jpg";
import { CircularProgress, Tooltip } from "@mui/material";
import Typography from '@mui/material/Typography';
import InfoIcon from '@mui/icons-material/Info';
import { Button } from "@mui/material";
import LoginPopUp from "./LoginPopUp.js";
import logo from "../transparent_logo.png";

function ErrorPopup({ show, message, onClose }) {
  const [isFadingOut, setIsFadingOut] = useState(false);

  useEffect(() => {
    if (show) {
      setIsFadingOut(false);
    }
  }, [show]);

  const handleClose = () => {
    setIsFadingOut(true);
    setTimeout(() => {
      onClose();
    }, 500);
  };

  if (!show && !isFadingOut) return null;

  return (
    <div className={`error-popup ${isFadingOut ? 'fade-out' : ''}`}>
      <img src={logo} alt="Logo" />
      <div className="error-content">
        <h2>Error</h2>
        <p>{message}</p>
      </div>
      <button className="close-button" onClick={handleClose}>&times;</button>
    </div>
  );
}

function PredictionPage() {
  const [symbol, setSymbol] = useState("");
  const [start_date, setStartDate] = useState("");
  const [end_date, setEndDate] = useState("");
  const [number_of_days, setDays] = useState("");
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showErrorPopup, setShowErrorPopup] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [openLoginPopup, setOpenLoginPopup] = useState(false);
  const [companyName, setCompanyName] = useState("");


  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      setOpenLoginPopup(true);
    }
  }, []); 

  const handleCloseLoginPopup = () => {
    setOpenLoginPopup(false);
  };

  const handleCompanyName = async () => {
    if (!symbol) return;
    const endpoint = `https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04_name?symbol=${symbol}`;
    try {
      const response = await axios.get(endpoint);
      setCompanyName(response.data);
    } catch (error) {
      console.error("Error fetching company name:", error);
      setCompanyName("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    await handleCompanyName();
    const endpoint = `https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04_prediction`;
    const startDate = "2022-01-01";
    const endDate = "2024-04-15";
    try {
      const response = await axios.get(endpoint, {
        params: { symbol, start_date: startDate, end_date: endDate, number_of_days },
        withCredentials: false,
      });

      // Parse the JSON string into an object
      const parsedData = response.data;

      if (Object.keys(parsedData).length === 0) {
        setErrorMessage("No data found for the given stock ticker and or date range.");
        setShowErrorPopup(true);
        setData({});
      } 
      else {
        setData(parsedData);
      }
      
    } catch (error) {
      let errMsg = "An unexpected error occurred.";
      if (error.response) {
        errMsg = error.response.data.body || "Error: " + error.response.statusText;
      } else if (error.request) {
        errMsg = "Failed to get a response from the server. Check for valid date range and entered fields.";
      }
      setErrorMessage(errMsg);
      setShowErrorPopup(true);
      setData([]);
      /* console.error("Error config:", error.config); */
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle downloading the JSON data
  const handleDownload = () => {
    const fileName = `${symbol}-${start_date}-${end_date}`;
    const json = JSON.stringify(data);
    const blob = new Blob([json], { type: 'application/json' });
    const href = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = href;
    link.download = `${fileName}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const setChartData = (chartId, data, title, xAxisLabel, yAxisLabel) => {
    const ctx = document.getElementById(chartId).getContext("2d");

    if (!window[chartId]) {
      window[chartId] = new Chart(ctx, {
        type: "line",
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: title,
              font: {
                size: 18, 
              },
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: xAxisLabel,  
              },
            },
            y: {
              title: {
                display: true,
                text: yAxisLabel,  
              },
            },
          },
        },
      });
    } else {
      if (window[chartId] instanceof Chart) {
        window[chartId].destroy();
      }
      window[chartId] = new Chart(ctx, {
        type: "line",
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: title,
              font: {
                size: 18, 
              },
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: xAxisLabel,  
              },
            },
            y: {
              title: {
                display: true,
                text: yAxisLabel,  
              },
            },
          },
        },
      });
    }
  };

  useEffect(() => {
    if (Object.keys(data).length > 0) {

      const chartData = {
        labels: Object.keys(data),
        datasets: [{
          label: symbol,
          data: Object.values(data),
          borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
          fill: false,
        }],
      };

      setChartData("myChart", chartData, "Prediction", "Date", "Stock Price");
    }
  }, [data]);

  const RenderStockInfoTooltip = () => {
    return (
      <
        Tooltip title=<React.Fragment>
          <Typography color="inherit">Warning</Typography>This prediction model is based on a simple linear regression using historical stock data.<br></br>
          <b>{"Model Used:"}</b> Linear Regression <br></br>
          <b>{"Date Range:"}</b> 2022-01-01 to 2024-04-15 (2 years)<br></br>
        </React.Fragment>
        >
        
          <InfoIcon style={{ fontSize: '20px', marginLeft: '5px', cursor: 'pointer', fill: '#50277a' }} />
        </Tooltip>
    );
  };

  return (
    <div
      className="dashboard"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundAttachment: "fixed",
        backgroundPosition: "center",
        minHeight: "100vh",
      }}
    >
      <div className="predict-form-container">
        <h1 style={{ display: 'inline-block' }}>Predict Prices <RenderStockInfoTooltip/>  </h1>
        
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="symbol">Stock Ticker</label>
            <input
              id="symbol"
              type="text"
              className="form-control"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value)}
              placeholder="eg: GOOG"
            />
          </div>
          <div className="input-group">
            <label htmlFor="symbol">Number of days you want to predict</label>
            <input
              id="number_of_days"
              type="number"
              className="form-control"
              value={number_of_days}
              onChange={(e) => setDays(e.target.value)}
              placeholder="eg: 30, 90, 365"
            />
          </div>
          <div className="input-group">
            <button type="submit" className="form-button">
              Get Predictions
            </button>
          </div>
        </form>
        <div className="company-name">
          {companyName && (
            <p style={{color: 'black', fontWeight:"bold", padding: '0', margin:'0', textAlign: "center"}}>Viewing prediction for {companyName}</p>
          )}
        </div>
        {isLoading && (
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "30px",
              }}
            >
              <CircularProgress style={{ color: 'purple', padding:'5px' }} />
              <p>Loading...</p>
            </div>
          )}
      </div>

      <div className="chart-predict-container">
      {
        data && Object.keys(data).length > 0 && (
          <>
            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChart"></canvas>
              </div>
            </div>
          </>
        )
      }
      </div>


      <div className="download-container">
          <Button variant="contained" color="secondary"  onClick={handleDownload}>Download as JSON</Button>
      </div>
     
      <LoginPopUp open={openLoginPopup} handleClose={handleCloseLoginPopup} />
      {showErrorPopup && (
        <ErrorPopup
          show={showErrorPopup}
          message={errorMessage}
          onClose={() => setShowErrorPopup(false)}
        />
      )}
    </div>
    
  );
}

export default PredictionPage;
