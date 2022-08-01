// Citation: Line 9
// Date: 08/01/2022
// Based on: "UseTube.js""
// Source URL: https://www.npmjs.com/package/usetube


const PORT = 3000
import express from 'express';
import usetube from 'usetube';

const app = express()

app.get('/', async (req, res) => {
    
    const data = await usetube.searchVideo('Bicycle Repairs');

    var info = data.videos;

    const array = []
    
    for (let i = 0; i < info.length; i++) {
        var curr_dict = info[i]
        var ids = curr_dict.id
        var titles = curr_dict.original_title
        array.push({
            ids,
            titles  
      })
    
    }

    res.send(array);
    
    })

app.listen(PORT, () => {console.log(`server running on PORT ${PORT}`)})