from . import db
from .base import ModeloBase

# Dica: data_inicio/data_fim usam db.Date (importe Date se precisar)


class Locacao(ModeloBase):
    __tablename__ = "locacoes"

    # TODO ALUNO: FK cliente_id → clientes_locadora.id
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes_locadora.id"), nullable=False)
    # TODO ALUNO: FK veiculo_id → veiculos.id
    veiculo_id = db.Column(db.Integer, db.ForeignKey("veiculos.id"), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)

    # TODO ALUNO: relationship cliente e veiculo

    cliente = db.relationship("ClienteLocadora",back_populates="locacoes")
    veiculo = db.relationship("Veiculo", back_populates="locacoes")

    @classmethod
    def listar_com_detalhes(cls):
        return cls.query.order_by(cls.data_criacao.desc()).all()
    

    @classmethod
    def salvar(cls, cliente_id, veiculo_id, data_inicio, data_fim, valor_total):
        locacao = cls(cliente_id=cliente_id, veiculo_id=veiculo_id, data_inicio=data_inicio, data_fim=data_fim, valor_total=valor_total or None)
        db.session.add(locacao)
        db.session.commit()
        return locacao

    def atualizar(self, cliente_id, veiculo_id, data_inicio, data_fim, valor_total):
        self.cliente_id = cliente_id
        self.veiculo_id = veiculo_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.valor_total = valor_total or None
        db.session.commit()

    def excluir(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Locacao {self.id}>"

