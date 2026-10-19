const  express= require('express');
const app =express();
const port =8080;
app.use((req,res,nextq)=>{
const startTime =Date.now();
res.on('finish',()=>{
const duration =Date.now()-startTime;
console.log(
`${new Date().toISOString()}  | `+
`${req.method} $ {req.originalUrl}  |`+
`Status:${res.statusCode}  |`+
`Time:${duration}  ms`
);
});


next();
});


app.get('/',(req,res)=>
{res.send('welcome to express  logger');
});

app.get('/about',(req,res)=>{
res.send('this is the About the page ');
});


app.get('/user',(req,res)=>{
res.json({
id:101,
name:"revanth",
department:"ai and ds"
});
}) 


app.use((req,res)=>{
res.status(404).send('404 page not found');
})


app.listen(port,()=>{
console.log('port is running');
});



159(13)2468

The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);
 

Example 1:

Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
Example 2:

Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:
P     I    N

