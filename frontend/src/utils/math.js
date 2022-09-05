import NormalDistribution from 'normal-distribution'
import * as ss from 'simple-statistics'

export function gauss_kernel(x) {
    return 1/Math.sqrt(2*Math.PI) * Math.exp(-0.5 * Math.pow(x,2))
}
function get_kde(x,data,kernel,bandwidth) {
    const N = data.length
    let res = 0
    for(let i = 0; i < N; i++) {
        res += kernel((x-data[i]) / bandwidth)    
    }
    res /= (N* bandwidth)
    return res
}
//Kernel density estimation
export function kde(data,kernel=gauss_kernel,bandwidth=0.1) {
    
    let linspace = require('linspace');
    let n = 50 
    let x = linspace(Math.min(...data),Math.max(...data),n)
    let y = []
    for(let i = 0; i < x.length; i++) {
        let val = get_kde(x[i],data,kernel,bandwidth)
        y.push(val)
    }
    return [x,y]
}
//cumulative distribution function
function get_std(data) {
    let mean = data.reduce((a, b) => a + b, 0) / data.length
    let sum = 0
    let N = data.length
    for(let i = 0; i < N; i++) {
        sum += Math.pow(data[i] - mean,2)
    }
    return Math.sqrt(1/N * sum)
}
export function cdf(data) {
    data = data.sort(function(a, b){return a - b})
    let x = data
    //sort data first
    //console.log(x)
    let mean = x.reduce((a, b) => a + b, 0) / x.length
    let std = get_std(x)
   //console.log(std)
    //Calc cdf
    let nor = new NormalDistribution(mean,std)
    let y = []
    for(let i = 0; i < x.length; i++) {
        y.push(nor.cdf(x[i]))
    }
    console.log([x,y])
    return [x,y]
}

export function correlation(x,y) {
    return ss.sampleCorrelation(x,y)
}