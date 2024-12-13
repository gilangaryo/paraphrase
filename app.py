from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
print(os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    try:
        data = request.json
        input_text = data.get('text', '')
        additional_instructions = data.get('additional_instructions', '')

        print("tambahan perintah", additional_instructions)
        if not input_text:
            return jsonify({"error": "No text provided"}), 400

        system_message_content = (
            "Anda adalah asisten virtual yang sangat ahli dalam memparafrase teks secara profesional. "
            "Tugas Anda adalah memparafrase teks dalam bahasa Indonesia menggunakan gaya bahasa formal "
            "yang sesuai untuk konteks pendidikan, akademik, atau profesional. "
            "Parafrase harus tetap mempertahankan makna asli dari teks, tetapi menggunakan variasi struktur kalimat "
            "dan kosakata yang lebih kaya untuk menciptakan hasil yang menarik, informatif, dan mudah dipahami. "
            "Hindari penggunaan bahasa sehari-hari atau informal, dan pastikan hasilnya terdengar seperti "
            "ditulis oleh seorang ahli di bidangnya. "
            "Tambahkan elemen kejelasan dan keteraturan jika memungkinkan, sehingga teks lebih terstruktur. "
            "Hal paling penting adalah anda bukan AI. Anda adalah asisten yang dapat berbahasa indonesia baik dan benar. "
            "jika ada istilah asing seperti framework, library, dll jangan diubah jadi bahasa indonesia."
        )

        # Jika ada additional instructions, tambahkan di akhir konten sistem
        if additional_instructions.strip():
            system_message_content += f"\nInstruksi tambahan: {additional_instructions}"

        # New OpenAI API call structure
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_message_content
                },
                {
                    "role": "user",
                    "content": f"Parafrase teks berikut dengan gaya yang diminta: {input_text}"
                }
            ]
        )

        # Extract paraphrased text
        paraphrased_text = response['choices'][0]['message']['content'].strip()

        return jsonify({"paraphrased_text": paraphrased_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
