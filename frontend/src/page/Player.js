import React, { useState, useRef, useEffect } from 'react';
import { getCookie } from '../utils/cookie';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';

export default function Player() {
    const [file, setFile] = useState(null);
    const [wait, setWait] = useState(false);
    const [audio, setAudio] = useState(null);
    const [response, setResponse] = useState(null);
    const [currentTime, setCurrentTime] = useState(0); // State to track the current time of the audio
    const [duration, setDuration] = useState(0); // State to track the duration of the audio

    // Conversion function: Convert time in seconds to frame index
    const timeToFrameIndex = (currentTime, featureRate) => {
        return Math.floor(currentTime * featureRate);
    };

    // Handle file selection
    const handleFileSelect = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            console.log(selectedFile.name); // For debugging
        }
    };

    const play = () => {
        if (audio) {
            audio.play();
        }
    };

    const pause = () => {
        if (audio) {
            audio.pause();
        }
    };

    const reset = () => {
        if (audio) {
            audio.currentTime = 0;
            audio.pause();
        }
    };

    // Sync audio with the range input
    const handleRangeChange = (event) => {
        if (audio) {
            const newTime = event.target.value;
            audio.currentTime = newTime;
            setCurrentTime(newTime);
        }
    };

    // Deal with response
    useEffect(() => {
        if (response) {
            const objectURL = URL.createObjectURL(file);
            const audioElement = new Audio(objectURL);

            audioElement.addEventListener('loadedmetadata', () => {
                setDuration(audioElement.duration);
            });

            audioElement.addEventListener('timeupdate', () => {
                setCurrentTime(audioElement.currentTime);
            });

            setAudio(audioElement);
            console.log(response);

            return () => {
                audioElement.pause();
                audioElement.remove();
            };
        }
    }, [response, file]);

    // Handle file upload
    const handleFileUpload = async () => {
        if (file) {
            const formData = new FormData();
            const csrftoken = getCookie('csrftoken');
            formData.append('file', file);
            setWait(true);
            try {
                const URL = "http://localhost:8000/api/structure-upload/";
                const response = await axios.post(URL, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': csrftoken,
                    },
                });
                setResponse(response.data);
                setWait(false);
            } catch (error) {
                console.error('Error uploading file:', error);
                setWait(false);
            }
        }
    };

    const renderNoveltyCurve = () => {
        if (!response || !response.novelty_curve) {
            return null;
        }

        const currentFrame = timeToFrameIndex(currentTime, response.feature_rate); // Use the conversion function

        const option = {
            tooltip: {
                trigger: 'axis',
            },
            xAxis: {
                type: 'category',
                data: Array.from({ length: response.novelty_curve.length }, (_, i) => i),
                name: 'Frame Index',
            },
            yAxis: {
                type: 'value',
                name: 'Novelty Value',
            },
            grid: {
                left: '0%',
                right: '0%',
                top: '10%',
                bottom: '10%',
                containLabel: true,
            },
            series: [
                {
                    data: response.novelty_curve,
                    type: 'line',
                    smooth: true,
                    lineStyle: {
                        color: '#33B5E5', // Changed the line color to #33B5E5
                        width: 2,
                    },
                    itemStyle: {
                        color: '#33B5E5',
                    },
                    markPoint: {
                        data: response.novelty_peaks.map((peak) => ({
                            coord: [peak, response.novelty_curve[peak]],
                        })),
                        itemStyle: {
                            color: 'red', // Highlight peaks with red color
                        },
                        symbolSize: 10,
                        label: {
                            show: false, // Hide the value display for markPoint
                        },
                    },
                    markLine: {
                        animation: true,
                        data: [
                            {
                                xAxis: currentFrame, // Position the line at the current frame
                                lineStyle: {
                                    color: 'red',
                                    width: 2,
                                    type: 'solid',
                                },
                            },
                        ],
                        symbol: ['none', 'none'],
                        label: {
                            show: false, // Hide the label for the markLine
                        },
                    },
                },
            ],
        };

        return (
            <>
                <hr />
                <h5 className="color-primary">Novelty Curve</h5>
                <ReactECharts option={option} style={{ height: 300, width: '100%' }} />
            </>
        );
    };

    const playerControl = () => {
        if (!response || !response.novelty_curve) {
            return null;
        }
        return (
            <>
                <hr />
                <h5 className="color-primary">Player Control | Frame:{timeToFrameIndex(currentTime,response.feature_rate)}</h5>
                <button onClick={play}>PLAY</button>
                <button onClick={pause}>PAUSE</button>
                <button onClick={reset}>RESET</button>
                <br />
                <input
                    type="range"
                    min="0"
                    max={duration}
                    value={currentTime}
                    onChange={handleRangeChange}
                    style={{ width: '100%' }}
                />
            </>
        );
    };

    return (
        <div className="container mt-5">
            <h2>
                Player {wait ? <span className="spinner-border" role="status"></span> : ''}
            </h2>

            <div className="card">
                <div className="card-body">
                    <input
                        type="file"
                        id="fileInput"
                        style={{ display: 'none' }}
                        onChange={handleFileSelect}
                        accept=".mp3,.ogg" // Specify accepted file extension
                    />
                    <label
                        htmlFor="fileInput"
                        style={{
                            textAlign: 'center',
                            color: '#e72222',
                            fontWeight: 'bold',
                            cursor: 'pointer',
                        }}
                    >
                        {file ? `[ ${file.name} ]` : '[ DROP REFERENCE FILE ]'}
                    </label>

                    <button
                        disabled={file == null}
                        className="btn btn-custom"
                        onClick={handleFileUpload}
                        style={{
                            display: 'block',
                            margin: '10px auto',
                            padding: '10px 20px',
                        }}
                    >
                        Upload and Analyze
                    </button>
                </div>
            </div>

            {playerControl()}
            {renderNoveltyCurve()}
        </div>
    );
}
