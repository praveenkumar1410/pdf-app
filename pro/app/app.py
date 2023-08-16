from flask import render_template, request, redirect, url_for
import os
import pdfminer.high_level
import openai

from flask import Flask

app = Flask(__name__)

openai.api_key = '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'

def extract_text_from_pdf(pdf_path):
    text = pdfminer.high_level.extract_text(pdf_path)
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pdf = request.files['pdf']
        pdf_filename = pdf.filename
        pdf_path = os.path.join('uploads', pdf_filename)

        # Create the 'uploads' directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)

        pdf.save(pdf_path)
        return redirect(url_for('question', pdf_path=pdf_path))
    return render_template('index.html')

@app.route('/question/<pdf_path>', methods=['GET', 'POST'])
def question(pdf_path):
    if request.method == 'POST':
        question = request.form['question']
        pdf_text = extract_text_from_pdf(pdf_path)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Q: {question}\nA:",
            max_tokens=100
        )
        answer = response.choices[0].text.strip()
        return render_template('answer.html', question=question, answer=answer)
    return render_template('question.html', pdf_text=extract_text_from_pdf(pdf_path), pdf_path=pdf_path)

if __name__ == '__main__':
    app.run(debug=True)
