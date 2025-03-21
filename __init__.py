from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #yacine

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

# Fonction pour décrypter une valeur
def decrypt_value(encrypted_value, key):
    try:
        fernet = Fernet(key)
        decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
        return decrypted_value
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"

# Route pour décrypter
@app.route('/decrypt/', methods=['POST'])
def decrypt():
    data = request.json
    encrypted_value = data.get('encrypted_value')
    key = data.get('key')

    if not encrypted_value or not key:
        return jsonify({"error": "Veuillez fournir 'encrypted_value' et 'key'."}), 400

    decrypted_value = decrypt_value(encrypted_value, key)
    return jsonify({"decrypted_value": decrypted_value})
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
