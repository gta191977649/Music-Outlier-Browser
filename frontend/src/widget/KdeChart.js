import React, { useEffect, useRef, useState } from 'react'
import ReactEcharts from "echarts-for-react"; 
import * as math from "../utils/math"
export default function KdeChart(props) {
    const [x,setX] = useState([])
    const [y,setY] = useState([])
    
    useEffect(()=>{
        try{
            let kde = math.kde(props.data.map(item=>item[props.discriminator]),math.gauss_kernel,props.bandwidth)
            //let x = kde[0].map(item => { return Math.round(item)})
            let x = kde[0].map(item => { return Math.round(item)})
            let y = kde[1]
            setX(x)
            setY(y)
        } catch(e) {
            setX([])
            console.log(e)
            
        }
        console.log('kde-render!')
    },[props])
    
    const op = {
        title: {
            text: 'Kernel density estimation'
        },
        grid: {
            top:50,
            bottom:70,
            left: 40,
            right: 10,
        },
        dataZoom: [
            {
                type: 'slider',

            }
        ],
        xAxis: {
            type: 'category',
            data: x
        },
        yAxis: {
            type: 'value'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            },
            formatter: function (params) {
                return `${props.discriminator} : ${params[0].name}<br/> p: ${params[0].data.toFixed(2)}`
            }
          },
        series: [
            {
                data:y,
                type: 'line',
                smooth: true,
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
        <React.Fragment>
            {x.length > 0 ? <ReactEcharts 
            option={op} 
            onEvents={{
                click: props.onClick,
                datazoom: (e) => {
                    let startIdx = Math.floor((e.start * 0.01) * (x.length-1))
                    let endIdx = Math.floor((e.end * 0.01) * (x.length-1))
                    let start = x[startIdx] 
                    let end = x[endIdx] 
                    
                    props.onZoomMoved(start,end)
                } ,
        }}
        /> : ""}
        </React.Fragment>
    )
}
