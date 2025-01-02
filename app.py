from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados (substitua pelo PostgreSQL do Railway)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de transação
class Transacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)

# Inicializa o banco de dados
db.create_all()

# Rota para adicionar transações
@app.route('/adicionar', methods=['POST'])
def adicionar():
    data = request.json
    nova_transacao = Transacao(
        descricao=data['descricao'],
        valor=data['valor'],
        tipo=data['tipo']
    )
    db.session.add(nova_transacao)
    db.session.commit()
    return jsonify({'message': 'Transação adicionada com sucesso!'})

# Rota para listar transações
@app.route('/transacoes', methods=['GET'])
def transacoes():
    transacoes = Transacao.query.all()
    return jsonify([{
        'id': t.id,
        'descricao': t.descricao,
        'valor': t.valor,
        'tipo': t.tipo
    } for t in transacoes])

if __name__ == '__main__':
    app.run(debug=True)
