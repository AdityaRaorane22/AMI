const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const User = require('./models/User');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(console.log);

app.post('/signup', async (req, res) => {
  const { firstName, lastName, dob, gender, mobile, email, password, confirmPassword } = req.body;
  if (!firstName || !lastName || !dob || !gender || !mobile || !email || !password || !confirmPassword || password !== confirmPassword) {
    return res.status(400).json({ message: 'Invalid input' });
  }

  try {
    if (await User.findOne({ email })) return res.status(400).json({ message: 'User exists' });

    const hashedPassword = await bcrypt.hash(password, 10);
    await new User({ firstName, lastName, dob, gender, mobile, email, password: hashedPassword }).save();
    res.status(201).json({ message: 'User registered' });
  } catch {
    res.status(500).json({ message: 'Server error' });
  }
});

app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ message: 'Email and password required' });

  try {
    const user = await User.findOne({ email });
    if (!user || !await bcrypt.compare(password, user.password)) {
      return res.status(400).json({ message: 'Invalid credentials' });
    }
    res.status(200).json({ message: 'Login successful' });
  } catch {
    res.status(500).json({ message: 'Server error' });
  }
});

app.listen(process.env.PORT || 5000, () => console.log(`Server running`));
