import psycopg2
from db_connection import get_connection

CHECKS = {
    "CPFs duplicados": """
        SELECT cpf, COUNT(*) AS ocorrencias 
        FROM Paciente 
        GROUP BY cpf 
        HAVING COUNT(*) > 1;
    """,
    "Registros de conselho duplicados": """
        SELECT registro_conselho, COUNT(*) AS ocorrencias 
        FROM Profissional_Saude 
        GROUP BY registro_conselho 
        HAVING COUNT(*) > 1;
    """,
    "Exames sem profissional válido": """
        SELECT e.id_exame, e.id_profissional 
        FROM Exame e 
        LEFT JOIN Profissional_Saude p ON e.id_profissional = p.id_profissional 
        WHERE p.id_profissional IS NULL;
    """,
    "Exames sem paciente válido": """
        SELECT e.id_exame, e.id_paciente 
        FROM Exame e 
        LEFT JOIN Paciente p ON e.id_paciente = p.id_paciente 
        WHERE p.id_paciente IS NULL;
    """,
    "Consultas sem paciente válido": """
        SELECT c.id_consulta, c.id_paciente 
        FROM Consulta c 
        LEFT JOIN Paciente p ON c.id_paciente = p.id_paciente 
        WHERE p.id_paciente IS NULL;
    """,
    "Consultas sem profissional válido": """
        SELECT c.id_consulta, c.id_profissional 
        FROM Consulta c 
        LEFT JOIN Profissional_Saude p ON c.id_profissional = p.id_profissional 
        WHERE p.id_profissional IS NULL;
    """,
    "Consultas sem unidade válida": """
        SELECT c.id_consulta, c.id_unidade_saude 
        FROM Consulta c 
        LEFT JOIN Unidade_Saude u ON c.id_unidade_saude = u.id_unidade_saude 
        WHERE u.id_unidade_saude IS NULL;
    """,
    "Exames com data futura": """
        SELECT id_exame, data_realizacao 
        FROM Exame 
        WHERE data_realizacao > NOW();
    """,
    "Consultas com data futura": """
        SELECT id_consulta, data 
        FROM Consulta 
        WHERE data > NOW();
    """,
    "Pressão arterial em formato inválido": r"""
        SELECT id_consulta, pressao_arterial 
        FROM Consulta 
        WHERE pressao_arterial !~ '^[0-9]{2,3}/[0-9]{2,3}$';
    """
}

def validar_consistencia():
    conn = get_connection()
    cur = conn.cursor()
    problemas = {}
    
    for descricao, sql in CHECKS.items():
        cur.execute(sql)
        rows = cur.fetchall()
        if rows:
            problemas[descricao] = rows
    
    cur.close()
    conn.close()
    return problemas

def imprimir_relatorio(problemas):
    if not problemas:
        print("Nenhum problema encontrado. Todos os dados estão consistentes!")
        return
    print("\n=== Relatório de Inconsistências Encontradas ===\n")
    for descricao, rows in problemas.items():
        print(f"{descricao}:")
        for row in rows:
            print("  ", row)
        print()

if __name__ == "__main__":
    problemas = validar_consistencia()
    imprimir_relatorio(problemas)

