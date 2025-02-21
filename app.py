
from flask import Flask, render_template, redirect, request
from pymysql import MySQLError as erroBD
from dbconfig import *

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT * FROM tasks ORDER BY status ASC'
        cursor.execute(comandoSQL)
        tasks = cursor.fetchall()
    except erroBD as erro:
        print(f'Erro de BD: {erro}')
    finally:
        encerrar_db(cursor, conexao)
        return render_template('index.html', tasks = tasks)
    
@app.route('/newtask', methods=['GET', 'POST'])
def newtask():
    if request.method == 'POST':
        try:
            descricao = request.form['descricao']
            data = request.form['data']
            conexao, cursor = conectar_db()
            comandoSQL = 'INSERT INTO tasks(descricao, data) VALUES (%s, %s)'
            cursor.execute(comandoSQL,(descricao,data))
            conexao.commit()
        except Exception as erro:
            print(f'Erro de backend: {erro}')
        except erroBD as erro:
            print(f'Erro de banco de dados: {erro}')
        finally:
            encerrar_db(cursor, conexao)
    return redirect('/')

@app.route('/excluir/<int:id>')
def excluir(id):
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'DELETE FROM tasks WHERE id = %s'
        cursor.execute(comandoSQL, (id,))
        conexao.commit()
    except Exception as erro:
        print(f'Erro de backend: {erro}')
    except erroBD as erro:
        print(f'Erro de banco de dados: {erro}')
    finally:
        encerrar_db(cursor, conexao)
    return redirect('/')

@app.route('/editartask/<int:id>', methods=['GET', 'POST'])
def editartask(id):
    if request.method == 'GET':
        try:
            conexao, cursor = conectar_db()
            comandoSQL = 'SELECT * FROM tasks WHERE id = %s'
            cursor.execute(comandoSQL, (id,))
            task = cursor.fetchone()
            comandoSQL = 'SELECT * FROM tasks ORDER BY status ASC'
            cursor.execute(comandoSQL)
            tasks = cursor.fetchall()
        except Exception as erro:
            print(f"Erro de backend: {erro}")
        except erroBD as erro:
            print(f"Erro de banco de dados: {erro}")
        finally:
            encerrar_db(cursor, conexao)
            return render_template('index.html', editartask=True, tasks = tasks, task = task)
    
    if request.method == 'POST':
        try:
            conexao, cursor = conectar_db()
            descricao = request.form['descricao']
            data = request.form['data']
            comandoSQL = 'UPDATE tasks SET descricao = %s, data = %s WHERE id = %s'
            cursor.execute(comandoSQL, (descricao, data, id))
            conexao.commit()
        except Exception as erro:
            print(f"Erro de backend: {erro}")
        except erroBD as erro:
            print(f"Erro de banco de dados: {erro}")
        finally:
            encerrar_db(cursor, conexao)
            return redirect ('/')
        
@app.route('/alterarstatus/<int:id>')
def alterarstatus(id):
    try:
        conexao, cursor = conectar_db()
        comandoSQL = 'SELECT status FROM tasks WHERE id = %s'
        cursor.execute(comandoSQL, (id,))
        task = cursor.fetchone()
        if task['status'] == 'Pendente':
            novostatus = 'Concluída'
        else:
            novostatus = "Pendente"

        comandoSQL = 'UPDATE tasks SET status = %s WHERE id = %s'
        cursor.execute(comandoSQL, (novostatus, id))
        conexao.commit()
    except Exception as erro:
        print(f"Erro de backend: {erro}")
    except erroBD as erro:
        print(f"Erro de banco de dados: {erro}")
    finally:
        encerrar_db(cursor, conexao)
        return redirect ('/')

        


if __name__ == '__main__':
    app.run(debug=True)

