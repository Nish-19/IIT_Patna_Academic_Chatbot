const generateMessage = (username,text)=>{
    return {
        username,
        text,
        createdAt:new Date().getTime()
    }
}

const createLocationMessage = (username,location)=>{
    return {
        username,
        url:location,
        createdAt: new Date().getTime()
    }
}

module.exports = {
    generateMessage,
    createLocationMessage
}