from loja import db
from loja.produtos.models import Addproduto


class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(200), unique=False, nullable=False)

    idproduto = db.Column(db.Integer, db.ForeignKey('addproduto.id'),nullable=False)
    addproduto = db.relationship('Addproduto',backref=db.backref('addprodutos', lazy=True))

    quantidade = db.Column(db.Integer, nullable=False)
    
    
    def __repr__(self):
            return '%r' % self.idproduto
    
db.create_all()

    
        