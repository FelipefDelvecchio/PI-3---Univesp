import mysql.connector
import os


def configurar_banco():
    try:
        host=os.getenv('host')
        user=os.getenv('user')
        password=os.getenv('password')
        database=os.getenv('Database')
        port=int(os.getenv('port', 3306))

        if not all([host, user, password, database]):
            raise ValueError("Uma ou mais variáveis de ambiente não estão configuradas corretamente.")
        
        
        conexao = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )

        if conexao.is_connected():
            print("Conexão com o banco de dados bem-sucedida!")
            return conexao
        else:
            print("Falha ao conectar ao banco de dados.")
            return None

    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
    except ValueError as e:
        print(f"Erro de valor: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return None
