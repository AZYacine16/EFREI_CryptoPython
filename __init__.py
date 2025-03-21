from cryptography.fernet import Fernet
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Génération de la clé par défaut (si l'utilisateur n'en fournit pas)
default_key = Fernet.generate_key()
f = Fernet(default_key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>', methods=['GET'])
def encryptage(valeur):
    """
    Route pour encrypter la valeur.
    L'option pour entrer une clé personnalisée est incluse.
    """
    key = request.args.get('key', default_key.decode())  # Récupère la clé personnalisée si elle est fournie
    fernet = Fernet(key.encode())  # Crée l'objet Fernet avec la clé
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = fernet.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:valeur>', methods=['GET'])
def decryptage(valeur):
    """
    Route pour décrypter la valeur.
    L'option pour entrer une clé personnalisée est incluse.
    """
    key = request.args.get('key', default_key.decode())  # Récupère la clé personnalisée si elle est fournie
    fernet = Fernet(key.encode())  # Crée l'objet Fernet avec la clé
    try:
        token = valeur.encode()  # Conversion str -> bytes
        decrypted_value = fernet.decrypt(token).decode()  # Décryptage
        return f"Valeur décryptée : {decrypted_value}"  # Retourne la valeur décryptée
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"  # Retourne l'erreur si le décryptage échoue

if __name__ == "__main__":
    app.run(debug=True)
