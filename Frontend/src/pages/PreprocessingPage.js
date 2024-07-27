import React, { useState, useEffect } from "react";
import axios from "axios";
import ProcessingDataTable1 from "./ProcessingDataTable1.js";
import ProcessingDataTable2 from "./ProcessingDataTable2.js";
import ProcessingDataTable3 from "./ProcessingDataTable3.js";
import backgroundImage from "./background.jpg";
import { CircularProgress } from "@mui/material";
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

function PreprocessingPage() {
  const [symbol, setSymbol] = useState("");
  const [start_date, setStartDate] = useState("");
  const [end_date, setEndDate] = useState("");
  const [file, setDataType] = useState("preprocessing-1");
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

  const dataTypes = {
    preprocessing1: "preprocessing-1",
    preprocessing2: "preprocessing-2",
    preprocessingFinal: "preprocessing-final",
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

  useEffect(() => {
    setData([]);
  }, [file]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    await handleCompanyName();
    const endpoint = `https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/retrieve`;
    try {
      const response = await axios.get(endpoint, {
        params: { file, symbol, start_date, end_date },
        withCredentials: false,
      });

      const parsedData = JSON.parse(response.data);
      if (!parsedData.events || parsedData.events.length === 0) {
        setErrorMessage("No data available for the specified parameters. Please check your inputs.");
        setShowErrorPopup(true);
        setData([]);
      } else {
        setData(parsedData.events);
      }
    } catch (error) {
      let errMsg = "An unexpected error occurred.";
      if (error.response) {
        errMsg = error.response.statusText || errMsg;
        if (error.response.data && error.response.data.body) {
          errMsg = error.response.data.body;
        }
      } else if (error.request) {
        errMsg = "Failed to get a response from the server. Check for valid date range and entered fields.";
      }
      setErrorMessage(errMsg);
      setShowErrorPopup(true);
      setData([]);
    } finally {
      setIsLoading(false);
    }
  };


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

  const renderTable = () => {
    if (isLoading) {
      return (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '300px' }}>
          <CircularProgress style={{ color: 'purple', padding:'5px'  }} />
          <p style={{color: 'white'}}>Loading...</p>
        </div>
      );
    } else if (data.length > 0) {
      switch (file) {
        case dataTypes.preprocessing1:
          return <ProcessingDataTable1 data={data} />;
        case dataTypes.preprocessing2:
          return <ProcessingDataTable2 data={data} />;
        case dataTypes.preprocessingFinal:
          return <ProcessingDataTable3 data={data} />;
        default:
          return null;
      }
    } else {
      return <p style={{color: 'white'}}>No data to display yet</p>;
    }
  };

  return (
    <div className="content" style={{
      backgroundImage: `url(${backgroundImage})`,
      backgroundSize: "cover",
      backgroundRepeat: "no-repeat",
      backgroundAttachment: "fixed",
      backgroundPosition: "center",
      minHeight: "100vh",
    }}>
      <div className="form-container">
        <h1>Preprocess Data</h1>
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
              aria-label="Stock Ticker"
            />
          </div>
          <div className="input-group">
            <label htmlFor="startDate">Start Date</label>
            <input
              id="startDate"
              type="date"
              className="form-control"
              value={start_date}
              onChange={(e) => setStartDate(e.target.value)}
              aria-label="Start Date"
            />
          </div>
          <div className="input-group">
            <label htmlFor="endDate">End Date</label>
            <input
              id="endDate"
              type="date"
              className="form-control"
              value={end_date}
              onChange={(e) => setEndDate(e.target.value)}
              aria-label="End Date"
            />
          </div>
          <div className="input-group">
            <label htmlFor="file">Data Type</label>
            <select
              id="file"
              className="form-control"
              value={file}
              onChange={(e) => setDataType(e.target.value)}
              aria-label="Data Type"
            >
              {Object.entries(dataTypes).map(([key, value]) => (
                <option key={key} value={value}>
                  {value.split("-").join(" ").toUpperCase()}
                </option>
              ))}
            </select>
          </div>
          <div className="input-group">
            <button type="submit" className="form-button" aria-label="Retrieve Data">
              Retrieve Preprocessed Data
            </button>
          </div>
          <div className="company-name">
            {companyName && (
              <p style={{color: 'black', fontWeight:"bold", padding: '0', margin:'0', textAlign: "center"}}>Viewing preprocessed data for {companyName}</p>
            )}
          </div>
        </form>
      </div>
      {isLoading ? (
        <div style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "300px",
        }}>
          <CircularProgress style={{ color: 'purple', padding:'5px'  }} />
          <p style={{color: 'white'}}>Loading...</p>
        </div> 
      ) : renderTable()}
      <Button variant="contained" color="secondary" onClick={handleDownload} aria-label="Download Data as JSON">
        Download as JSON
      </Button>
      {showErrorPopup && (
        <ErrorPopup
          show={showErrorPopup}
          message={errorMessage}
          onClose={() => setShowErrorPopup(false)}
        />
      )}
      <LoginPopUp open={openLoginPopup} handleClose={handleCloseLoginPopup} />
    </div>
  );
}

export default PreprocessingPage;
