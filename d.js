
const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

let students = [
    { id: 1, name: 'mani', age: 20 },
    { id: 2, name: 'reventh', age: 22 },
    { id: 3, name: 'sanvith', age: 19 }
];

// POST: Add a new student
app.post('/api/students', (req, res) => {
    const newStudent = {
        id: students.length + 1,
        name: req.body.name,
        major: req.body.major
    };

    if (newStudent.name && newStudent.major) {
        students.push(newStudent);
        res.status(201).json(newStudent);
    } else {
        res.status(400).json({
            message: 'Name and major are required'
        });
    }
});

// GET: Retrieve all students
app.get('/api/students', (req, res) => {
    res.status(200).json(students);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
