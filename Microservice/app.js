import fetch from 'node-fetch';

async function getResults() {
    try {
      const response = await fetch('http://localhost:3000');
  
      if (!response.ok) {
        throw new Error(`Error! status: ${response.status}`);
      }
  
      const result = await response.json();
      return result;
    } catch (err) {
      console.log(err);
    }
  }
  
  console.log(await getResults());
