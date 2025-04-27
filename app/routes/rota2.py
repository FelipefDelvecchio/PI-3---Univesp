from flask import  jsonify 
from app import app
from app.conexao import configurar_banco


@app.route("/dados" , methods=['GET'])
def dados_institucao():
    try:
        bd = configurar_banco()
        cursor = bd.cursor()

        inst_menos_doadas = """SELECT 
                                instituicoes.nome, 
                                locais_doacao.endereco, 
                                locais_doacao.cidade,
                                COALESCE(SUM(doacoes.quantidade), 0) AS total_doacoes  -- Substitui NULL por 0
                            FROM locais_doacao
                                LEFT JOIN instituicoes ON locais_doacao.instituicao_id = instituicoes.id
                                LEFT JOIN doacoes ON doacoes.local_id = locais_doacao.id
                            GROUP BY locais_doacao.id
                            ORDER BY total_doacoes ASC
                            LIMIT 3;"""
        
        cursor.execute(inst_menos_doadas)
        inst_doadas = cursor.fetchall()

        dados1 = [inst_doadas[0][0], inst_doadas[0][1] , inst_doadas[0][2]]
        dados2 = [inst_doadas[1][0] , inst_doadas[1][1], inst_doadas[1][2]]
        dados3 = [inst_doadas[2][0] , inst_doadas[2][1] , inst_doadas[2][2]]
        cursor.close()
        bd.close()

        return jsonify(dados1=dados1, dados2=dados2, dados3=dados3)
    except Exception as e : 
        print("erro" , e)   
        return jsonify(error="Erro ao processar a solicitação"), 500



@app.route("/grafico")
def grafico():
    try:
        bd = configurar_banco()
        cursor = bd.cursor()

        grafico_dados = """SELECT instituicoes.nome, SUM(doacoes.quantidade) AS total_doado
                            FROM doacoes
                            JOIN locais_doacao ON doacoes.local_id = locais_doacao.id
                            JOIN instituicoes ON locais_doacao.instituicao_id = instituicoes.id
                            GROUP BY instituicoes.nome
                            ORDER BY total_doado DESC;"""

        cursor.execute(grafico_dados)
        dados = cursor.fetchall()

        dados_convertidos = [{"nome": nome, "total_doado": total_doado} for nome, total_doado in dados]

        return jsonify(dados=dados_convertidos)
    except Exception as e:
        print("erro", e)
        return jsonify(error="Erro ao processar a solicitação" ) , 500
    
    


      