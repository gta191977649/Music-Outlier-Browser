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
    const [waveFile, setWaveFile] = useState(null);
    const [analysisResponse, setAnalysisResponse] = useState(null);
    const [wait,setWait] = useState(false);
    const [currentPosition, setCurrentPosition] = useState(0); 
    const [currentChord, setCurrentChord] = useState("N/A"); 
    const [audio, setAudio] = useState(null);
    const [audioTime, setAudioTime] = useState(0);
    const [chordMapView, setChordMapView] = useState(false);
    const [wavesurfer, setWavesurfer] = useState(null)

    


    const handlePlay = () => {
        if (audio) {
            audio.play();
        }
    };

    const handlePause = () => {
        if (audio) {
            audio.pause();
        }
    };

    const handleReset = () => {
        if (audio) {
            audio.currentTime = 0;
        }
    };

    const handleTimeUpdate = () => {
        
        const currentTime = audio.currentTime;
        setAudioTime(currentTime);

        const chordTimings = analysisResponse.chord_data.chord_timing_ls;
        for (let i = 0; i < chordTimings.length; i++) {
            const [startTime, , endTime] = chordTimings[i];
            if (currentTime >= startTime && currentTime <= endTime) {
                setCurrentPosition(i); // Set the position to the index of the current chord
                setCurrentChord(analysisResponse.chord_data.chord_name[i])
                break; // Exit the loop once the correct index is found
            }
        }
     
    };
    // Handle file selection
    const handleFileSelect = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            console.log(selectedFile.name); // For debugging
        }
    };

    const handleWaveFileSelect = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setWaveFile(selectedFile);
            const audioUrl = URL.createObjectURL(selectedFile);
            setAudio(new Audio(audioUrl));
            
        }
    };

    useEffect(() => {
        if (audio) {
            audio.addEventListener('timeupdate', handleTimeUpdate);

            // Clean up
            return () => {
                audio.removeEventListener('timeupdate', handleTimeUpdate);
            };
        }
    }, [audio,analysisResponse]);

    // Handle file upload
    const handleFileUpload = async () => {
        if (file) {
            const formData = new FormData();
            const csrftoken = getCookie('csrftoken')
            formData.append('file', file);
            setWait(true);
            try {
                //const URL = "./api/midi-upload/"
                const URL = "http://localhost:8000/api/midi-upload/"
                const response = await axios.post(URL, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': csrftoken
                    }
                });
                setAnalysisResponse(response.data.chords);
                setWait(false);
            } catch (error) {
                console.error('Error uploading file:', error);
                setWait(false);
            }
        }
    };

    const renderPlot = (title,values_data,color) => {

        const data = {
            labels: values_data.map((_, index) => `${index + 1}`),
         
            datasets: [
                {
                    label: title,
                    data: values_data,
                    fill: false,
                    backgroundColor: color,
                    borderColor: color,
                    borderWidth: 1.5,
                    pointRadius: 2,
                    tension: 0.1,
                    stepped: true,
                },
            ],
        };

        const options = {
            maintainAspectRatio: false,
            responsive: true,
            
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                annotation: {
                    annotations: {
                        line1: {
                            type: 'line',
                            xMin: currentPosition,
                            xMax: currentPosition,
                            borderColor: '#e72222',
                            borderWidth: 2,
                        }
                    }
                },
                zoom: {
                    zoom: {
                      wheel: {
                        enabled: true,
                      },
                      pinch: {
                        enabled: true
                      },
                      mode: 'xy',
                    }
                },
                legend: {
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            family:"JR",
                            size: 14
                        }
                    }
                }
            }
        };

        return (
            <div>
                <Line data={data} options={options} height={200} />
            </div>
        );
    }
    const renderResponse = () => {
        return (
            <>
                <WavesurferPlayer
                    height={100}
                    waveColor="blue"
                    url={URL.createObjectURL(waveFile)}
                />
                {renderPlot("Tension Change",analysisResponse.chord_data.tension_change,"#E72222")}
                {renderPlot("Color Change",analysisResponse.chord_data.color_change,"#00965F")}
                {renderPlot("Theta (Chord) Change",analysisResponse.chord_data.chord_theta,"#1A43BF")}
            </>
    

        )
    };
    const onReady = (ws) => {
        setWavesurfer(ws)
    }

    return (
      
        <div className='container mt-5'>
            <h2>Pattern Analysis { wait ? <span class="spinner-border" role="status"></span> :""}</h2>

            <div className="card">
                <div className="card-body">
                    <input
                        type="file"
                        id="fileInput"
                        style={{ display: 'none' }}
                        onChange={handleFileSelect}
                        accept=".mid"  // Specify accepted file extension
                    />
                    <label
                        htmlFor="fileInput"
                        style={{ textAlign: 'center', color: "#e72222", fontWeight: "bold", cursor: "pointer" }}
                    >
                        {file ? `[ ${file.name} ]` : "[ DROP MIDI FILE ]"}
                    </label>
                    <input
                        type="file"
                        id="fileInput2"
                        style={{ display: 'none' }}
                        onChange={handleWaveFileSelect}
                        accept=".wav,.mp3" 
                    />
                    <label
                        htmlFor="fileInput2"
                        style={{ textAlign: 'center', color: "#343a40", fontWeight: "bold", cursor: "pointer" }}
                    >
                        {waveFile ? `[ ${waveFile.name} ]` : "[ DROP REFERENCE FILE ]"}
                    </label>
                    <p>
                        <small>MIDIファイルとオーディオファイルのタイミングが一致しているかご確認お願いします。<br/>時間が異なる曲には対応しておりませんので、ご了承ください。</small>
                    </p>
                    <button className='btn btn-custom' onClick={handleFileUpload} style={{ display: 'block', margin: '10px auto', padding: '10px 20px' }}>
                        Upload and Analyze
                    </button>
                </div>
            </div>
            {/* Audio controls */}
            <div className="card mt-4">
                <div className="card-header">
                    CONTROL [TIME:{audioTime},BAR:{currentPosition},CHORD: {currentChord}]
                </div>
                <div className="btn-group" role="group" aria-label="Basic example">
                    <button type="button" className="btn btn-nurupo" onClick={handlePlay}>PLAY</button>
                    <button type="button" className="btn btn-nurupo" onClick={handlePause}>PAUSE</button>
                    <button type="button" className="btn btn-nurupo" onClick={handleReset}>RESET</button>
                </div>

            </div>


            <div className="card mt-4">
            
                <div className="card-header">
                    分析  {analysisResponse ? `Key:${analysisResponse.key} ${analysisResponse.mode},Tempo:${analysisResponse.tempo} BPM` :""}
                </div>
                <div className="card-body">
                    {analysisResponse !== null ? renderResponse() : '[ N/A ]'}
                </div>
            </div>
            <div className="card mt-4">
                <div className="card-header" onClick={()=>{setChordMapView(!chordMapView)}}>
                    CHORD MAP {!chordMapView ? <small>[CLICK EXPLAND ▼]</small> : ""}
                </div>
                <Collapse isOpened={chordMapView}>
                <div class="d-flex flex-wrap">
                    {analysisResponse !== null ? analysisResponse.chord_data.chord_name.map((chord,i)=>{
                        if (i == currentPosition) {
                            return(
                                <div key={i} class="p-2 bd-highlight flex-chord" style={{color:"#e72222",background:"#ffdddd",fontWeight:"bold"}}>
                                    {chord}
                                    <br/>
                                    <small>
                                        {analysisResponse.chord_data.chord_theta[i].toFixed(2)}
                                    </small>
                                </div>
                            )
                        } else {
                            return(
                                <div key={i} class="p-2 bd-highlight flex-chord" >
                                    {chord}
                                    <br/>
                                    <small>
                                        {analysisResponse.chord_data.chord_theta[i].toFixed(2)}
                                    </small>
                                </div>
                            )
                        }
                        
                    }): "[ N/A ]"}
                  
                </div>
                </Collapse>
            </div>
        </div>
    );
}
