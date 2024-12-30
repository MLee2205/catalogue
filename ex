Pour intégrer le user_id récupéré du microservice d'authentification dans votre microservice de catalogue de voyage, voici une approche détaillée :
1. Modéliser votre table Catalogue

Assurez-vous que votre modèle de base de données pour le catalogue de voyage a un champ user_id qui peut stocker l'identifiant de l'utilisateur. Par exemple, avec SQLAlchemy :

python

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CatalogueVoyage(Base):
    __tablename__ = 'catalogue_voyage'
    
    id = Column(Integer, primary_key=True)
    destination = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # Liaison avec la table users

    # Autres champs comme prix, description, etc.

2. Récupération du user_id

Dans votre microservice de choix de voyage, après avoir décodé le JWT pour obtenir le user_id, vous pouvez l'utiliser pour créer ou mettre à jour un enregistrement dans votre catalogue.
3. Exemple d'endpoint pour créer un voyage

Voici comment vous pourriez structurer un endpoint pour créer un voyage dans le microservice de catalogue :

python

from flask import Flask, request, jsonify
import jwt
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configurez votre base de données
# engine = create_engine('votre_url_base_de_données')
# Session = sessionmaker(bind=engine)

@app.route('/catalogue-voyage', methods=['POST'])
def create_voyage():
    token = request.headers.get('Authorization').split()[1]  # Extraire le token
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        user_id = payload['user_id']

        # Récupérer les données du voyage à partir du corps de la requête
        data = request.json
        destination = data.get('destination')

        # Créer un nouvel enregistrement dans le catalogue
        # session = Session()
        nouveau_voyage = CatalogueVoyage(destination=destination, user_id=user_id)
        # session.add(nouveau_voyage)
        # session.commit()

        return jsonify({"message": "Voyage créé avec succès.", "user_id": user_id}), 201

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expiré."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalide."}), 401

# Autres endpoints (GET, PUT, DELETE, etc.) pour gérer le CRUD

if __name__ == '__main__':
    app.run(debug=True)

4. Points importants

    Validation du token : Assurez-vous de toujours vérifier le token JWT pour garantir que l'utilisateur est authentifié.

    Enregistrement du voyage : Lors de l'ajout d'un voyage, utilisez le user_id obtenu pour le lier à cet enregistrement dans votre table de catalogue.

    CRUD : Pour d'autres opérations (GET, PUT, DELETE), assurez-vous de toujours récupérer le user_id de la même manière afin d'effectuer des opérations en fonction de l'utilisateur authentifié.

Conclusion

En suivant cette approche, vous pourrez gérer les voyages de chaque utilisateur en liant chaque enregistrement à son user_id dans votre catalogue de voyages. Cela facilite également la gestion des autorisations et des données liées à chaque utilisateur. Si vous avez d'autres questions ou avez besoin de précisions, n'hésitez pas à demander !

