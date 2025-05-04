const express = require('express');
const mongoose = require('mongoose');
const app = express();
const port = 1111;

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/AMI', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).then(() => {
  console.log("Connected to MongoDB");
}).catch(err => {
  console.log("Error connecting to MongoDB:", err);
});

// Define a schema for the logs collection
const logSchema = new mongoose.Schema({
  Emp_name: String,
  Dept_ID: Number,
  Dept_Name: String,
  Access_ID: [Number],
  Access: String,
  Date_Time: String,
  Accessed_Files: [
    {
      Access_ID: Number,
      Access: String
    }
  ]
});

// Create a model for the logs collection
const Log = mongoose.model('Log', logSchema, 'logs');

// Define a route to get all data
app.get('/logs', async (req, res) => {
  try {
    const logs = await Log.find();
    res.json(logs);
  } catch (error) {
    console.error("Error fetching logs:", error);
    res.status(500).json({ message: "Internal Server Error" });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
