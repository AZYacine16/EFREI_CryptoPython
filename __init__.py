from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Génération de la clé par défaut (si l'utilisateur n'en fournit pas)
default_key = Fernet.generate_key().decode()  # Convertir en chaîne pour une utilisation facile

@app.route('/')
def hello_world():
    """
    Route principale pour afficher une page d'accueil.
    """
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>', methods=['GET'])
def encryptage(valeur):
    """
    Route pour encrypter la valeur.
    L'utilisateur peut fournir une clé personnalisée via le paramètre `key`.
    """
    try:
        # Récupère la clé personnalisée si elle est fournie, sinon utilise la clé par défaut
        key = request.args.get('key', default_key)

        # Vérifie que la clé est valide
        try:
            fernet = Fernet(key.encode())  # Crée l'objet Fernet avec la clé
        except ValueError:
            return jsonify({"error": "Clé invalide. La clé doit être une chaîne de 32 bytes encodée en base64."}), 400

        # Cryptage de la valeur
        valeur_bytes = valeur.encode()  # Conversion str -> bytes
        token = fernet.encrypt(valeur_bytes)  # Encrypte la valeur
        return jsonify({"encrypted_value": token.decode()})  # Retourne le token en str

    except Exception as e:
        return jsonify({"error": f"Une erreur inattendue s'est produite : {str(e)}"}), 500

@app.route('/decrypt/<string:valeur>', methods=['GET'])
def decryptage(valeur):
    """
    Route pour décrypter la valeur.
    L'utilisateur peut fournir une clé personnalisée via le paramètre `key`.
    """
    try:
        # Récupère la clé personnalisée si elle est fournie, sinon utilise la clé par défaut
        key = request.args.get('key', default_key)

        # Vérifie que la clé est valide
        try:
            fernet = Fernet(key.encode())  # Crée l'objet Fernet avec la clé
        except ValueError:
            return jsonify({"error": "Clé invalide. La clé doit être une chaîne de 32 bytes encodée en base64."}), 400

        # Décryptage de la valeur
        token = valeur.encode()  # Conversion str -> bytes
        decrypted_value = fernet.decrypt(token).decode()  # Décryptage
        return jsonify({"decrypted_value": decrypted_value})  # Retourne la valeur décryptée

    except InvalidToken:
        return jsonify({"error": "Clé invalide ou valeur cryptée corrompue."}), 400
    except Exception as e:
        return jsonify({"error": f"Une erreur inattendue s'est produite : {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
