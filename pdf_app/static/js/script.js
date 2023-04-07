const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

// Parse URL-encoded bodies (as sent by HTML forms)
app.use(bodyParser.urlencoded({ extended: true }));

// Serve the HTML file
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// Handle the form submission and generate the PDF file
app.post('/generate_pdf', (req, res) => {
  // Get the form data
  const { first_name, last_name, dob, current_date, member_id, claim_number } = req.body;

  // Run the Python script to generate the PDF file
  const pythonProcess = spawn('python', ['generate_pdf.py', first_name, last_name, dob, current_date, member_id, claim_number]);
  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });
  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
  pythonProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    // Send the generated PDF file as a response
    res.sendFile(__dirname + '/insurance_claim.pdf');
  });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
