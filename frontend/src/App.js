import React, { useState } from 'react';
import './App.css';
import {
    BrowserRouter,
    Routes,
    Route,
    Link
} from "react-router-dom";
import Main from "./page/Main"
import About from "./page/About"
import Spotify from './page/Spotify';
import Anlysis from './page/Anlysis'
import Contrast from './page/Contrast';
import ChordVS from './page/ChordVS'
import Structure from './page/Structure'
import Player from './page/Player';
export default function App() {
    const [sidebarOpen, setSidebarOpen] = useState(false);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

  return (
    <div>
        <BrowserRouter>
            <header>
                <p className='logo'>♪ Music Browser</p>
                <ul className='header-nav'>
                    <li><Link to="/" className="nav-link px-2">Home</Link></li>
                    <li><Link to="/player" className="nav-link px-2">Player</Link></li>
                    <li><Link to="/structure" className="nav-link px-2">Structure</Link></li>
                    <li><Link to="/anlysis" className="nav-link px-2">Anlysis</Link></li>
                    <li><Link to="/contrast" className="nav-link px-2">Contrast</Link></li>
                    <li><Link to="/chordvs" className="nav-link px-2">Chord Visualizer</Link></li>
                    <li><Link to="/spotify" className="nav-link px-2">Spotify API</Link></li>
                    <li><Link to="/about" className="nav-link px-2">About</Link></li>
                </ul>

            </header>
  
            <Routes>
                <Route path='/' element={<Main/>}/>
                <Route path='/player' element={<Player/>}/>
                <Route path='/about' element={<About/>}/>
                <Route path='/spotify' element={<Spotify/>}/>
                <Route path='/anlysis' element={<Anlysis/>}/>
                <Route path='/contrast' element={<Contrast/>}/>
                <Route path='/chordvs' element={<ChordVS/>}/>
                <Route path='/structure' element={<Structure/>}/>
            </Routes>
            <footer>Music Browser</footer>

        </BrowserRouter>

    </div>
  )
}
