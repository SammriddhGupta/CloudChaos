import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import CollectDataPage from './CollectDataPage';

test('renders Collect Data header', () => {
  render(
    <MemoryRouter>
      <CollectDataPage />
    </MemoryRouter>
  );
  const headerElement = screen.getAllByText('Collect Data')[0];
  expect(headerElement).toBeInTheDocument();
});

// Need to add more tests
