from flask import Flask, render_template, request, jsonify, send_file
from src.embedding import get_vectorstore
from src.prompt import get_chat_prompt
from src.chatbot import init_bot
from transformers import BartForConditionalGeneration, BartTokenizer
import traceback
import markdown
import whisper
import os
import asyncio
import edge_tts
import uuid
import re

app = Flask(__name__)


vectorstore = get_vectorstore(index_name="medical-chatbot")
template = get_chat_prompt()
final_chain, memory, conv_chain = init_bot(vectorstore, template)

bart_model_name = "facebook/bart-base"
tokenizer = BartTokenizer.from_pretrained(bart_model_name)
bart_model = BartForConditionalGeneration.from_pretrained(bart_model_name)

whisper_model = whisper.load_model("tiny")


def normalize_text(text):
    try:
        inputs = tokenizer([text], return_tensors="pt")
        outputs = bart_model.generate(**inputs)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print("ERROR in normalize_text:", e)
        traceback.print_exc()
        return text


def markdown_to_html(md_text):
    return markdown.markdown(md_text, extensions=["tables"])


def clean_for_tts(text):
    text = re.sub(r"[\U00010000-\U0010ffff]", "", text)  # Remove emojis
    text = re.sub(r"#+\s*", "", text)   # Remove markdown headers
    text = re.sub(r"[*_`>~]", "", text)  # Remove other markdown chars
    return text.strip()


async def generate_tts_async(text, filename):
    try:
        communicate = edge_tts.Communicate(text, voice="en-GB-SoniaNeural")
        await communicate.save(filename)
        return filename
    except Exception as e:
        print("ERROR in Edge TTS:", e)
        traceback.print_exc()
        return None


def text_to_speech(text):
    filename = f"response_{uuid.uuid4().hex}.mp3"
    clean_text = clean_for_tts(text)   
    return asyncio.run(generate_tts_async(clean_text, filename))


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        user_input = request.json.get("question")
        tts_flag = request.json.get("tts", False)
        if not user_input:
            return jsonify({"answer": "<p>Please enter a question.</p>"}), 400

        normalized_input = normalize_text(user_input)
        response = conv_chain({"question": normalized_input})
        raw_answer = response.get("answer", "No answer returned")
        html_answer = markdown_to_html(raw_answer)

        audio_file = None
        if tts_flag:
            audio_file = text_to_speech(raw_answer)

        return jsonify(
            {
                "answer": html_answer,   
                "audio": f"/get_audio?file={audio_file}&v={uuid.uuid4().hex}" if audio_file else None,
            }
        )

    except Exception as e:
        print("ERROR in /ask route:", e)
        traceback.print_exc()
        return (
            jsonify({"answer": f"<p>Something went wrong: {e}</p>", "audio": None}),
            500,
        )


@app.route("/voice", methods=["POST"])
def voice():
    try:
        audio_file = request.files.get("audio")
        tts_flag = request.form.get("tts", "false").lower() == "true"
        if not audio_file:
            return jsonify({"answer": "<p>No audio uploaded.</p>", "audio": None}), 400

        tmp_path = "temp_audio.wav"
        audio_file.save(tmp_path)

        try:
            result = whisper_model.transcribe(tmp_path)
            user_input = result.get("text", "")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        if not user_input:
            return jsonify(
                {"answer": "<p>Could not transcribe audio.</p>", "audio": None}
            ), 400

        normalized_input = normalize_text(user_input)
        response = conv_chain({"question": normalized_input})
        raw_answer = response.get("answer", "No answer returned")
        html_answer = markdown_to_html(raw_answer)

        audio_file_out = None
        if tts_flag:
            audio_file_out = text_to_speech(raw_answer)

        return jsonify(
            {
                "answer": html_answer,
                "audio": f"/get_audio?file={audio_file_out}&v={uuid.uuid4().hex}" if audio_file_out else None,
            }
        )

    except Exception as e:
        print("ERROR in /voice route:", e)
        traceback.print_exc()
        return (
            jsonify({"answer": f"<p>Something went wrong: {e}</p>", "audio": None}),
            500,
        )


@app.route("/get_audio")
def get_audio():
    file = request.args.get("file")
    if file and os.path.exists(file):
        return send_file(file, mimetype="audio/mpeg")
    return "File not found", 404


if __name__ == "__main__":
    print("Flask server started. QA ready.")
    app.run(host="0.0.0.0", port=5000, debug=True)
