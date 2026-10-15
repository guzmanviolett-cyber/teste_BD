def add_usuario(cursor, id, nome, email):
    """Adiciona um usuario ao banco de dados"""
    cursor.execute('''INSERT INTO usuarios(id, nome, email) 
    VALUES(?, ?, ?)''', (id, nome, email))

def buscar_usuario(cursor, email):
    """Buscar usuario por email """
    cursor.execute("SELECT * FROM usuarios WHERE email = ?" (email))
    return cursor.fetchone()


