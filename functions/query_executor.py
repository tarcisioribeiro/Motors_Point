import mysql.connector
from dictionary.db_config import db_config

# Conexão com o banco
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Cadastro de cliente
def cadastrar_cliente(nome, telefone, email, endereco):
    sql = "INSERT INTO clientes (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)"
    valores = (nome, telefone, email, endereco)
    cursor.execute(sql, valores)
    conn.commit()
    print("Cliente cadastrado com sucesso!")
