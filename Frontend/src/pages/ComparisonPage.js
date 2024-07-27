import React, { useState, useEffect } from "react";
import axios from "axios";
import Chart from "chart.js/auto";
import { CircularProgress, Tooltip} from "@mui/material";
import InfoIcon from '@mui/icons-material/Info';
import backgroundImage from "./background.jpg";
import logo from "../transparent_logo.png";
import LoginPopUp from "./LoginPopUp.js";

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

const StockComparison = () => {
  const [stocks, setStocks] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sentimentData, setSentimentData] = useState([]);
  const [filteredSymbols, setFilteredSymbols] = useState([]);
  const [showErrorPopup, setShowErrorPopup] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [openLoginPopup, setOpenLoginPopup] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      setOpenLoginPopup(true);
    }
  }, []); 

  const handleCloseLoginPopup = () => {
    setOpenLoginPopup(false);
  };
  
  const fetchData = async () => {
    setIsLoading(true);
    setSentimentData([]);
    const stockSymbols = stocks.split(",").map((symbol) => symbol.trim());
    const filtered = stockSymbols.filter(sym => sym.endsWith('.AX')).map(sym => sym.replace('.AX', ''));
    setFilteredSymbols(filtered);

    try {

      const promise = stockSymbols.map(symbol =>
        axios.get(
          `https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/retrieve`,
          {
            params: {
              file: "preprocessing-final",
              symbol,
              start_date: startDate,
              end_date: endDate,
            },
          }
        )
      );

      const responses = await Promise.all(promise);
      const stockDataStrings = responses.map((response) => response.data);
      const stockData = stockDataStrings.map((str) => JSON.parse(str));

      let sentimentResponses = [];
      if (filtered.length > 0) {
        const sentimentPromises = filtered.map(symbol =>
          axios.get(`https://676tg4mqw9.execute-api.ap-southeast-2.amazonaws.com/dev/stocks/${symbol}/sentiment`)
        );
  
        const sentimentResults = await Promise.allSettled(sentimentPromises);
        sentimentResponses = sentimentResults
          .filter(response => response.status === 'fulfilled')
          .map(response => response.value.data);
  
        const errors = sentimentResults
          .filter(response => response.status === 'rejected')
          .map(response => response.reason.config.params.symbol);
        if (errors.length > 0) {
          setErrorMessage(`No sentiment data found for the entered stock(s): ${errors.join(', ')}`);
          setShowErrorPopup(true);
        }
      }

      if (
        typeof stockData[0] === "object" &&
        Array.isArray(stockData[0].events)
      ) {
        const chartDataOpen = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.open),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataHigh = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.high),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataLow = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.low),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataClose = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.close),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataVolume = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.volume),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataAvgDaily = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.average_daily_price),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataPrRange = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.price_range),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataMA7 = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.moving_average_7_days),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataMA14 = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.moving_average_14_days),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        const chartDataMA30 = {
          labels: stockData[0].events.map((item) => item.timestamp),
          datasets: stockData.map((data, index) => ({
            label: stockSymbols[index],
            data: data.events.map((item) => item.moving_average_30_days),
            borderColor: "#" + ((Math.random() * 0xffffff) << 0).toString(16),
            fill: false,
          })),
        };

        setChartData("myChartOpen", chartDataOpen, "Open Prices", "Date", "Stock Price");
        setChartData("myChartHigh", chartDataHigh, "High Prices", "Date", "Stock Price");
        setChartData("myChartLow", chartDataLow, "Low Prices", "Date", "Stock Price");
        setChartData("myChartClose", chartDataClose, "Close Prices", "Date", "Stock Price");
        setChartData("myChartVolume", chartDataVolume, "Volume", "Date", "Stock Volume");
        setChartData("myChartAvgDaily", chartDataAvgDaily, "Average Daily Price", "Date", "Stock Price");
        setChartData("myChartPrRange", chartDataPrRange, "Price Range", "Date", "Stock Range");
        setChartData("myChartMA7", chartDataMA7, "Moving Averages 7 days", "Date", "Stock Price");
        setChartData("myChartMA14", chartDataMA14, "Moving Averages 14 days", "Date", "Stock Price");
        setChartData("myChartMA30", chartDataMA30, "Moving Averages 30 days", "Date", "Stock Price");

        setSentimentData(sentimentResponses);
      } else {
        console.error("Data is not in the expected format:", stockData[0]);
        setShowErrorPopup(true);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("An error occurred while fetching data.");
      setShowErrorPopup(true);
    }
    setIsLoading(false);
  };

  const renderSentimentTable = () => {
    if (sentimentData.length > 0 && sentimentData.every(data => data.events && data.events.length > 0)) {
      return (
        <div className="sentiment-analysis-box">
          {sentimentData.map((data, index) => (
            <div key={index}>
              <h3>Latest Sentiment Analysis for {filteredSymbols[index]}</h3>
              <table className="sentiment-table">
                <thead>
                  <tr>
                    <th>Article Title</th>
                    <th className="positive">Positive</th>
                    <th className="neutral">Neutral</th>
                    <th className="negative">Negative</th>
                    <th>Compound</th>
                    <th>Subjectivity</th>
                    <th>Polarity</th>
                    <th>Published</th>
                  </tr>
                </thead>
                <tbody>
                  {data.events.map((event, idx) => (
                    <tr key={idx}>
                      <td>{event.attribute.article_title}</td>
                      <td className={event.attribute.pos > 0 ? "positive" : ""}>{event.attribute.pos.toFixed(3)}</td>
                      <td className={event.attribute.neu > 0 ? "neutral" : ""}>{event.attribute.neg.toFixed(3)}</td>
                      <td className={event.attribute.neg > 0 ? "negative" : ""}>{event.attribute.neg.toFixed(3)}</td>
                      <td>{event.attribute.compound.toFixed(3)}</td>
                      <td>{event.attribute.subjectivity.toFixed(3)}</td>
                      <td>{event.attribute.polarity.toFixed(3)}</td>
                      <td>{new Date(event.attribute.published).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
        </div>
      );
    }
    return null;
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

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!stocks || !startDate || !endDate) {
      setErrorMessage("Please fill in all fields.");
      setShowErrorPopup(true);
      return;
    }
    fetchData();
  };

  const renderStockInfoTooltip = () => {
    return (
      <Tooltip title="Sentiment analysis supported for stocks on the ASX, use the .AX suffix (e.g- WOW.AX for Woolworths).">
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
      <div className="chart-form-container">
        <div>
          <LoginPopUp open={openLoginPopup} handleClose={handleCloseLoginPopup} />
          <h1 style={{ display: 'inline-block' }}>Compare Stocks {renderStockInfoTooltip()}</h1>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label>
                Stock Tickers (comma-separated):
                <input
                  type="text"
                  placeholder="eg: GOOG, AAPL, WOW.AX"
                  value={stocks}
                  onChange={(e) => setStocks(e.target.value)}
                  required
                />    
              </label>
            </div>
            <div className="input-group">
              <label>
                Start Date:
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  required
                />
              </label>
            </div>
            <div className="input-group">
              <label>
                End Date:
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  required
                />
              </label>
            </div>
            <div className="input-group">
              <button type="submit">Compare</button>
            </div>
          </form>
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
        <br></br>
      </div>
      <br></br>
      {sentimentData.length > 0 && !isLoading && (
        <div className="sentiment-analysis-container" style={{ marginTop: '20px', padding: '20px', backgroundColor: 'white', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
          {renderSentimentTable()}
        </div>
      )}
      <div className="chart-container">
        { stocks && (
          <>
            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartOpen"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: This graph displays the opening prices of the selected stocks over the specified time range. Opening prices represent the first traded prices of the stocks at the beginning of each trading day.</p>
                <p><b>Positive Signs</b>: A stable or increasing trend in opening prices can indicate investor confidence or positive market sentiment towards the stock.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartHigh"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: The high prices graph shows the highest traded prices of the selected stocks within each trading day.</p>
                <p><b>Positive Signs</b>: Rising high prices can signify increasing demand for the stock and may indicate potential upward momentum.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartLow"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: This graph illustrates the lowest traded prices of the selected stocks during each trading day.</p>
                <p><b>Positive Signs</b>: Consistently high low prices might suggest that the stock is experiencing strong support levels, potentially indicating a robust market for the stock.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartClose"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: The close prices graph represents the final traded prices of the selected stocks at the end of each trading day.</p>
                <p><b>Positive Signs</b>: A consistent or rising trend in closing prices is generally considered a positive sign, suggesting that the stock is performing well over time.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartVolume"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: This graph depicts the trading volume of the selected stocks, representing the total number of shares traded within each trading day.</p>
                <p><b>Positive Signs</b>: Increasing volume alongside price movement can validate the strength of a trend. High volume during upward price movements can indicate strong buying interest.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartAvgDaily"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: The average daily price graph showcases the average traded price of the selected stocks for each trading day.</p>
                <p><b>Positive Signs</b>: A rising average daily price can indicate increasing value and potential profitability of the stock.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartPrRange"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: This graph illustrates the difference between high and low prices of the selected stocks during each trading day, representing the price volatility.</p>
                <p><b>Positive Signs</b>: A narrowing price range over time can suggest reduced volatility and increased stability in the stock's price movement.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartMA7"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: This graph displays the 7-day moving averages of the selected stocks, smoothing out short-term price fluctuations to identify trends.</p>
                <p><b>Positive Signs</b>: Prices above the 7-day moving average can indicate an uptrend, while prices below can suggest a downtrend. Crossovers of moving averages can also signal potential trend changes.</p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartMA14"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: Similar to the 7-day moving averages, this graph shows the 14-day moving averages of the selected stocks.</p>
                <p><b>Positive Signs</b>: Consistent alignment of the 14-day moving average with the stock's price </p>
              </div>
            </div>

            <div className="chart-item">
              <div className="chart-card">
                <canvas id="myChartMA30"></canvas>
              </div>
              <div className="chart-description">
                <p><b>Meaning</b>: This graph presents the 30-day moving averages of the selected stocks, providing a longer-term perspective on price trends.</p>
                <p><b>Positive Signs</b>: Prices trending above the 30-day moving average can indicate a bullish market sentiment, while prices below may suggest a bearish sentiment.</p>
              </div>
            </div>
          </>
        )}
              {showErrorPopup && (
        <ErrorPopup
          show={showErrorPopup}
          message={errorMessage}
          onClose={() => setShowErrorPopup(false)}
        />
      )}
      </div>
    </div>
  );
};

export default StockComparison;
