const PORT = 3000
import express from 'express';
import usetube from 'usetube';
import bodyParser from 'body-parser';

const app = express()

app.use(bodyParser.urlencoded({ extended: false }))
 
app.use(bodyParser.json())

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