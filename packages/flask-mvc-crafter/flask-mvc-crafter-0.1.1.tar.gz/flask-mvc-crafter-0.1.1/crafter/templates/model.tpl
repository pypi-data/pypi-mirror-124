from . import db

class $model_name_uc(db.Model):
    __tablename__ = '${table_name}'

    id = db.Column(db.Integer, primary_key=True)
    

    def __repr__(self):
        return f'<$model_name_uc {self.id}>'