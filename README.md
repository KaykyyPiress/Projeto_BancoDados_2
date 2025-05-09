# Sistema de Banco de Dados – Sistema de Saúde

## 📚 Objetivo do Projeto
Este projeto acadêmico visa implementar um sistema de banco de dados relacional que simula o funcionamento básico de um sistema de saúde. Com ele, é possível armazenar e gerenciar informações sobre:

- **Pacientes**
- **Profissionais de Saúde**
- **Unidades de Saúde**
- **Consultas**
- **Exames** 
---

## 🛠️ Estrutura do Projeto

O projeto contempla:
- Modelo Entidade-Relacionamento (ER)
- Modelo relacional em Terceira Forma Normal (3FN)
- Scripts SQL para criação (DDL) e manipulação dos dados
- Queries SQL específicas para testes funcionais
- Geração de dados fictícios para testes

---

## 📷 MER e ME

![ME](https://github.com/user-attachments/assets/e0a83cdb-b549-4791-908b-5a8d1c8a2ec8)

![MER](https://github.com/user-attachments/assets/3e69149c-7b6a-49cf-8080-94a589576717)

---

## ⚙️ Queries Implementadas

Algumas consultas SQL desenvolvidas para extrair insights e validar o sistema:

1. **Total de Consultas por Paciente:**
   - Retorna cada paciente com o total de consultas realizadas, permitindo identificar usuários mais ativos e potenciais necessidades de atenção especializada.

2. **Profissionais com Mais Exames Realizados:**
   - Lista os profissionais de saúde ordenados pela quantidade de exames que realizaram, auxiliando no balanço de carga de trabalho.

3. **Distribuição de Exames por Tipo:**
   - Apresenta a quantidade de exames agrupados por tipo (Laboratorial vs Imagem), oferecendo visão das demandas por categoria.
     
4. **Pacientes sem Consultas Registradas:**
   - Exibe pacientes que ainda não possuem consultas agendadas ou realizadas, viabilizando ações de acompanhamento ou correção de cadastro.

5. **Média de Pressão Arterial em Consultas:**
   - Calcula a média dos valores sistólico e diastólico de pressão arterial registrados, fornecendo indicadores clínicos da população atendida.

---

## 📂 Organização dos Arquivos

```
├── sql/
│   ├── dados_dml.sql
│   ├── questions_dql.sql
│   └── tabela_ddl.sql
├── README.md
├── db_connection.py
├── main.py
└── validador.py
```

---

## 🚀 Como Executar

1. Clone o repositório.
2. No terminal, execute os comandos:
   - `pip install faker`
   - `pip install psycopg2`
3. Em seguida, configure as seguintes variaveis de conexão com o supabase no arquivo db_connection.py:
   - `SUPABASE_USER` (linha 11)
   - `SUPABASE_PASSWORD` (linha 12)
3. Execute os scripts em ordem: 
   - `main.py`
   - `validadorSupa.py`
     
---

## 📝 Autores

- [Kayky Pires de Paula R.A.: 22.222.040-2](https://github.com/KaykyyPiress)
- [Mariane de Sousa Carvalho R.A.: 22.123.105-3](https://github.com/carvalhosmari)
- [Rafael Dias Silva Costa R.A.: 22.222.039-4](https://github.com/rafadias008)

---

📌 **Observação:** Projeto desenvolvido para fins acadêmicos, podendo ser adaptado para uso em cenários reais.

