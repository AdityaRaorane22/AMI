const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bcrypt = require('bcrypt'); // Password hashing
const User = require('./models/user');

const app = express();
app.use(cors());
app.use(express.json());

// MongoDB connection
mongoose.connect('mongodb://localhost:27017/AMI')
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.error("MongoDB error:", err));

// Signup route
app.post('/signup', async (req, res) => {
  try {
    const { firstName, lastName, dob, gender, mobile, password, confirmPassword, departmentId } = req.body;

    if (password !== confirmPassword) {
      return res.status(400).json({ message: 'Passwords do not match' });
    }

    const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}@neuralfusion.com`;

    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: 'User already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10); // Hash password

    const user = new User({
      firstName,
      lastName,
      dob,
      gender,
      mobile,
      password: hashedPassword,
      email,
      departmentId
    });

    await user.save();

    res.status(201).json({ message: 'User registered successfully', email });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
});

// Login route
app.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(401).json({ message: 'Invalid email or password' });

    const isMatch = await bcrypt.compare(password, user.password); // Compare hashed
    if (!isMatch) return res.status(401).json({ message: 'Invalid email or password' });

    res.status(200).json({
      message: 'Login successful',
      user: {
        name: `${user.firstName} ${user.lastName}`,
        email: user.email
      }
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
});

// Start server
app.listen(5000, () => console.log('Server running on http://localhost:5000'));
