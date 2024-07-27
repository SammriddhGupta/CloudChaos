import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import PreprocessingPage from './PreprocessingPage';

test('renders Collect Data header', () => {
  render(
    <MemoryRouter>
      <PreprocessingPage />
    </MemoryRouter>
  );
  const headerElement = screen.getAllByText('Preprocess Data')[0];
  expect(headerElement).toBeInTheDocument();
});

/* 
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import PreprocessingPage from './PreprocessingPage';

jest.mock('axios');

describe('PreprocessingPage', () => {
  beforeEach(() => {
    axios.get.mockResolvedValue({
      data: JSON.stringify({ events: [] }),
    });
  });

  it('renders the form and retrieves data', async () => {
    render(<PreprocessingPage />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText('Stock Symbol'), {
      target: { value: 'AAPL' },
    });
    fireEvent.change(screen.getByLabelText('Start Date'), {
      target: { value: '2022-01-01' },
    });
    fireEvent.change(screen.getByLabelText('End Date'), {
      target: { value: '2022-01-10' },
    });

    // Click the submit button
    fireEvent.click(screen.getByText('Retrieve Preprocessed Data'));

    // Wait for the API call to complete
    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledTimes(1);
    });

    expect(axios.get).toHaveBeenCalledWith(
      'https://kffxjq6hph.execute-api.ap-southeast-2.amazonaws.com/SE3011-24-F11A-04/retrieve',
      {
        params: {
          file: 'preprocessing-1',
          symbol: 'AAPL',
          start_date: '2022-01-01',
          end_date: '2022-01-10',
        },
        withCredentials: false,
      }
    );

    // Check if the data table is rendered
    const noDataMessage = screen.getByText('No data to display yet');
    expect(noDataMessage).toBeInTheDocument();
  });

  it('displays an error popup when no data is returned', async () => {
    axios.get.mockResolvedValue({
      data: JSON.stringify({ events: [] }),
    });

    render(<PreprocessingPage />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText('Stock Symbol'), {
      target: { value: 'AAPL' },
    });
    fireEvent.change(screen.getByLabelText('Start Date'), {
      target: { value: '2022-01-01' },
    });
    fireEvent.change(screen.getByLabelText('End Date'), {
      target: { value: '2022-01-10' },
    });

    // Click the submit button
    fireEvent.click(screen.getByText('Retrieve Preprocessed Data'));

    // Wait for the API call to complete
    await waitFor(() => {
      const errorMessage = screen.getByText('No data available for the specified parameters. Please check your inputs.');
      expect(errorMessage).toBeInTheDocument();
    });
  });

  it('displays an error popup when an unexpected error occurs', async () => {
    axios.get.mockRejectedValue(new Error('An unexpected error occurred.'));

    render(<PreprocessingPage />);

    // Fill out the form
    fireEvent.change(screen.getByLabelText('Stock Symbol'), {
      target: { value: 'AAPL' },
    });
    fireEvent.change(screen.getByLabelText('Start Date'), {
      target: { value: '2022-01-01' },
    });
    fireEvent.change(screen.getByLabelText('End Date'), {
      target: { value: '2022-01-10' },
    });

    // Click the submit button
    fireEvent.click(screen.getByText('Retrieve Preprocessed Data'));

    // Wait for the error popup to display
    await waitFor(() => {
      const errorMessage = screen.getByText('An unexpected error occurred.');
      expect(errorMessage).toBeInTheDocument();
    });
  });

  // Add more tests as needed
});
 */