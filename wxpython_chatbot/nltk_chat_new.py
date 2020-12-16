from nltk.chat.util import Chat, reflections

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?",]
    ],
    [
        r"what is your name?",
        ["I'm academic chatbot. Nice meeting you.",]
    ],
    [
        r"how are you ?",
        ["I'm doing good\nHow about You ?",]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i'm doing good",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"(.*) age?",
        ["I'm a computer program dude\nSeriously you are asking me this?",]
        
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
        
    ],
    [
        r"(.*) created ?",
        ["Group of geeks from IITP created me using Python's NLTK library ","top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Patna, India',]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"(.*) (sports|game) ?",
        ["I'm a very big fan of Football",]
    ],
    [
        r"who (.*) sportsperson ?",
        ["Messy","Ronaldo","Roony"]
    ],
    [
        r"who (.*) (moviestar|actor)?",
        ["Brad Pitt"]
    ],
    [
        r"quit",
        ["Bye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
    ],
    [
        r"how to ask a (.*) ?",
        ["Enter D in the input and then ask the database question"]
    ],
    [
        r"thank (.*)",
        ["You are welcome"]
    ],
    [
        r"it was nice speaking to you",
        ["Thank You! My pleasure"]
    ],
    [
        r"(this|that|it) is (.*) (bad|sad|disappointing)",
        ["I am sorry to learn that"]
    ],
    [
        r"(this|that|it) is (.*) (good|awesome|cool|nice)",
        ["That's great!"]
    ],
    [
        r"okay",
        ["Nice, you have any more questions?"]
    ],
]


def chatty(utter):
    #print("Hi, I'm Chatty and I chat alot ;)\nPlease type lowercase English language to start a conversation. Type quit to leave ") #default message at the start
    chat = Chat(pairs, reflections)
    if utter == '':
        print(chat.respond(input("> ")))
    else:
        result = chat.respond(utter)
        # if result == None:
        #     print('Sorry general query not found. These are the most similar sounding queries')
        #     find_similarity(utter)
        #     choice = input('Do you want to give feedback for DB question (Y/N): ')
        #     if choice == 'Y' or choice == 'y':
        #         feedback_file.write(utter + "," + "1\n")
        # else:
        #     print(chat.respond(utter))
        if result == None:
            result = "None"
        return result

if __name__ == "__main__":
    chatty()