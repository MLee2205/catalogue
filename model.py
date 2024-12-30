# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text



db = SQLAlchemy()


#classe voyage
class Voyage(db.Model):
    __tablename__ = 'voyage'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    classe_voyage=db.Column(db.String(50), nullable=False)
    ville_depart = db.Column(db.String(50), nullable=False)
    ville_arrivee = db.Column(db.String(50), nullable=False)
    heure_depart= db.Column(db.String(100),  nullable=False)
    date_voyage= db.Column(db.Date, nullable=False)
    
    def __repr__(self):
        return f'<Voyage {self.user_id}>'
    
    def serialize(self):
        return {
            
            'id': self.id,
            'user_id': self.user_id,
            'ville_depart': self.ville_depart,
            'ville_arrivee': self.ville_arrivee,
            'heure_depart': self.heure_depart,
            'date_voyage': self.date_voyage,

        }



#classe bus












def reset_sequence(table_name, id_column):
    # Exécute la commande pour réinitialiser la séquence
    sql = f"""
    SELECT setval(pg_get_serial_sequence(:table_name, :id_column), coalesce(max({id_column}), 1) )
    FROM {table_name};
    """
    db.session.execute(text(sql), {'table_name': table_name, 'id_column': id_column})
    db.session.commit()