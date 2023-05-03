export function sleep(ms: number) {
    return new Promise(r => setTimeout(r, ms));
}


export function randomIntFromInterval(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
  }
  