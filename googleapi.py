from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
import os


app = Flask(__name__)

@app.route("/generate-interview", methods = ["GET"])
def generate_interview():

    # data = request.json
    data = request.get_json(silent=True) or {}


    company = data.get("company",  "Amazon")                      
    tech_stack = data.get("tech_stack",  """["java", "sql","python"]""")                
    no_of_questions = data.get("questions", "5")            
    type_of_interview = data.get("type","technical")              #technical or behavior oriented
    difficulty = data.get("level", "easy")                        #easy or medium or difficult

    prompt = f""" Hey, You are an recuter for {company} company. You have a candidate in interview call. You need to take an interview to that candidate.
                The tech stack is {tech_stack}.
                the number of questions to ask questions are {no_of_questions}.
                From the two types of interview types (i.e., Behaviour or technical), the interview now is supposed to be  {type_of_interview}.
                The difficulty level is {difficulty}.
                Now generate questions based on above explanantions. Don't generate special symbols because the questions you generate is to be read by a Ai Machine.
                The text you generate is to be conversational.
                insert new line character when ever required
                
    
    """
    client = genai.Client( api_key = os.getenv("gemini_key") )
    response  = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents=prompt

        )

    print(response.text)



    return jsonify({
        "questions" : response.text
    })

if __name__ == "__main__":
    load_dotenv()
    app.run("0.0.0.0",debug= True)

