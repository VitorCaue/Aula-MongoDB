from flask import Flask, jsonify, request
from config import bd, pedidos_collection, produtos_collection, clientes_collection

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World."

#Criação de classes
class Clientes():
    def __init__(self, id_cliente, nome, data_nascimeto, email, cpf,):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimeto
    
    def serialize(self):
        return{
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento,
        }

class Produtos():
    def __init__(self,id_produto,nome,descricao,preco,categoria):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria

    def serialize(self):
        return{
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "categoria": self.categoria,
        }
    
class Pedidos():
    def __init__(self,id_produto,data_pedido,id_cliente,valor):
        self.id_produto = id_produto
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido
        self.valor = valor

    def serialize(self):
        return{
            "id_produto": self.id_produto,
            "id_cliente": self.id_cliente,
            "data_pedido": self.data_pedido,
            "valor": self.valor,
        }

#Criação de rotas

@app.route("/clientes")
def lista_clientes():
    try:
        clientes = clientes_collection.find()

        clientes_serializado = []
        for cliente in clientes:
            cliente['_id'] = str(cliente['_id'])
            clientes_serializado.append(cliente)
        
        return jsonify(clientes_serializado), 200

    except Exception as e:
        print(f"Erro: {e}")
        return "Erro ao listar clientes", 500


@app.route("/insertCliente")
def set_cliente():
    dados = request.get_json()
    novo_cliente = Clientes(
        id_cliente = dados['id_cliente'],
        nome= dados['nome'],
        email= dados['email'],
        cpf= dados['cpf'],
        data_nascimento = dados['data_nascimento']
    )

    resultado = clientes_collection.insert_one(novo_cliente.serialize())

    if resultado.inserted_id:
        novo_cliente.id_cliente = str(resultado.inserted_id)
        return jsonify (novo_cliente.serialize()),201
    else:
        return "Erro ao inserir cliente.", 500

if __name__ == "__main__":
    app.run(debug=True)