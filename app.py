from flask import Flask,render_template,request, jsonify
from flask_cors import CORS

userPrompt = """
Your job is to take data and format it in JSON following this template strictly:
{
"firstName" : "first name",
"lastName": "last name",
"hotel" : "hotel name", 
"room" : "hotel room number",
"tour" :  "tour name from data ",
"tour date" : " DD-MM-YYYY",
"adults" : "number of adults",
"children": "number of children",
"infants": "number of infants",
"phone number": " phone number",
"time" : " pick up time from data",
"fee" : "total fee number",
"currency" : "total fee currency",
"country" : "country name by phone number"
}

you pay extra attention to match the data correctly, especially the number of adults,children, and infants, as well as the dates and times, and prices. Never modify or add data, this is extremely important.

the PAX means the number of people in the following form : Pax :<num1> + <num2> + <num3>free where <num1> is the adults number, <num2> is the children number, and <num3> is the infants number (num3 is always accompanied with a "free" word)
if you see something like pax: 1+2free it means that there is 1 adult and 2 infants only, whereas 1+2 means 1 adult and 1 child, and 2+1+1free is 2 adults, 1 child, and 1 infant.

the dates must be in the DD-MM-YYYY format, all numbers, no month names, the seperators must be dashes, not backslashes.

the time format is HH:MM , without AM and PM.

the total fee must be a number without the currency added to it

the currency must always be returned as a word without a symbol, the allowed words are : dollar, euro, lira , pound.

the phone number should include the + at the beginning if it was provided in the input data

Do not change the formatting of the template, your reply will only include the template above, you will never modify it, add to it, or remove from it, you will always follow it.

it is also very important that you follow the JSON template mentioned beforehand.

if any of the data is missing, leave the field blank, do not insert "?" or anything in its place, do not write a comment.

The form must always be returned in English. If the input is in another language (mainly russian or german), first translate the data English then fill the template in English. Translate everything including the tour's name. send the form in English strictly.

you will never say anything outside of the template, not a single word, just send the template and nothing else, if the user asks for something else, always replay with the exact words "I can't".

Do not say anything if there isn't enough data to fill the template, just add what you can and leave the rest empty

"""



app = Flask(__name__)
CORS(app)


#comment the code below if you dont want to use groq
from groq import Groq
client = Groq(
    api_key="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",
)
def makeRequest(userInput):
    messagesArr = [
        {"role" : "system",
         "content" : "You are a great assistant, you do what is asked of you and you follow instructions precisely"
        },
        {"role" : "user",
         "content" : userPrompt            
        },
        {"role" : "assistant",
         "content" : "Ok, please send me the data."            
        },
        {
            "role": "user",
            "content": userInput,
        }
    ]
    chat_completion = client.chat.completions.create(
    messages= messagesArr,
    model="mixtral-8x7b-32768",
    )
    return (chat_completion.choices[0].message.content)



""" #zuki ai code below, comment out if you want to use something else
import openai
def makeRequest(userInput):
    messagesArr = [
        {"role" : "system",
         "content" : "You are a great assistant, you do what is asked of you and you follow instructions precisely"
        },
        {"role" : "user",
         "content" : userPrompt            
        },
        {"role" : "assistant",
         "content" : "Ok, please send me the data."            
        },
        {
            "role": "user",
            "content": userInput,
        }
    ]
    openai.api_key = "zu-dd0f11b75f0ba8b279045c057961934e"    #for zuki ai
    openai.api_base = "https://zukijourney.xyzbot.net/v1"
    chat_completion = openai.ChatCompletion.create(
        stream=False, # can be true
        model="gpt-3.5-turbo",  # "claude-2",
    
        messages= messagesArr,
    )
    return(chat_completion.choices[0].message.content) 
    """



@app.route("/")
def index():
    return makeRequest("hi")

# define an app to return the read value from the gpt api
@app.route("/api", methods = ["GET"])
def returnAPI():
    message = request.args.get("message")
    print(message)
    if not message:
        return jsonify("INVALID REQUEST")
    
    GptApiResponse = str(makeRequest(message))
    response = {"response":GptApiResponse}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port= int("5000"), debug = True)
    
#good luck using this :) it barely works haha