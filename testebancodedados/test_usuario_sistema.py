import pytest
import sqlite3
from usuario_sistema import add_usuario, buscar_usuario

@pytest.fixture

def db_conexao():
    """ Fixture que configura una conexão con o banco de dados sqlite temporario e garante
    a limpeza dos recursos após do teste"""

    conn = sqlite3.connect(":memory:") #Cria DB em memória
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE usuarios(
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE)''')
    conn.commit()
    yield conn, cursor

    conn.close()
@pytest.mark.parametrize(
    ("id", "nome", "email", "nome_esperado"),
    [
       ( 1, "Ashlee", "guzmanviolett@gmail.com", "Ashlee"),
       (2, "Aybar", "aybarazo@email.com", "Aybar"),
       (3, "Alejandra", "alevalen@gmail.com", "Alejandra")
    ]
    )
@pytest.mark.unit #É so uma etiqueta. Sem registro no pytest.init

def test_add_usuarios(db_conexao, id, nome, email, nome_esperado):
    conn, cursor = db_conexao
    add_usuario(cursor, id, nome, email)
    resultado = buscar_usuario(cursor, email)
    assert resultado is not None
    assert resultado[1] == nome_esperado
    assert resultado[2] == email

@pytest.mark.integration
@pytest.mark.slow
def test_buscar_usuario_com_email_inexistente(db_conexao):
    import time

    conn, cursor = db_conexao

    for i in range(100):

        add_usuario(cursor, i, f"User{i}", f"User{i}@example.com")
        # inserte UM usuario por interação. As f-string
        # sustituem o i por o valor atual
        #i=0 -> id=0, nome="User0", email="user@example.com"

    conn.commit()
    #confirma todas as inserções de vez

    #pause
    time.sleep(2)

    for i in range(100):
        resultado = buscar_usuario(cursor, f"User{i}@example.com" )
        assert resultado is not None

        assert resultado[1] == f"User{i}"
        assert resultado[2] ==f"User{i}@example.com"

