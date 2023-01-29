import logo from '../logo.svg';
import React, { useEffect, useMemo, useState } from 'react';
import Chart from '../widget/Chart'
import KdeChart from '../widget/KdeChart'
import CdfChart from '../widget/CdfChart';
import ClusterChart from '../widget/ClusterChart';
import axios from 'axios'
import * as math from '../utils/math' 

function App() {

  const FEATURES = [
    'loudness','tempo','mode','key','genre','title','artist'
  ]
  const KEY_NAMES = [
    'C','C#','D','D#','E','F','F#','G','G#','A','A#','B'
  ]
  const [query,setQuery] = useState([])
  const [result,setResult] = useState([])
  const [clusterData,setClusterData] = useState([])
  const [selectedSong,setSelectedSong] = useState()
  const [discriminator,setDiscriminator] = useState("loudness")
  const [limit,setLimit] = useState(1000)
  const [error,setError] = useState(false)
  const [bandwidth,setBandwith] = useState(0.1)
  const [sidebarFullScreen,setSidebarFullScreen] = useState(false)

  useEffect(()=>{
    doCluster()
  },[result])
  
  // MAIN ------ CURD Functions For Query ------
  const updateQuery = (feature,criteria,val) => {
    const newQuery = query.map((item)=>{
      if(item.feature === feature) {
        return {...item,"criteria":criteria,"value":val}
      }
      return item
    })
    setQuery(newQuery)
    console.log(query)
  }
  const removeQuery = (index) => {
    setQuery(query.filter((o, i) => index !== i));
  };
  const addQuery = (feature) => {
    console.log(feature)
    let q = {
        "feature":feature,
        "criteria":"eq",
        "value":0
    }
    setQuery([...query,q])
    console.log(query)
  }
  //Helper Function
  const isParameterSelect = (feature) => {
    return query.filter(item=>{
      return item["feature"] == feature
    })
  }

  const render_features = FEATURES.map((item,idx)=>{
    if (isParameterSelect(item).length == 0) {
      return(
        <span key={idx} className="badge text-bg-light features-bage" onClick={()=>{
          addQuery(item)
        }}>{item}</span>
      )
    }
    
  })
  const render_query = query.map((query,idx)=>{
   
    return(
      <div key={idx} className="input-group mb-3">
        <span className="input-group-text">{query.feature}</span>
        <select onChange={(e)=>{
          updateQuery(query.feature,e.target.value,query.value)
        }} defaultValue={query.criteria} className="form-select input-group-text">
          <option value="eq">=</option>
          <option value="gt">&#62;</option>
          <option value="ls">&#60;</option>
          <option value="contain">Contain</option>
        </select>
        <input type="text" value={query.value} onChange={(e)=>{
          updateQuery(query.feature,query.criteria,e.target.value)
        }} className="form-control"/>
        <button className="btn btn-danger" onClick={()=>{
          removeQuery(idx)
        }}>X</button>
    </div>
    )
  })

  const renderResults = (data) => data.map((item,idx)=> {
    return(
      <div key={idx} className="card mt-3">
        <div className="card-body">
          <h3>{item.title} - {item.artist}</h3> 
          <span className="badge text-bg-primary">ID: {item.id}</span>
          <span className="badge text-bg-dark">{item.genre}</span>
          <span className="badge text-bg-secondary">Tempo: {item.tempo}</span>
          <span className="badge text-bg-success">Loudness: {item.loudness} dB</span>
          <span className="badge text-bg-danger">Key: {KEY_NAMES[item.key]}</span>
          <br/>
          <a href={`https://www.youtube.com/results?search_query=${item.title} - ${item.artist}`} target="_blnk">Find it on youtube</a>
        </div>
      </div>
    )
  })
  


  const renderDiscriminatorSelect = <div className="input-group mb-3">
  <span className="input-group-text">Feature</span><select defaultValue={discriminator}  onChange={(e)=>{
    setDiscriminator(e.target.value)
  }} className="form-select input-group-text" >
    {
      FEATURES.map((item,idx)=>{
        return (
          <option key={idx} value={item}>{item}</option>
        )
      })
    }
  </select></div>
   
  const onOutlierClicked = (e) =>{
    console.log(e)
    setSelectedSong([e])
  } 

  const onKDEGraphClicked = (e) =>{
    let target = parseInt(e.name)
    //console.log(target)
    //filtering the select song from the cliked value
    let data = result.filter((item)=>{
      return item[discriminator] >= target-1 && item[discriminator] <= target+1
    })
    setSelectedSong(data)
  }
  
  const onCorrelationClicked = (e) => {
    let idx = e["dataIndex"]
    let targetSong = result[idx]
    console.log(targetSong)
    setSelectedSong([targetSong])
  }

  const onDataZoomMoved = (start,end) => {
    //filter data from the range
    let data = result.filter((item)=>{
      return item[discriminator] >= start && item[discriminator] <= end
    })
    console.log(start,end)
    setSelectedSong(data)
    
  }


  const searchSong = () => {
    const URL = "./api/search/"
    //const URL = "http://localhost:8000/api/search/"
    axios.post(URL,{
      "query":query,
      "limit":limit,
    })
    .then(res => {
      const data = res.data;
      setResult(data)
     
      //restore status
      setSelectedSong()
      console.log(data)
      setError(false)
    })
    .catch((err) =>  {
        console.log(err)
        setError(err.message)
    })
  }
  const doCluster = () => {
    setClusterData([])
    //const URL = "http://localhost:8000/api/cluster/"
    const URL = "./api/cluster/"
    axios.post(URL,{
      "query":query,
      "limit":limit,
    })
    .then(res => {
      const data = res.data;
      console.log("Cluster")
      setClusterData(data)
    })
    .catch((err) =>  {
        console.log(err)
        setClusterData([])
    })
  }

  const renderCharts = useMemo(()=> {
    return <React.Fragment>
      <Chart data={result} discriminator={discriminator} onClick={onOutlierClicked}/>
      <CdfChart data={result} discriminator={discriminator} onClick={onKDEGraphClicked}/>
      <KdeChart data={result} discriminator={discriminator} bandwidth={bandwidth} onClick={onKDEGraphClicked} onZoomMoved={onDataZoomMoved}/>
      <ClusterChart data={clusterData} features={FEATURES} discriminator={discriminator} onClick={onCorrelationClicked}/>
    </React.Fragment>
  },[result,clusterData,discriminator])
  
  return (
    <div className="App mt-3">
      <div className="row">

        <div className={sidebarFullScreen ? "col-12 side-bar" :"col-3 side-bar"}>
          <div className="form-check form-switch m-3">
            <input className="form-check-input" type="checkbox" role="switch" value={sidebarFullScreen} onChange={(e)=>{
              setSidebarFullScreen(e.target.checked)
            }}/>
            <label className="form-check-label" for="flexSwitchCheckDefault">Full Screen</label>
          </div>
          <div className="card"  >
            <div className="card-header">
              Search Query
            </div>
            <div className="card-body">
              <p>Query:</p>
              {render_query}
              <p>Features Pool:</p>


              {render_features}
              <div className="input-group mt-3">
                <span className="input-group-text" id="basic-addon1">Limit</span>
                <input type="number" className="form-control" value={limit}
                  onChange={(e)=>{
                    setLimit(e.target.value)
                  }}
                />
              </div>

              <p>Request Query Param</p>
              <div className="input-group">
                <textarea className="form-control" aria-label="With textarea" value={JSON.stringify(query)} readOnly={true}/>
              </div>
             

              <div className="input-group mt-3">
                <button type="button" className="btn btn-primary" onClick={()=>{searchSong()}}>Search</button>
              </div>

            </div>
          </div>

          <div className="card" >
            <div className="card-header">
              Discriminator
            </div>
            <div className="card-body">
            {renderDiscriminatorSelect}
            <div className="input-group mb-3">
              <span className="input-group-text">Bandwidth (h)</span>
              <input type="number" className="form-control" value={bandwidth} onChange={(e)=>setBandwith(e.target.value)}/>
            </div>
                  {renderCharts}
            </div>
          </div>
        </div>
        <div className="col-9">
          <div className='container'>
            <h1>Result ({selectedSong ? selectedSong.length : result.length})</h1>
            {error ? 
            <div className="alert alert-danger" role="alert">
            {error}
            </div>
            :""}

            {selectedSong ? 
              <div className="input-group mt-3">
                <button type="button" className="btn btn-danger" onClick={(e)=>{
                  setSelectedSong()
                }}>Back to all results</button>
              </div>: ""
            }
            {selectedSong ?  renderResults(selectedSong) : renderResults(result)}

            
          </div>
        
        </div>
      </div>
      
    </div>
  );
}

export default App;
