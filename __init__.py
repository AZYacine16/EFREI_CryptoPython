from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Génération d'une clé Fernet pour le cryptage/décryptage
key = Fernet.generate_key()
f = Fernet(key)

# Route principale pour afficher une page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')  # Assurez-vous d'avoir un fichier `hello.html` dans le dossier `templates`

# Route pour crypter une valeur
@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    try:
        valeur_bytes = valeur.encode()  # Conversion de la chaîne en bytes
        token = f.encrypt(valeur_bytes)  # Cryptage de la valeur
        return f"Valeur encryptée : {token.decode()}"  # Retourne le token sous forme de chaîne
    except Exception as e:
        return f"Erreur lors du cryptage : {str(e)}", 500

# Fonction pour décrypter une valeur
def decrypt_value(encrypted_value, key):
    try:
        fernet = Fernet(key)
        decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()  # Décryptage de la valeur
        return decrypted_value
    except Exception as e:
        raise ValueError(f"Erreur lors du décryptage : {str(e)}")

# Route pour décrypter une valeur (méthode POST)
@app.route('/decrypt/', methods=['POST'])
def decrypt():
    try:
        # Récupération des données JSON de la requête
        data = request.json
        if not data:
            return jsonify({"error": "Aucune donnée JSON fournie."}), 400

        encrypted_value = data.get('encrypted_value')
        key = data.get('key')

        # Validation des champs requis
        if not encrypted_value or not key:
            return jsonify({"error": "Veuillez fournir 'encrypted_value' et 'key'."}), 400

        # Décryptage de la valeur
        decrypted_value = decrypt_value(encrypted_value, key)
        return jsonify({"decrypted_value": decrypted_value})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Une erreur inattendue s'est produite : {str(e)}"}), 500

# Point d'entrée de l'application
if __name__ == "__main__":
    app.run(debug=True)
