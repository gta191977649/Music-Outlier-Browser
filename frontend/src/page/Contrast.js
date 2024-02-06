import React, { useState, useRef, useEffect } from 'react';
import { Collapse } from 'react-collapse';
import axios from 'axios';
import { getCookie } from '../utils/cookie';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';
import annotationPlugin from 'chartjs-plugin-annotation';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions";
import TimelinePlugin from "wavesurfer.js/dist/plugins/timeline";
import SpectrogramPlugin from "wavesurfer.js/dist/plugins/spectrogram";
import WebAudio from 'wavesurfer.js/dist/webaudio.js'

//import MarkerPlugin from "wavesurfer.js/dist/plugins/marker";
import * as Tone from 'tone'



export default function Contrast() {
    const [chord_file, setChordFile] = useState(null);
    const [waveFile, setWaveFile] = useState(null);
    const waveformRef = useRef(null); 
    const timelineRef = useRef(null);
    const chordSynth = useRef(null);
    const wavesurferRef = useRef(null); 
    const regionsRef = useRef({});

    const [currentTime, setCurrentTime] = useState(0);
    const [currentChordName, setChordChordName] = useState("N/A");
    const SIGNAL_OFFSET = 0.1
    let lastEnteredRegionRef = useRef(0);


    const chordColor = {
        'C': '#FFFF00', 'CM7': '#FFFF00', 'C7': '#FFFF00',
          'Cm': '#E0FF00', 'Cm7': '#E0FF00',
      
        'C#': '#C0FF00', 'C#M7': '#C0FF00',  'C#7': '#C0FF00',
          'C#m': '#80FF00','C#m7': '#80FF00',
        'Db': '#C0FF00', 'DbM7': '#C0FF00',  'Db7': '#C0FF00',
          'Dbm': '#80FF00','Dbm7': '#80FF00',
      
        'D': '#00FF00', 'DM7': '#00FF00', 'D7': '#00FF00',
          'Dm': '#00FF80', 'Dm7': '#00FF80',
      
        'D#': '#00FFC0', 'D#M7': '#00FFC0',  'D#7': '#00FFC0',
          'D#m': '#00FFE0','D#m7': '#00FFE0',
        'Eb': '#00FFC0', 'EbM7': '#00FFC0',  'Eb7': '#00FFC0',
          'Ebm': '#00FFE0','Ebm7': '#00FFE0',
      
        'E': '#00FFFF', 'EM7': '#00FFFF', 'E7': '#00FFFF',
          'Em': '#00E0FF', 'Em7': '#00E0FF',
      
        'F': '#00C0FF', 'FM7': '#00C0FF',  'F7': '#00C0FF',
          'Fm': '#0080FF','Fm7': '#0080FF',
      
        'F#': '#0000FF', 'F#M7': '#0000FF',  'F#7': '#0000FF',
          'F#m': '#8000FF','F#m7': '#8000FF',
        'Gb': '#0000FF', 'GbM7': '#0000FF',  'Gb7': '#0000FF',
          'Gbm': '#8000FF','Gbm7': '#8000FF',
      
        'G': '#C000FF', 'GM7': '#C000FF',  'G7': '#C000FF',
          'Gm': '#E000FF','Gm7': '#E000FF',
      
        'G#': '#FF00FF', 'G#M7': '#FF00FF', 'G#7': '#FF00FF',
          'G#m': '#FF00E0', 'G#m7': '#FF00E0',
        'Ab': '#FF00FF', 'AbM7': '#FF00FF', 'Ab7': '#FF00FF',
          'Abm': '#FF00E0', 'Abm7': '#FF00E0',
      
        'A': '#FF00C0', 'AM7': '#FF00C0', 'A7': '#FF00C0',
          'Am': '#FF0080', 'Am7': '#FF0080',
      
        'A#': '#FF0000','A#M7': '#FF0000', 'A#7': '#FF0000',
          'A#m': '#FF8000', 'A#m7': '#FF8000',
        'Bb': '#FF0000','BbM7': '#FF0000', 'Bb7': '#FF0000',
          'Bbm': '#FF8000', 'Bbm7': '#FF8000',
      
        'B': '#FFC000', 'BM7': '#FFC000', 'B7': '#FFC000',
          'Bm': '#FFE000', 'Bm7': '#FFE000','N':"#808080",'X':"#808080",
    };
    const chordMappings = {
      // Major Chords
      'C': ['C4', 'E4', 'G4'],
      'C#': ['C#4', 'F4', 'G#4'],
      'D': ['D4', 'F#4', 'A4'],
      'D#': ['D#4', 'G4', 'A#4'],
      'E': ['E4', 'G#4', 'B4'],
      'F': ['F4', 'A4', 'C5'],
      'F#': ['F#4', 'A#4', 'C#5'],
      'G': ['G4', 'B4', 'D5'],
      'G#': ['G#4', 'C5', 'D#5'],
      'A': ['A4', 'C#5', 'E5'],
      'A#': ['A#4', 'D5', 'F5'],
      'B': ['B4', 'D#5', 'F#5'],
  
      // Minor Chords
      'Cm': ['C4', 'D#4', 'G4'],
      'C#m': ['C#4', 'E4', 'G#4'],
      'Dm': ['D4', 'F4', 'A4'],
      'D#m': ['D#4', 'F#4', 'A#4'],
      'Em': ['E4', 'G4', 'B4'],
      'Fm': ['F4', 'G#4', 'C5'],
      'F#m': ['F#4', 'A4', 'C#5'],
      'Gm': ['G4', 'A#4', 'D5'],
      'G#m': ['G#4', 'B4', 'D#5'],
      'Am': ['A4', 'C5', 'E5'],
      'A#m': ['A#4', 'C#5', 'F5'],
      'Bm': ['B4', 'D5', 'F#5'],
  
      // Major 7th Chords
      'CM7': ['C4', 'E4', 'G4', 'B4'],
      'C#M7': ['C#4', 'F4', 'G#4', 'C5'],
      'DM7': ['D4', 'F#4', 'A4', 'C#5'],
      'D#M7': ['D#4', 'G4', 'A#4', 'D5'],
      'EM7': ['E4', 'G#4', 'B4', 'D#5'],
      'FM7': ['F4', 'A4', 'C5', 'E5'],
      'F#M7': ['F#4', 'A#4', 'C#5', 'F5'],
      'GM7': ['G4', 'B4', 'D5', 'F#5'],
      'G#M7': ['G#4', 'C5', 'D#5', 'G5'],
      'AM7': ['A4', 'C#5', 'E5', 'G#5'],
      'A#M7': ['A#4', 'D5', 'F5', 'A5'],
      'BM7': ['B4', 'D#5', 'F#5', 'A#5'],
  
      // Minor 7th Chords
      'Cm7': ['C4', 'D#4', 'G4', 'A#4'],
      'C#m7': ['C#4', 'E4', 'G#4', 'B4'],
      'Dm7': ['D4', 'F4', 'A4', 'C5'],
      'D#m7': ['D#4', 'F#4', 'A#4', 'C#5'],
      'Em7': ['E4', 'G4', 'B4', 'D5'],
      'Fm7': ['F4', 'G#4', 'C5', 'D#5'],
      'F#m7': ['F#4', 'A4', 'C#5', 'E5'],
      'Gm7': ['G4', 'A#4', 'D5', 'F5'],
      'G#m7': ['G#4', 'B4', 'D#5', 'F#5'],
      'Am7': ['A4', 'C5', 'E5', 'G5'],
      'A#m7': ['A#4', 'C#5', 'F5', 'G#5'],
      'Bm7': ['B4', 'D5', 'F#5', 'A5'],
  
      // Dominant 7th Chords
      'C7': ['C4', 'E4', 'G4', 'A#4'],
      'C#7': ['C#4', 'F4', 'G#4', 'B4'],
      'D7': ['D4', 'F#4', 'A4', 'C5'],
      'D#7': ['D#4', 'G4', 'A#4', 'C#5'],
      'E7': ['E4', 'G#4', 'B4', 'D5'],
      'F7': ['F4', 'A4', 'C5', 'D#5'],
      'F#7': ['F#4', 'A#4', 'C#5', 'E5'],
      'G7': ['G4', 'B4', 'D5', 'F5'],
      'G#7': ['G#4', 'C5', 'D#5', 'F#5'],
      'A7': ['A4', 'C#5', 'E5', 'G5'],
      'A#7': ['A#4', 'D5', 'F5', 'G#5'],
      'B7': ['B4', 'D#5', 'F#5', 'A5'],
  };
  
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
                // SpectrogramPlugin.create({
                //   labels: true,
                //   height: 200,
                //   splitChannels: false,
                // })
                // WaveSurfer.cursor.create({
                //     showTime: true,
                //     opacity: 0.5,
                //     customShowTimeStyle: {
                //       'padding': '5px',
                //       'padding-top': '100px',
                //       'font-size': '12px'
                //     }
                // }),
         
            ],
        });

    }
    const visualizeChords = (chordLabels) => {
      let baseColorMap = ["#4A9CBB", "#9D6AFF"]
      let prevChord = 'N';
      let waveObj = wavesurferRef.current.plugins[0]
      waveObj.clearRegions();
      let downBeatStartTime = 0;
      let beat_time = 0;
      let beatCounter = 0; // Initialize a counter to keep track of beats
      chordLabels.forEach((line, i) => {
        if (!line) return
        let labelComps = line.split('\t')
        if (labelComps.length != 3) return
  
        let start_time = parseFloat(labelComps[0]);
        let beat_number = parseInt(labelComps[1], 10);
  
        // Increment beatCounter and reset if it reaches 4
        beatCounter = beat_number === 1 ? 1 : beatCounter + 1;
  
        // Calculate beat_time at every 4th beat or when the beat starts over
        if (beat_number === 4 || beatCounter === 1) {
          if (i >= 3) {
            downBeatStartTime = parseFloat(chordLabels[i - 3].split('\t')[0]); // Start of the bar
            beat_time = (start_time - downBeatStartTime) / 3; // Divided by 3 because it's the difference between 4 beats
          } else {
            // Handle the case for the first few chords before enough data is available
            downBeatStartTime = start_time; // Fallback to current start time
            beat_time = 0; // No beat time can be calculated yet
          }
        }
  
        let chordName = labelComps[2].replace(':maj7', 'M7').replace(':min7', 'm7')
                                     .replace(':maj', '').replace(':min', 'm').replace(':', '');
  
        // Continue the loop for chords named "N" or "X" after updating beat time
        // if (chordName === "N" || chordName === "X") return;
  
        let color = baseColorMap[0]; // default color, you may want to change logic for color
        if (chordName in chordColor)
          color = chordColor[chordName]
        
        let region = waveObj.addRegion({
          start: start_time-SIGNAL_OFFSET,
          end: (start_time + beat_time)-SIGNAL_OFFSET, // This assumes constant beat time for each chord in the bar
          color: color.concat("77"),
          drag: false,
          resize: false
        })
        regionsRef.current[region.id] = region;
        region.setContent(`${chordName}\n${beat_number}`)
      });
    }
    
    const readChordFile = (file) => {
        const reader = new FileReader();

        reader.onload = (event) => {
            // This will execute after the file is read
            const base64data = event.target.result.replace(
              'data:application/octet-stream;base64,','');
          
            let chordText = atob(base64data);
            let chordLabels = chordText.split('\n');
            visualizeChords(chordLabels);
        };
    
        reader.onerror = (error) => {
            // Handle errors
            console.log('Error: ', error);
        };
    
        reader.readAsDataURL(file); // Read the file
    }
    const handleWaveFileSelect = (event) => {
        const file = event.target.files[0];
        setWaveFile(file);

        // // Create a new instance of WaveSurfer if it doesn't exist
        // if (!wavesurferRef.current) {
        //     wavesurferRef.current =createWaveSuer()
        // }

        // Load the selected wave file into WaveSurfer
        const objectURL = URL.createObjectURL(file);
        
        wavesurferRef.current.load(objectURL);
    };

    const handleChordFileSelect = (event) => {
        const file = event.target.files[0];
        setChordFile(file)
        readChordFile(file)
    }

    const handlePlay=() =>{
      wavesurferRef.current.setVolume(0.8);
      wavesurferRef.current.play();
        
    }
    const handlePause=() =>{
        wavesurferRef.current.pause();
    }
    const handleReset=() =>{
        wavesurferRef.current.setTime(0);
    }
    const playChord = (chordName) => {
      const notes = chordMappings[chordName];
      if (notes) {
          // `notes` can be an array of strings like ["C4", "E4", "G4"]
          
          chordSynth.current.triggerAttackRelease(notes, '4n'); // '1n' represents a whole note. You can change the duration as needed.
          console.log(chordName)
        } else {
          console.log('Chord not found:', chordName);
      }
  };
    // const checkForRegionEntry = (currentTime) => {
    //   Object.values(regionsRef.current).forEach((region,idx) => {
    //       if (currentTime >= region.start && currentTime <= region.end && lastEnteredRegionRef !== region.id) {
    //         let chord = region.content.textContent
    //         setChordChordName(chord)
    //         playChord(chord)
    //         console.log('Chord:', chord);
    //         lastEnteredRegionRef = region.id
            
    //           // Perform your action for region entry
    //           // Ensure you handle the case where you're continuously within the region
    //       }
    //   });
    // };
  
    // Clean up WaveSurfer instance on component unmount
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
              let chord_c = region.content.textContent
              let chord = chord_c.split("\n")[0]
              setChordChordName(chord)
              playChord(chord)
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
    }, []);

    return (
        <div className='container mt-5'>
            <h2>対照分析</h2>

            <div className="card">
                <div className="card-body">
                    {/* ... existing code ... */}
                    <input
                        type="file"
                        id="fileInput1"
                        style={{ display: 'none' }}
                        onChange={handleWaveFileSelect}
                        accept=".wav,.mp3"
                    />
                    <label
                        htmlFor="fileInput1"
                        style={{ textAlign: 'center', color: "#343a40", fontWeight: "bold", cursor: "pointer" }}
                    >
                        {waveFile ? `[ ${waveFile.name} ]` : "[ DROP AUDIO FILE ]"}
                    </label>

                    <input
                        type="file"
                        id="fileInput2"
                        style={{ display: 'none' }}
                        onChange={handleChordFileSelect}
                        accept=".lab"
                    />
                    <label
                        htmlFor="fileInput2"
                        style={{ textAlign: 'center', color: "#343a40", fontWeight: "bold", cursor: "pointer" }}
                    >
                        {chord_file ? `[ ${chord_file.name} ]` : "[ DROP CHORD FILE ]"}
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
            <div className="card mt-4">
                <div className="card-header">
                  コート解析:{currentChordName}
                </div>
                <div className="card-body">
                  {/* WaveSurfer waveform container */}
                  <div ref={waveformRef} style={{ height: '200px', marginTop: '20px' }} />
                  <div ref={timelineRef}/>
                </div>
            </div>
        </div>
    );
}
