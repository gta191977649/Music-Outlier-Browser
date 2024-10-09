import React, { useState,useRef,useEffect,useMemo } from 'react';
import {Collapse} from 'react-collapse';

import axios from 'axios';
import { getCookie } from '../utils/cookie';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Line,Bar } from 'react-chartjs-2';
  
import annotationPlugin from 'chartjs-plugin-annotation';
import WavesurferPlayer from '@wavesurfer/react'


// Registering components and plugin for Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  annotationPlugin
);
ChartJS.defaults.font.family = 'JR'; 
export default function Analysis() {
    const [file, setFile] = useState(null);
    const [wait,setWait] = useState(false);
    const [audio, setAudio] = useState(null);
    const [response,setResponse] = useState(null)
    // Handle file selection
    const handleFileSelect = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            console.log(selectedFile.name); // For debugging
        }
    };

    const playAtSegment = (segmentIdx) => {
        let start = response.segments[segmentIdx][0]
        console.log(`start time ${start}`)
        audio.currentTime = start;
        audio.play();
    }

    const playAtSection = (sectionIdx) => {
        let start = response.boundaries[sectionIdx]
        console.log(`start time ${start}`)
        audio.currentTime = start;
        audio.play();
    }

    const stop = () => {
        audio.pause();
        audio.currentTime = 0;
    }
    // Deal with response
    useEffect(() => {
        if(response) {
            const objectURL = URL.createObjectURL(file);
            setAudio(new Audio(objectURL));
            console.log(response)
        }
    }, [response]);

    // Handle file upload
    const handleFileUpload = async () => {
        if (file) {
            const formData = new FormData();
            const csrftoken = getCookie('csrftoken')
            formData.append('file', file);
            setWait(true);
            try {
                //const URL = "./api/midi-upload/"
                const URL = "http://localhost:8000/api/structure-upload/"
                const response = await axios.post(URL, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': csrftoken
                    }
                });
                setResponse(response.data)
                setWait(false);
            } catch (error) {
                console.error('Error uploading file:', error);
                setWait(false);
            }
        }
    };


    return (
      
        <div className='container mt-5'>
            <h2>Structure Analysis { wait ? <span class="spinner-border" role="status"></span> :""}</h2>

            <div className="card">
                <div className="card-body">
                    <input
                        type="file"
                        id="fileInput"
                        style={{ display: 'none' }}
                        onChange={handleFileSelect}
                        accept=".mp3"  // Specify accepted file extension
                    />
                    <label
                        htmlFor="fileInput"
                        style={{ textAlign: 'center', color: "#e72222", fontWeight: "bold", cursor: "pointer" }}
                    >
                        {file ? `[ ${file.name} ]` : "[ DROP REFERENCE FILE ]"}
                    </label>
                   
                    <button disabled={file == null} className='btn btn-custom' onClick={handleFileUpload} style={{ display: 'block', margin: '10px auto', padding: '10px 20px' }}>
                        Upload and Analyze
                    </button>
                </div>
            </div>

            
           
        </div>
    );
}
