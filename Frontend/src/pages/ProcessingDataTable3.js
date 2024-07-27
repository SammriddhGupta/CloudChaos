import React from 'react';

const ProcessingDataTable3 = ({ data }) => {
  const formatData = (value) => {
    return typeof value === 'number' ? value.toFixed(2) : (value || value === 0 ? value : 'N/A');
  };  
    
  return (
    <div className="table-container">
      <h2 style={{color: 'white'}}>Stock Price Data</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Open (USD)</th>
            <th>High (USD)</th>
            <th>Low (USD)</th>
            <th>Close (USD)</th>
            <th>Volume</th>
            <th>Daily Return (%)</th>
            <th>Average Daily Price (USD)</th>
            <th>Price Range (USD)</th>
            <th>Moving Average 7 Days (USD)</th>
            <th>Moving Average 14 Days (USD)</th>
            <th>Moving Average 30 Days (USD)</th>

          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{formatData(item.timestamp)}</td>
              <td>{formatData(item.open)}</td>
              <td>{formatData(item.high)}</td>
              <td>{formatData(item.low)}</td>
              <td>{formatData(item.close)}</td>
              <td>{formatData(item.volume)}</td>
              <td>{formatData(item.daily_return)}</td>
              <td>{formatData(item.average_daily_price)}</td>
              <td>{formatData(item.price_range)}</td>
              <td>{formatData(item.moving_average_7_days)}</td>
              <td>{formatData(item.moving_average_14_days)}</td>
              <td>{formatData(item.moving_average_30_days)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ProcessingDataTable3;
