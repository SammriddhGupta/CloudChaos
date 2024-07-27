import { render, screen, fireEvent } from '@testing-library/react';
import App from './App.js';

describe('App', () => {
  it('renders the navigation links', () => {
    render(<App />);
    
    expect(screen.getByAltText('Logo')).toBeInTheDocument();
    expect(screen.getByText('Collection')).toBeInTheDocument();
    expect(screen.getByText('Preprocessing')).toBeInTheDocument();
    expect(screen.getByText('Comparison')).toBeInTheDocument();
  });

  /* it('navigates to the Collection page', () => {
    render(<App />);
    
    const collectionLink = screen.getByText('Collection');
    fireEvent.click(collectionLink);
    
    const collectDataText = await screen.getAllByText('Collect Data')[0];  // Get the first matching element
    expect(collectDataText).toBeInTheDocument();
  });

  it('navigates to the Preprocessing page', () => {
    render(<App />);
    
    const preprocessingLink = screen.getByText('Preprocessing');
    fireEvent.click(preprocessingLink);
    
    const preprocessingPageText = await screen.getByText('Preprocessing Page');  // Update this to match the actual text in PreprocessingPage
    expect(preprocessingPageText).toBeInTheDocument();
  });

  it('navigates to the Comparison page', () => {
    render(<App />);
    
    const comparisonLink = screen.getByText('Comparison');
    fireEvent.click(comparisonLink);
    
    const comparisonPageText = await screen.getByText('Comparison Page');  // Update this to match the actual text in ComparisonPage
    expect(comparisonPageText).toBeInTheDocument();
  });

  it('navigates to the Landing page', () => {
    render(<App />);
    
    const landingLink = screen.getByText('Back to Landing');
    fireEvent.click(landingLink);
    
    const landingPageText = screen.getByText('Welcome to Landing Page');  // Update this to match the actual text in LandingPage
    expect(landingPageText).toBeInTheDocument();
  }); */
});
