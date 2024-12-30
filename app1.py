from flask import Flask, render_template,request, jsonify, session,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from schemas import VoyageSchema
from model import Voyage, db
import jwt
import datetime
from model import *



#################################### CONFIGURATION DE L APPLICATION FLASK #################################

#l'objet flask pour instancier une application
app = Flask(__name__)
#ma = Marshmallow(app)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://yvanna1:1234@localhost/catalogue'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy avec l'application
db.init_app(app) 




####################fonction de creation  du jwt pour recuperer les infos sur le voyage de l user ##


SECRET_KEY = 'votre_clé_secrète'  # Remplacez par une clé secrète plus complexe

def create_jwt(classe_voyage, ville_depart,ville_arrivee,heure_depart,date_voyage):
    payload = {
        'classe_voyage': classe_voyage,
        'ville_depart' :ville_depart,
        'ville_arrivee' :ville_arrivee,
        'heure_depart' : heure_depart,
        'date_voyage' : date_voyage,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  # Durée de validité du token
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token






################# CREATION D UNE INSTANCE DE VOYAGE##########################################################


SECRET_KEY = 'votre_clé_secrète'  # Assurez-vous que cela est sécurisé

@app.route('/catalogues/templates/choix_voyage', methods=['GET'], endpoint='choix_voyage_get')
def choix_voyage_get():
        
    token = request.args.get('token')
        
    if token is None:
        return jsonify({"error": "Token manquant."}), 400
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user_name=payload['user_name']
        user_surname = payload['user_surname']
        num_cni = payload['num_cni']
        email =payload['email']

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Le token a expiré."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalide."}), 401

    # Afficher le formulaire de choix de voyage
    return render_template('choix_voyage.html', token=token)












@app.route('/catalogues/templates/choix_voyage_post', methods=['POST'], endpoint='choix_voyage_post')
def choix_voyage_post():

    token = request.form.get('token')

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user_name=payload['user_name']
        user_surname = payload['user_surname']
        num_cni = payload['num_cni']
        email =payload['email']
       
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Le token a expiré."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalide."}), 401

        # Récupérer les données du choix de voyage depuis le formulaire
    classe_voyage = request.form['classe_voyage']
    ville_depart = request.form['ville_depart']
    ville_arrivee = request.form['ville_arrivee']
    heure_depart = request.form['heure_depart']
    date_voyage = request.form['date_voyage']

        #Réinitialiser la séquence avant d'insérer
    reset_sequence('voyage', 'id')

     
        # Créer une nouvelle instance de voyage
    new_voyage = Voyage(
            user_id=user_id,
            classe_voyage=classe_voyage,
            ville_depart=ville_depart,
            ville_arrivee=ville_arrivee,
            heure_depart=heure_depart,
            date_voyage=date_voyage,
        )

       # Ajouter et valider l'instance de voyage dans la base de données
    try:
        db.session.add(new_voyage)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": "Erreur lors de l'enregistrement du voyage.", "details": str(e)}), 500

#recuperation de l'id du voyage en cours
    id = new_voyage.id

    token2 = create_jwt(classe_voyage,ville_depart,ville_arrivee,heure_depart,date_voyage)
    return render_template('confirmation.html',id=id,token2=token2,token=token)











#######################Lecture de tous les choix de voyages enregistres######################################


@app.route('/catalogues/read',methods=['GET'])
def read():
    voyages=Voyage.Query.all() 
    return jsonify([voy.serialize() for voy in voyages])








#######################Modification d'un enregistrement de voyage############################################


#############definition de la route pour renvoyer le template pour la modification#############################

@app.route('/catalogues/templates/edition/<int:id>', methods=['GET'])
def edition(id):
    voyage = Voyage.query.get(id)
    
    if not voyage:
        return jsonify({'error': 'voyage non trouvé'}), 404

    # Afficher le formulaire de modification 
    return render_template('edition.html', voyage=voyage)





#############definition de la route pour recuperer les modifications et la valider dans le bd
@app.route('/catalogues/templates/update<int:id>', methods=['POST'])
def update_voyage(id):
    voyage = Voyage.query.get(id)
    
   
    
    if not voyage:
        return jsonify({'error': 'voyage non trouvé'}), 404

    # Récupérer les données du formulaire
    data = request.form 
    voyage.classe_voyage = data.get('classe_voyage', voyage.classe_voyage)
    voyage.ville_depart = data.get('ville_depart', voyage.ville_depart)
    voyage.ville_arrivee = data.get('ville_arrivee', voyage.ville_arrivee)
    voyage.heure_depart = data.get('heure_depart', voyage.heure_depart)
    voyage.date_voyage = data.get('date_voyage', voyage.date_voyage)



    # Enregistrer les modifications dans la base de données
    db.session.commit()
    id=voyage.id
    token2 = create_jwt(voyage.classe_voyage,voyage.ville_depart,voyage.ville_arrivee,voyage.heure_depart,voyage.date_voyage)
    return jsonify({'voyage mis a jour trouvé'})




##################### SUPPRESSION #########################################################################

#point de terminaison pour la suppression des voyages
@app.route('/catalogues/delete/<int:id>', methods = ['POST'])
def delete(id):
    voyage = Voyage.query.get(id)

   
    if not voyage:
        return jsonify({'error': 'Voyage non trouvé'}), 404

    # Supprimer le voyage de la session
    db.session.delete(voyage)
    db.session.commit()
    
    return redirect('http://127.0.0.1:5001/')








############################ execution de l'application ####################################################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 

