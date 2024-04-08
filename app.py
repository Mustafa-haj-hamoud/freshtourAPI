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

-you pay extra attention to match the data correctly, especially the number of adults,children, and infants, as well as the dates and times, and prices. Never modify or add data, this is extremely important.
-the PAX means the number of people, if the pax is 2, it means there are 2 adults. If the pax is 2+1, it means 2 adults and one child. if the pax is 2+1free, it means there are 2 adults and 1 infant, if it is 2+1+3free, it means 2 adults and 1 child and 3 infants, use these as examples and extrpolate accordingly. 
-the dates must be in the dd-mm-yyyy format, all numbers, no month names, the seperators must be dashes, not backslashes.
-the time format is hh:mm , without am and pm.
-the total fee must be a number without the currency added to it.
-the currency must always be returned as a word without a symbol, the allowed words are : dollar, euro, lira , pound.
-the phone number should include the + at the beginning if it was provided in the input data.
-Do not change the formatting of the template, your reply will only include the template above, you will never modify it, add to it, or remove from it, you will always follow it.
-it is also very important that you follow the JSON template mentioned beforehand.
-if any of the data is missing, leave the field blank, do not insert "?" or anything in its place, do not write a comment.
-The form must always be returned in English. If the input is in another language (mainly russian or german), first translate the data English then fill the template in English. Translate everything including the tour's name. send the form in English strictly.
-you will never say anything outside of the template, not a single word, just send the template and nothing else, if I ask for something else, reply with the exact words "I can't".
-Do not tell me that there isn't enough data to fill the template, just fill the provided data and leave the rest empty
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
    
#good luck using this :) it barely works 
#just kidding it works just fine :D