import mysql.connector
from mysql.connector import errorcode

print('Conectando...')

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root'
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
else:
    print('Conectado')

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS jogoteca;")

cursor.execute("CREATE DATABASE jogoteca;")

cursor.execute("USE jogoteca")

# criando tabelas
TABLES = {}

TABLES['Jogos'] = ('''
    CREATE TABLE `jogoteca`.`jogos` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(50) NOT NULL,
      `categoria` VARCHAR(40) NOT NULL,
      `console` VARCHAR(20) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `jogoteca`.`usuarios` (      
      `nome` VARCHAR(20) NOT NULL,
      `nickname` VARCHAR(8) NOT NULL,
      `senha` VARCHAR(100) NOT NULL,
      PRIMARY KEY (`nickname`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print('Criando tabela {}:'.format(tabela_nome), end='')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela já existe')
        else:
            print(err.msg)
    else:
        print('ok')

# inserindo usuários
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) values (%s,%s,%s)'

usuarios = [
    ("Bruno Divino", "BD", "alohomora"),
    ("Kaue Sabino", "KS", "kaue123"),
]

cursor.executemany(usuario_sql,usuarios)

cursor.execute('select * from jogoteca.usuarios')
print('---------------- Usuários ----------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo jogos
jogo_sql = 'INSERT INTO jogos (nome, categoria, console) values (%s,%s,%s)'

jogos = [
    ("Tetris", "Puzzle", "Atari"),
    ("God of War", "Hack and Slash", "PS2"),
    ("Mortal Kombat I", "Luta", "PS2"),
    ("Valorant", "FPS", "PC"),
    ("Crash Titans", "Hack n Slash", "PS2"),
    ("Need for Speed", "Corrida", "PS2"),
]

cursor.executemany(jogo_sql,jogos)

cursor.execute('select * from jogoteca.jogos')
print('---------------- Jogos ----------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando pra gravar no banco
conn.commit()

cursor.close()
conn.close()
