import React from 'react'
import {ScatterChart, Scatter, Line, XAxis, YAxis,ZAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Chart(props) {
    const data = [
        {
          name: 'Page A',
          uv: 4000,
          pv: 2400,
          amt: 2400,
        },

      ];
    return (

        <ResponsiveContainer width="100%" height={200}>
            <ScatterChart
            margin={{ top: 20, right: 0, left: 0, bottom: 0 }}
            data={props.data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis />
            <YAxis />
            <ZAxis type="number" range={[10, 10]} />
            <Tooltip formatter={(i,j,k)=> {
              return `${k.payload.title} - ${k.payload.artist}`
            }} />
            <Legend />
            <Scatter dataKey={props.discriminator} fill="#0d6efd" onClick={props.onClick}/>
            </ScatterChart>
        </ResponsiveContainer>
    
    )
}