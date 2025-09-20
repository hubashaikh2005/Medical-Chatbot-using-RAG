from flask import Flask, render_template, request, jsonify
from src.embedding import get_vectorstore
from src.prompt import get_chat_prompt
from src.chatbot import init_bot
from transformers import BartForConditionalGeneration, BartTokenizer
import traceback
import markdown

app = Flask(__name__)

#Initialize vectorstore and prompt
vectorstore = get_vectorstore(index_name="medical-chatbot")
template = get_chat_prompt()

#Initialize chatbot chain with memory
final_chain, memory, conv_chain = init_bot(vectorstore, template)

#Initialize BART model for input normalization
bart_model_name = "facebook/bart-base"
tokenizer = BartTokenizer.from_pretrained(bart_model_name)
model = BartForConditionalGeneration.from_pretrained(bart_model_name)

def normalize_text(text):         #Using BART to expand slang/abbreviations and fix simple typos
    inputs = tokenizer([text], return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def markdown_to_html(md_text):       #Convert Markdown text to HTML
    return markdown.markdown(md_text, extensions=["tables"])

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("question")
        normalized_input = normalize_text(user_input)
        response = conv_chain({"question": normalized_input})
        raw_answer = response.get("answer", "No answer returned")
        html_answer = markdown_to_html(raw_answer)

        return jsonify({"answer": html_answer})
    except Exception:
        print("ERROR in /ask route:")
        traceback.print_exc()
        return jsonify({"answer": "<p>Something went wrong. Please try again.</p>"}), 500

if __name__ == "__main__":
    print("Flask server started. QA ready.")
    app.run(host="0.0.0.0", debug=True)
