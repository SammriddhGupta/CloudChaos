import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ComparisonPage from './ComparisonPage';

test('renders Collect Data header', () => {
  render(
    <MemoryRouter>
      <ComparisonPage />
    </MemoryRouter>
  );
  const headerElement = screen.getAllByText('Compare Stocks')[0];
  expect(headerElement).toBeInTheDocument();
});