import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import NewTrials from '../pages/NewTrials';

test('renders learn react link', () => {
  render(<NewTrials />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
