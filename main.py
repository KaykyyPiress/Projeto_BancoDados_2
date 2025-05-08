import os
import random
from faker import Faker
from db_connection import get_connection  # se você quiser executar direto no banco

fake = Faker('pt_BR')

def gerar_dml(
    num_profissionais=10,
    num_pacientes=50,
    num_unidades=5,
    num_exames=100,
    num_consultas=100
):
    statements = []

    # 1) Limpa dados na ordem de dependência (FKs para PKs)
    statements += [
        "DELETE FROM Consulta;",
        "DELETE FROM Exame;",
        "DELETE FROM Unidade_Saude;",
        "DELETE FROM Paciente;",
        "DELETE FROM Profissional_Saude;"
    ]

    # 2) Profissionais de Saúde
    for i in range(1, num_profissionais + 1):
        nome = fake.name().replace("'", "")
        cargo = random.choice(["Clínico Geral","Pediatra","Cardiologista","Enfermeiro"])
        tipo_registro = random.choice(["CRM","COREN","CRF","CRO"])
        registro = fake.bothify(text='??-#####')
        statements.append(
            f"INSERT INTO Profissional_Saude "
            f"(id_profissional, nome, cargo, tipo_registro, registro_conselho) VALUES "
            f"({i}, '{nome}', '{cargo}', '{tipo_registro}', '{registro}');"
        )

    # 3) Pacientes
    for i in range(1, num_pacientes + 1):
        nome = fake.name().replace("'", "")
        cpf = fake.cpf().replace('.', '').replace('-', '')
        nascimento = fake.date_of_birth(minimum_age=0, maximum_age=90)
        sexo = random.choice(['M','F','O'])
        statements.append(
            f"INSERT INTO Paciente "
            f"(id_paciente, cpf, nome, data_nascimento, sexo) VALUES "
            f"({i}, '{cpf}', '{nome}', '{nascimento}', '{sexo}');"
        )

    # 4) Unidades de Saúde
    tipos = ['UBS','UPA','Hospital Municipal','Pronto Socorro']
    for i in range(1, num_unidades + 1):
        tipo = random.choice(tipos)
        nome = f"{tipo} {fake.city()}"
        cidade = fake.city()
        bairro = fake.street_name()
        statements.append(
            f"INSERT INTO Unidade_Saude "
            f"(id_unidade_saude, nome, tipo_unidade, cidade, bairro) VALUES "
            f"({i}, '{nome}', '{tipo}', '{cidade}', '{bairro}');"
        )

    # 5) Exames
    exames_possiveis = ['Hemograma','Raio-X','Ultrassom','Eletrocardiograma']
    for i in range(1, num_exames + 1):
        exame = random.choice(exames_possiveis)
        tipo = random.choice(['Laboratorial','Imagem'])
        data = fake.date_time_between(start_date='-6M', end_date='now')
        prof = random.randint(1, num_profissionais)
        pac  = random.randint(1, num_pacientes)
        statements.append(
            f"INSERT INTO Exame "
            f"(id_exame, nome_exame, tipo_exame, data_realizacao, id_profissional, id_paciente) VALUES "
            f"({i}, '{exame}', '{tipo}', '{data}', {prof}, {pac});"
        )

    # 6) Consultas
    tipos_consulta = ['Primeira Consulta','Retorno','Emergência']
    for i in range(1, num_consultas + 1):
        data = fake.date_time_between(start_date='-6M', end_date='now')
        tipo = random.choice(tipos_consulta)
        sintomas = fake.sentence(nb_words=6).replace("'", "")
        pressao = f"{random.randint(80,140)}/{random.randint(50,90)}"
        pac = random.randint(1, num_pacientes)
        prof = random.randint(1, num_profissionais)
        uni = random.randint(1, num_unidades)
        statements.append(
            f"INSERT INTO Consulta "
            f"(id_consulta, data, tipo, sintomas, pressao_arterial, "
            f"id_paciente, id_profissional, id_unidade_saude) VALUES "
            f"({i}, '{data}', '{tipo}', '{sintomas}', '{pressao}', "
            f"{pac}, {prof}, {uni});"
        )

    return "\n".join(statements)

# def salvar_script(dml, path="sql/saude_dml.sql"):
#     os.makedirs(os.path.dirname(path), exist_ok=True)
#     with open(path, "w", encoding="utf-8") as f:
#         f.write(dml)
#     print(f"Script DML salvo em {path}")


def execute_script_from_files():
    """
    Executa os scripts 'ddl_script.sql' e 'dml_script.sql' da raiz do projeto.
    O DDL é executado primeiro, e só se ele for bem-sucedido o DML é executado.
    """
    ddl_path = "sql/tabela_ddl.sql"
    dml_path = "sql/dml_saude.sql"

    try:
        with open(ddl_path, 'r', encoding='utf-8') as ddl_file:
            ddl_script = ddl_file.read()
        with open(dml_path, 'r', encoding='utf-8') as dml_file:
            dml_script = dml_file.read()

        conn = get_connection()
        cur = conn.cursor()
        print("Conectado ao Supabase com sucesso.")

        # Executa DDL
        if ddl_script:
            print("Executando script DDL...")
            for comando in ddl_script.split(";"):
                comando = comando.strip()
                if comando:
                    cur.execute(comando + ";")
            conn.commit()
            print("Script DDL executado com sucesso.")

        # Executa DML
        if dml_script:
            print("Executando script DML...")
            for comando in dml_script.split(";"):
                comando = comando.strip()
                if comando:
                    cur.execute(comando + ";")
            conn.commit()
            print("Script DML executado com sucesso.")

        cur.close()
        conn.close()
        print("Todos os comandos foram executados com sucesso.")

    except FileNotFoundError as fe:
        print(f"Arquivo não encontrado: {fe.filename}")
    except Exception as e:
        print(f"Erro ao executar os comandos no Supabase: {e}")

if __name__ == "__main__":
    dml = gerar_dml()

    # Opcional: gravar o script em um arquivo
    with open("sql/dml_saude.sql", "w", encoding='utf-8') as file:
        file.write(dml)
    print("Script DML gerado e salvo com sucesso!")


    # se quiser já executar:
    execute_script_from_files()