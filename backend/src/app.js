const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(express.json());
app.use(cors());

const port = 5000;

// Endpoint to upload data.json file
app.post('/upload', (req, res) => {
    const data = JSON.stringify(req.body);

    // Save the data to data.json file
    const fs = require('fs');
    fs.writeFileSync(path.join(__dirname, 'data.json'), data);

    // Run the Python script
    exec('python scripts/model.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${stderr}`);
            return res.status(500).send('Error processing data');
        }
        res.json(JSON.parse(stdout));
    });
});

app.listen(port, () => {
    console.log(`Server started on port ${port}`);
});
