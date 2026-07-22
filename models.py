from flask_sqlalchemy import SQLAlchemy

#conexão com o banco de dados
db=SQLAlchemy ()

class Lista (db.Model):
    __tablename__ = "lista"
    id=db.Column(
        db.Integer,
        primary_key=True
    )

    texto = db.Column(
    db.Text,
    nullable=False
)

    data = db.Column(
    db.String(50)
)
    
    concluida = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )