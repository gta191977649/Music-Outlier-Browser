import React, { useState ,useEffect} from 'react'
import ReactEcharts from "echarts-for-react"; 
import * as math from "../utils/math"

export default function CorrelationChart(props) {
    const [compareDiscriminator,setCompareDiscriminator] = useState("loudness")
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
        try {
            let x = props.data.map(item=>item[compareDiscriminator])
            let y = props.data.map(item=>item[props.discriminator])
            let d = []
            for(let i = 0; i < x.length; i++) {
                d.push([x[i],y[i]])
            }
            console.log(d)
            setData(d)
            setCorrelation(math.correlation(x,y))
            
        }catch(e) {
            console.log(e)
        }
    },[props,compareDiscriminator])

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
                let targetSong = props.data[idx]
                
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
                        color:"#0d6efd",
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
