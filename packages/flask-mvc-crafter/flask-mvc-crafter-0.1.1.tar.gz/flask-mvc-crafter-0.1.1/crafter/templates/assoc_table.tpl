from . import db

${assoc_name} = db.Table('${assoc_name}', 
    db.Column('${model_1}_id', db.Integer, db.ForeignKey('${model_1}.id'), primary_key=True), 
    db.Column('${model_2}_id', db.Integer, db.ForeignKey('${model_2}.id'), primary_key=True)
)