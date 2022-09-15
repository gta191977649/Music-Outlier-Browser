import React, { useState ,useEffect} from 'react'
import ReactEcharts from "echarts-for-react"; 
import * as math from "../utils/math"

export default function ClusterChart(props) {
    const [compareDiscriminator,setCompareDiscriminator] = useState("tempo")
    const [data,setData] = useState([])
    const [correlation,setCorrelation] = useState(0)

    //Render Selection
    const renderDiscriminatorSelect = <div className="input-group mb-3">
    <span className="input-group-text">{props.discriminator} vs {compareDiscriminator}</span><select defaultValue={compareDiscriminator}  onChange={(e)=>{
      setCompareDiscriminator(e.target.value)
    }} className="form-select input-group-text" >
      {
        props.features.map((item,idx)=>{
          return (
            <option key={idx} value={item}>{item}</option>
          )
        })
      }
    </select></div>
    //On Mount
    useEffect(()=> {
        //console.log(props.data.data)
        setData([])
        try {
            let x = props.data.data.map(item=>item[compareDiscriminator])
            let y = props.data.data.map(item=>item[props.discriminator])
            let d = []
            for(let i = 0; i < x.length; i++) {
                d.push([x[i],y[i]])
            }
            console.log(d)
            //setData(d)
            setTimeout(function() {
                setData(d)
            },200)
            setCorrelation(math.correlation(x,y))
            
        }catch(e) {
            console.log(e)
        }
    },[props,compareDiscriminator])
    const colors = [
        '#c23531',
        '#0984e3',
        '#00b894',
        '#a29bfe',
        '#e84393',
        '#e17055',
        '#ca8622',
        '#bda29a',
        '#6e7074',
        '#546570',
        '#c4ccd3'
    ]

    const op = {
        // title: {
        //     text: 'Cumulative Distribution'
        // },
        grid: {
            top:50,
            bottom:70,
            left: 40,
            right: 10,
        },
        xAxis: {
        },
        yAxis: {
        },
        
        tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            formatter: function (params) {
                let idx = params[0]["dataIndex"]
                let targetSong = props.data.data[idx]
                return `${targetSong["title"]}<br/> ${targetSong["artist"]}<br/>${params[0].value}`
            }
          },
        series: [
            {
                symbolSize: 5,
                // symbolSize: function (dataItem) {
                //     return dataItem[1] * 0.3;
                // },
                data: data,
                type: 'scatter',
                lineStyle: {color: '#0d6efd'},
                itemStyle: {
                    normal:{
                        color: function(e) {
                            if (props.data.data !== undefined) {
                                let idx = parseInt(e.dataIndex)
                                console.log("idx",idx)
                                let song = props.data.data[idx]
                                if(song) return colors[song["label"]]
                                else return "#0d6efd"
                            }
                            return "#0d6efd"
                        },
                    }
                }
            }
        ]
    }

    return (
        <div>
            <h6>Correlation Analysis</h6>
            {renderDiscriminatorSelect}
            <ReactEcharts option={op} 
            onEvents={{
                click: props.onClick,
            }}
            />
            <small>X:{compareDiscriminator}, Y:{props.discriminator}</small>
            <br/>
            <small>Correlation: {correlation}</small>
        </div>
    )
}
