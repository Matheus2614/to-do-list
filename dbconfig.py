import pymysql

#Configuração do BD

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'senai'
DB_DATABASE = 'todolist'

#Função para conectar o DB
def conectar_db():
    conexao = pymysql.connect( #alterado aqui
        host = DB_HOST,
        user = DB_USER,
        password =  DB_PASSWORD,
        database = DB_DATABASE,
        cursorclass = pymysql.cursors.DictCursor #alterado aqui
    )

    cursor = conexao.cursor() #Para poder usar o proprio nome do campo invés de indices
    return conexao, cursor

#Função para encerrar o DB
def encerrar_db(cursor, conexao):
    cursor.close
    conexao.close