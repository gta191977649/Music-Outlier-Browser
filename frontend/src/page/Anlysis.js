import React, {useState} from 'react';

export default function Analysis() {
    const [file, setFile] = useState("");
    return (
        <div className='container mt-5'>
            <h2>Contrast Analysis</h2>
            
            <div class="card">
                <div class="card-body">
                    <input 
                        type="file" 
                        id="fileInput" 
                        style={{ display: 'none' }} 
                        onChange={handleFileSelect}
                    />
                    <label 
                        htmlFor="fileInput" 
                        style={{textAlign:'center', color:"#e72222", fontWeight:"bold", cursor: "pointer"}}
                    >
                        [ DROP FILE ]
                    </label>
                </div>
            </div>

            <div class="card mt-4">
                <div className="card-header">
                    分析応答
                </div>
                <div class="card-body">
                    [ N/A ]
                </div>
            </div>
        </div>
    );

    function handleFileSelect(event) {
        // Handle file selection
        const file = event.target.files[0];
        console.log(file.name); // Process the file as needed
    }
}
