const users=[]

//addUser,newUser,getUser,getUsersInRoom

const addUser = ({id,username,room})=>{
    //clean the data,lowercase and trim
    username=username.trim().toLowerCase()
    room=room.trim().toLowerCase()
    //validate the data
    if(!username||!room) {
        return {
            error: 'username and room are required'
        }
    }
    //check for existing user
    const existingUser=users.find((user)=>{
        return (user.room===room&&user.username===username)
    })

    if(existingUser) {
        return {
            error: 'username is in use'
        }
    }

    //store user
    const user={id,username,room}
    users.push(user)
    return {user}
}

const removeUser=(id)=>{
    const index=users.findIndex((user)=>user.id===id)

    if(index!==-1){
        return users.splice(index,1)[0]
    }
}

const getUser = (id)=>{
    const user=users.find((user)=>user.id===id)

    if(!user) return undefined
    return user
}

const getUsersInRoom = (room)=>{
    return users.filter((user)=>user.room===room)
}

module.exports = {
    addUser,
    removeUser,
    getUser,
    getUsersInRoom
}