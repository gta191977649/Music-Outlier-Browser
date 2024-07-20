import React, { useState,useRef,useEffect,useMemo } from 'react';
import * as hdf5 from 'jsfive';
import annotationPlugin from 'chartjs-plugin-annotation';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions";
import TimelinePlugin from "wavesurfer.js/dist/plugins/timeline";
import SpectrogramPlugin from "wavesurfer.js/dist/plugins/spectrogram";
import WebAudio from 'wavesurfer.js/dist/webaudio.js'
import * as Tone from 'tone'


export default function About() {
    // Constants
    const [file, setFile] = useState(null);
    const [h5File,setH5File] = useState(null);
    const [currentRegionStart,setRegionStart] = useState(0)

    // Time related
    const [currentTime, setCurrentTime] = useState(0);
    const [currentTimeIndex, setTimeIndex] = useState(0);
    const [currentChordName, setChordChordName] = useState("N/A");
    const SIGNAL_OFFSET = 0.3
    // Create REFs
    const waveformRef = useRef(null); 
    const timelineRef = useRef(null);
    const chordSynth = useRef(null);
    const wavesurferRef = useRef(null); 
    const regionsRef = useRef({});


    function cleanAndParseH5Array(h5Array) {
        // Step 1: Remove null bytes and other unwanted characters from each string
        const cleanedArray = h5Array.map(item => item.replace(/\x00+/g, ''));
    
        // Step 2: Parse each cleaned JSON string into an object
        const jsonArray = cleanedArray.map(item => JSON.parse(item));
    
        return jsonArray;
    }
    
    function cleanAndParseChordOriginal(chordOriginalArray) {
        const cleanedArray = [];
        
        for (let i = 0; i < chordOriginalArray.length; i += 3) {
            const time = chordOriginalArray[i].replace(/\x00+/g, '');
            const beat = chordOriginalArray[i + 1].replace(/\x00+/g, '');
            const chordLabel = chordOriginalArray[i + 2].replace(/\x00+/g, '');
            cleanedArray.push([parseFloat(time), parseFloat(beat), chordLabel]);
        }
    
        return cleanedArray;
    }
    
    const handlePlay=() =>{
        wavesurferRef.current.setVolume(1);
        wavesurferRef.current.play();     
    }

    const handlePause=() =>{
        wavesurferRef.current.pause();
    }

    const handleReset=() =>{
        wavesurferRef.current.setTime(0)
    }

    const loadChords = (chordLabels) => {
        let waveObj = wavesurferRef.current.plugins[0]
        waveObj.clearRegions();

        for(let i = 0; i < chordLabels.length; i++) {
            let time, beat, chord
            [time,beat,chord] = chordLabels[i]
            console.log(time,beat,chord)
            let region = waveObj.addRegion({
                start: time-SIGNAL_OFFSET,
                end: (time-SIGNAL_OFFSET ), // This assumes constant beat time for each chord in the bar
                color: "rgba(74, 156, 187, 0.5)",
                drag: false,
                resize: false
            })

            regionsRef.current[region.id] = region;
            region.setContent(`${chord}\n${beat}`)

        }
    }

    const createWaveSuer = () =>{
        return WaveSurfer.create({
            container: waveformRef.current,
            waveColor: 'violet',
            progressColor: 'purple',
            cursorColor: 'navy',
            barWidth: 2,
            scrollParent: true,
            minPxPerSec: 80,
            plugins: [ 
                RegionsPlugin.create({}),
                TimelinePlugin.create({
                    container: timelineRef,
                    timeInterval: 1,
                }),
               
            ],
        });

    }
    const handleFileSelect = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            const objectURL = URL.createObjectURL(selectedFile);
            wavesurferRef.current.load(objectURL);
            console.log(selectedFile.name); 

        }
    };

    const handleFileSelectH5 = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            setH5File(selectedFile);
            console.log(selectedFile.name); // For debugging
            
            const reader = new FileReader();
            reader.onload = (e) => {
                let barr = e.target.result;
                try {
                    var f = new hdf5.File(barr, selectedFile.name);
                    // Read Section Label
                    let g_section = f.get('section/section_label').value;
                    g_section = cleanAndParseH5Array(g_section)
                    // Read Chord Labels
                    let g_chords = f.get('chord/chord_original').value;
                    g_chords = cleanAndParseChordOriginal(g_chords)

                    loadChords(g_chords)
                   
                    
                } catch (error) {
                    console.error("Error reading the HDF5 file:", error);
                }
            };
            reader.readAsArrayBuffer(selectedFile);
        }
    };
    

    const playChord = (chordName) => {
        const notes = chordName;
        if (notes) {
            // `notes` can be an array of strings like ["C4", "E4", "G4"]
            
            chordSynth.current.triggerAttackRelease(notes, '4n'); // '1n' represents a whole note. You can change the duration as needed.
            console.log(chordName)
          } else {
            console.log('Chord not found:', chordName);
        }
    }

    
    useEffect(() => { 
        if(!chordSynth.current) {
            const context = new Tone.Context({ latencyHint: "interactive" });            
            Tone.setContext(context);
  
            chordSynth.current = new Tone.PolySynth(Tone.AMSynth).toDestination();
            console.log(Tone.getContext().latencyHint);
  
          
          }
          // Setup WaveSurfer instance
          if (!wavesurferRef.current) {
              wavesurferRef.current = createWaveSuer()
  
              // Listen to the 'audioprocess' event to update the current play time
              wavesurferRef.current.on('audioprocess', (time) => {
                  setCurrentTime(time);
                  //checkForRegionEntry(time);
              });
  
              // Also update time when audio finishes playing
              wavesurferRef.current.on('finish', () => {
                  setCurrentTime(0); // Reset the current time when audio finishes
              });
  
              wavesurferRef.current.on('region-created', (region) => {
                console.log("reg created")
              });
              wavesurferRef.current.plugins[0].on('region-in', (region) => {
                //console.log('Entered region:', region.content);
                //console.log(region.start.toFixed(1))
                // setRegionStart(region.start.toFixed(1))
                // let chord_c = region.content.textContent
                // let chord = chord_c.split("\n")[0]
                // setChordChordName(chord)
                //playChord("C4")
                const synth = new Tone.PolySynth().toDestination();
                // set the attributes across all the voices using 'set'
                synth.set({ detune: -1200 });
                // play a chord
                synth.triggerAttackRelease(["A6"], 0.2);

              });
              console.log(wavesurferRef.current)
              console.log("wavesurferRef created")
          }
  
         
  
          // Clean up WaveSurfer instance on component unmount
          return () => {
              if (wavesurferRef.current) {
                  // Remove event listeners to avoid memory leaks
                  wavesurferRef.current.un('audioprocess');
                  wavesurferRef.current.un('finish');
                  wavesurferRef.current.un('region-in');
                  
                  // Destroy WaveSurfer instance
                  wavesurferRef.current.destroy();
                  wavesurferRef.current = null;
              }
          };

    },[])
    return (
        <div className='container mt-5'>
            <h3>コート分析</h3>
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
                        style={{ textAlign: 'center', color: file ? "black" : "#e72222", fontWeight: "bold", cursor: "pointer" }}
                        >
                            {file ? `[ ${file.name} ]` : "[ DROP MP3 ]"}
                        </label>
                        <input
                            type="file"
                            id="fileInput2"
                            style={{ display: 'none' }}
                            onChange={handleFileSelectH5}
                            accept=".h5"  // Specify accepted file extension
                        />
                        <label
                        htmlFor="fileInput2"
                        style={{ textAlign: 'center', color: h5File ? "black" : "#e72222", fontWeight: "bold", cursor: "pointer" }}
                        >
                            {h5File ? `[ ${h5File.name} ]` : "[ DROP H5 REFERENCE ]"}
                        </label>
                    </div>
                </div>

                <div className="card mt-4">
                    <div className="card-header">
                    時間:{currentTime}
                    </div>
                    <div className="btn-group" role="group" aria-label="Basic example">
                        <button type="button" className="btn btn-nurupo" onClick={handlePlay}>再生</button>
                        <button type="button" className="btn btn-nurupo" onClick={handlePause}>一時停止</button>
                        <button type="button" className="btn btn-nurupo" onClick={handleReset}>リセット</button>
                    </div>

                </div>
                
                <div className={file ? "card mt-4": "d-none"}>
                    <div className="card-header">
                        VISUALIZER:
                    </div>
                    <div className="card-body">
                        {/* WaveSurfer waveform container */}
                        <div ref={waveformRef} style={{ height: file? '200px': "0px", marginTop: '20px' }} />
                    </div>
                </div>
        </div>
    )
}
