from flask import Flask,render_template,request, jsonify
from flask_cors import CORS
from groq import Groq

systemPrompt = """
you are a great assistant
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

if the data says something in the lines of "Pax: 2+1+1free" or "Pax: 2+1Free" then the free part of the Pax is the number of infants, so 2+1free is 2 adults and 1 infant, 1+10free is 1 adult and 10 infants.

the dates must be in the DD-MM-YYYY format, all numbers, no month names, the seperators must be dashes, not backslashes.

the time format is HH:MM , without AM and PM.

the currency should always be returned as a word without a symbol, the allowed words are : dollar, euro, lira , pound.

Do not change the formatting of the template, your reply will only include the template above, you will never modify it, add to it, or remove from it, you will always follow it.

it is also very important that you follow the JSON template mentioned beforehand.
DO NOT put the JSON data inside an array, return only the JSON.
Do not comment on the input data, just send the output data and nothing with it.

if any of the data is missing, leave it blank, do not insert "?" or anything in its place.

The form must always be returned in English. If the input is in another language (mainly russian or german), first translate the data English then fill the template in English. Translate everything including the tour's name. send the form in English strictly.

you pay extra attention to match the data correctly, especially the number of adults,children, and infants, as well as the dates and times, and prices. Never modify or add data, this is extremely important.
"""

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key="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",
)

def makeRequestToGroq(userInput):
    chat_completion = client.chat.completions.create(
    messages=[
        {"role" : "system",
         "content" : systemPrompt
            
        },
        {
            "role": "user",
            "content": userInput,
        }
    ],
    model="mixtral-8x7b-32768",
    )
    return (chat_completion.choices[0].message.content)


@app.route("/")
def index():
    return makeRequestToGroq("hi")

# define an app to return the read value from the gpt api
@app.route("/api", methods = ["GET"])
def returnAPI():
    message = request.args.get("message")
    print(message)
    if not message:
        return jsonify("INVALID REQUEST")
    
    GptApiResponse = makeRequestToGroq(message)
    return GptApiResponse


    