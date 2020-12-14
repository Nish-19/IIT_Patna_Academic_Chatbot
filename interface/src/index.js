const express=require('express')
const http=require('http')
const path=require('path')
const Filter=require('bad-words')
const socketio=require('socket.io')
const {generateMessage,createLocationMessage}=require('./utils/messages')
const messages = require('./utils/messages')
const {addUser,removeUser,getUser,getUsersInRoom}=require('./utils/users')
const fs=require('fs')
const shell=require('shelljs')

const app=express()
const server=http.createServer(app)
const io=socketio(server)

const port=process.env.PORT||3000
const publicDirectoryPath=path.join(__dirname,'../public')

app.use(express.static(publicDirectoryPath))

io.on('connection',(socket)=>{
    console.log('new web socket connection')
    
    socket.on('sendMessage',(message,cb)=>{
        const filter=new Filter()
        const user=getUser(socket.id)
        if(filter.isProfane(message)) {
            return cb('Profanity is not allowed')
        }
        io.to(user.room).emit('message',generateMessage(user.username,message))
        fs.writeFile('input.txt',message,()=>{
            shell.exec('./script.sh',()=>{
                fs.readFile('output.txt',{encoding: "utf8"},(err,data)=>{
                    var answer=err
                    if(!answer) {
                        answer=data
                    }
                    io.to(user.room).emit('message',generateMessage(user.username,answer))
                })
            })
        })
        cb()
    })
    socket.on('join',({username,room},cb)=>{
        const {error,user}=addUser({id:socket.id,username,room})
        if(error) {
            return cb(error)
        }
        socket.join(user.room)
        socket.emit('message',generateMessage('admin','welcome to my chat application'))
        socket.broadcast.to(user.room).emit('message',generateMessage('admin',`${user.username} has joined`))
        io.to(user.room).emit('roomData',{
            room:user.room,
            users:getUsersInRoom(user.room)
        })
        cb()
    })
    socket.on('disconnect',()=>{
        const user=removeUser(socket.id)
        if(user) {
            io.to(user.room).emit('message',generateMessage('admin',`${user.username} has left`))
            io.to(user.room).emit('roomData',{
                room:user.room,
                users:getUsersInRoom(user.room)
            })
        }
    })
})

server.listen(port,()=>{
    console.log(`server started on port ${port}`)
})