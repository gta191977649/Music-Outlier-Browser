import React, { useEffect,useState } from 'react'
import axios from 'axios'
import queryString from 'query-string';
export default function Spotify() {
    const [token, setToken] = useState(false)
    const [searchKey,setSearchKey] = useState("")
    const [searchID,setSearchID] = useState("")
    const [items,setItems] = useState([])
    const [audioFeatures,setAudioFeatureItems] = useState([])
    const CLIENT_ID = "caa2adfbf90a4368ade7472f2493095e"
    const REDIRECT_URI = "http://localhost:3000/spotify"
    const AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
    const RESPONSE_TYPE = "token"

    useEffect(()=>{
        console.log("Run sportfy")
        //const hash = window.location.hash
        const params = queryString.parse(window.location.hash)

        console.log(window.location.hash)
        if(params && params['access_token']) {
            setToken(params['access_token'])
        }        
    },[])

    const search = () => {
        axios.get("https://api.spotify.com/v1/search", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            params: {
                q: searchKey,
                type: "track,artist"
            }
        }).then((res)=>{
            setItems(res.data.tracks.items)
            console.log(res.data)
        }).catch(err=>{
            console.log(err)
        })
    }
    const searchAudioFeatures = () => {
        setAudioFeatureItems([])
        axios.get("https://api.spotify.com/v1/audio-features", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            params: {
                ids: searchID
            }
        }).then((res)=>{
            setAudioFeatureItems(res.data["audio_features"])
            console.log(res.data["audio_features"])
        }).catch(err=>{
            console.log(err)
        })
    }
    const renderResults = items.map(item => (
        <li className='tracks-items' key={item.id} onClick={()=>{
            setSearchID(item.id)
            searchAudioFeatures()
        }}>
           {item.name} : {item.id}
        </li>
    ))
    const renderAudioFeatures = audioFeatures.map(item=>{
        if(item) {
            return Object.keys(item).map(key =>{
                return <li>{key} : {item[key]}</li>
            })
        } else {
            return <p>No DATA!</p>
        }
    })

    return (
        <div className='container'>
            <br/>
            <div className='card'>
            <div class="card-header">
                Auth Info
            </div>
                <div class="card-body">
                <a href={`${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}`}>Login to Spotify</a>
                <p>Token: {token ? token : "False"}</p>
                </div>
            </div>
            <br/>
            
            <div className='card'>
                <div class="card-header">
                    Track Results
                    <input value={searchKey} onChange={(e)=>setSearchKey(e.target.value)}/>
                    <button onClick={search}>Search</button>
                </div>
                <div class="card-body">
                {renderResults}
                </div>
            </div>
            <br/>
            
            <div class="card">
                <div class="card-header">
                    Audio Features
                    <input value={searchID} onChange={(e)=>setSearchID(e.target.value)}/>
                    <button onClick={searchAudioFeatures}>Search</button>
                </div>
                <div class="card-body">
                {renderAudioFeatures}
                </div>
            </div>
        </div>
    )
}
