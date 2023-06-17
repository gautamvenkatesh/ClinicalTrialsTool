import React from 'react';
import logo from './logo.svg';
import './App.css';

import Search  from './pages/Search';
import NewTrials  from './pages/NewTrials';
import SearchResults from './pages/SearchResults';
import NavBar from './components/NavBar';

import {Routes, Route, Link} from 'react-router-dom';


function App() {
  return (
    <>
    <NavBar/>
    <Routes>

      <Route path="/" element={<NewTrials/>} />
      <Route path="/search" element={<Search/>} />
      <Route path="/results" element={<SearchResults/>} />
    </Routes>
    </>

  );
}

export default App;
