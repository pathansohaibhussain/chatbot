from flask import Flask, render_template, request, jsonify
import aiml
import os

app = Flask(__name__)

# Initialize AIML Kernel
kernel = aiml.Kernel()

# Load brain file or AIML files
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="aiml/std-startup.xml", commands="load aiml b")
    kernel.saveBrain("bot_brain.brn")


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/ask", methods=["POST"])
def ask():
    message = request.form["messageText"].strip()

    if message.lower() == "save":
        kernel.saveBrain("bot_brain.brn")
        return jsonify({"status": "OK", "answer": "Brain saved!"})

    bot_response = kernel.respond(message)
    return jsonify({"status": "OK", "answer": bot_response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
