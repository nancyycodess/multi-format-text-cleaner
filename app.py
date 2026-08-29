from flask import Flask, render_template, request
import os

app = Flask(__name__)


def clean_text(text, remove_whitespace, formatting, pattern, replacement):
    text = text.encode("utf-8", errors="ignore").decode("utf-8")

    if remove_whitespace:
        text = " ".join(text.split())

    if pattern:
        text = text.replace(pattern, replacement)

    if formatting:
        text = text.strip()
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")

    return text


def batch_processing():
    input_folder = "input_files"
    output_folder = "output_files"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith(".txt"):
            with open(os.path.join(input_folder, file), "r", encoding="utf-8") as f:
                content = f.read()

            cleaned = clean_text(content, True, True, "", "")

            with open(os.path.join(output_folder, file), "w", encoding="utf-8") as f:
                f.write(cleaned)


@app.route("/", methods=["GET", "POST"])
def home():
    cleaned_text = ""

    if request.method == "POST":
        text = request.form.get("text", "")
        remove_whitespace = request.form.get("whitespace") == "on"
        formatting = request.form.get("formatting") == "on"
        pattern = request.form.get("pattern", "")
        replacement = request.form.get("replacement", "")

        cleaned_text = clean_text(
            text,
            remove_whitespace,
            formatting,
            pattern,
            replacement
        )

        batch_processing()

    return render_template("index.html", cleaned_text=cleaned_text)


if __name__ == "__main__":
    app.run(debug=True)