const express=require('express');
const  app=express();
app.use((req,res,next)=>{
console.log("using the  console....");
next();
});
app.get('/',(req,res) =>{
res.send('hello world');
});


app.get('/home',(req,res)=>{
res.send('home page');
});
app.post('/',(res,req)=>{
res.send('post request to home papge');
});
app.use((req,res)=>{
res.status(404).send('error 404 page not found');

})	
app.listen(8080,()=>{
console.log("starte on the port 8080");
});








