from flask import render_template , request , jsonify
from app import app 
from app.conexao import configurar_banco

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/Cadastre")
def formulario():
    return render_template("formulario.html")

@app.route("/doar")
def doar():
    endereco = request.args.get("endereco")
    nome = request.args.get('nome')
    cidade = request.args.get("cidade")
    return render_template("doações.html" , endereco=endereco , nome=nome , cidade=cidade)


@app.route("/cadastrar" , methods = ["POST"])
def cadastrar():
    try:
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        cidade = request.form.get('cidade')
        print(nome , endereco , cidade)
        
        bd = configurar_banco()
        cursor = bd.cursor()

        # Inserir dados da instituição
        cursor.execute("""
            INSERT INTO instituicoes (nome)
            VALUES (%s)
        """, (nome,))
        
        # Capturar o ID 
        instituicao_id = cursor.lastrowid

        # Inserir dados do endereço
        cursor.execute("""
            INSERT INTO locais_doacao (instituicao_id, endereco, cidade)
            VALUES (%s, %s,%s)
        """, ( instituicao_id ,endereco, cidade))

     
        bd.commit()

        return jsonify({"mensagem": "Instituição e endereço adicionados com sucesso!"}), 201

    except Exception as e:
        bd.rollback()
        return jsonify({"erro": str(e)}), 400

    finally:
        bd.close()



@app.route("/cadastrar_doação" , methods = ["POST"])
def cadastrar_doação():
    bd = None
    try:
        nome = request.form.get('nome')
        quantidade = request.form.get('quantidade')
        
        try:
            quantidade = int(quantidade)
        except ValueError:
            return jsonify({"erro": "Quantidade inválida."})


        bd = configurar_banco()
        cursor = bd.cursor()

        # Pegar Id dda instituição com base no nome
        query_id_instituicao = """ select instituicoes.id  from instituicoes
                            where instituicoes.nome = %s """

        cursor.execute(query_id_instituicao , (nome,))
        id_instituicao = cursor.fetchone()

        # Verificar se a Instituição existe
        if not id_instituicao:
            return jsonify({"erro": "Instituição não encontrada."}), 404


        # Pegar o id do Local (Endereço e cidade)
        query_id_local = """select locais_doacao.id	from locais_doacao
                    where instituicao_id = %s;"""
        
        cursor.execute(query_id_local , (id_instituicao[0],))
        id_local = cursor.fetchone()

        if not id_local:
            return jsonify({"erro": "Local de doação não encontrado."}), 404

        print(id_local)

        # Inserir na tabela de doações
        query_quantidade= """INSERT INTO doacoes (local_id, quantidade)
                    VALUES (%s, %s) """

        cursor.execute(query_quantidade,(id_local[0],quantidade))


        bd.commit()

        return jsonify({"mensagem": "Quantidade Cadastrada com sucesso!"}), 201

    except Exception as e:
        bd.rollback()
        return jsonify({"erro": str(e)}), 400

    finally:
        bd.close()



