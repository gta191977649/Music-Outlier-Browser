import React from 'react'
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
export default function App() {
  return (
    <div>
        <BrowserRouter>
            <header>
                <p className='logo'>♪ Music Browser</p>
                <ul className='header-nav'>
                    <li><Link to="/" className="nav-link px-2">Home</Link></li>
                    <li><Link to="/spotify" className="nav-link px-2">Spotify API</Link></li>
                    <li><Link to="/about" className="nav-link px-2">About</Link></li>
                    <li><Link to="/anlysis" className="nav-link px-2">Anlysis</Link></li>
                </ul>
            </header>
            <Routes>
                <Route path='/' element={<Main/>}/>
                <Route path='/about' element={<About/>}/>
                <Route path='/spotify' element={<Spotify/>}/>
                <Route path='/anlysis' element={<Anlysis/>}/>
            </Routes>
        </BrowserRouter>
    </div>
  )
}
