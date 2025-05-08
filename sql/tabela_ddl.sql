-- DDL para criação das tabelas do Sistema de Saúde tipo SUS
DROP TABLE IF EXISTS Consulta CASCADE;
DROP TABLE IF EXISTS Exame CASCADE;
DROP TABLE IF EXISTS Unidade_Saude;
DROP TABLE IF EXISTS Paciente;
DROP TABLE IF EXISTS Profissional_Saude;


CREATE TABLE Profissional_Saude (
    id_profissional   SERIAL PRIMARY KEY,
    nome              VARCHAR(100) NOT NULL,
    cargo             VARCHAR(100) NOT NULL,
    tipo_registro     VARCHAR(50)  NOT NULL,
    registro_conselho VARCHAR(50)  NOT NULL UNIQUE
);

CREATE TABLE Paciente (
    id_paciente      SERIAL PRIMARY KEY,
    cpf              CHAR(11)     NOT NULL UNIQUE,
    nome             VARCHAR(100) NOT NULL,
    data_nascimento  DATE         NOT NULL,
    sexo             CHAR(1)      NOT NULL
        CHECK (sexo IN ('M','F','O'))
);

CREATE TABLE Unidade_Saude (
    id_unidade_saude SERIAL PRIMARY KEY,
    nome             VARCHAR(100) NOT NULL,
    tipo_unidade     VARCHAR(50)  NOT NULL,
    cidade           VARCHAR(100) NOT NULL,
    bairro           VARCHAR(100) NOT NULL
);

CREATE TABLE Exame (
    id_exame         SERIAL PRIMARY KEY,
    nome_exame       VARCHAR(100) NOT NULL,
    tipo_exame       VARCHAR(50)  NOT NULL,
    data_realizacao  TIMESTAMP    NOT NULL,
    id_profissional  INT          NOT NULL,
    id_paciente      INT          NOT NULL,
    FOREIGN KEY (id_profissional) REFERENCES Profissional_Saude(id_profissional),
    FOREIGN KEY (id_paciente)     REFERENCES Paciente(id_paciente)
);

CREATE TABLE Consulta (
    id_consulta      SERIAL PRIMARY KEY,
    data             TIMESTAMP    NOT NULL,
    tipo             VARCHAR(50)  NOT NULL,
    sintomas         TEXT,
    pressao_arterial VARCHAR(20),
    id_paciente      INT          NOT NULL,
    id_profissional  INT          NOT NULL,
    id_unidade_saude INT          NOT NULL,
    FOREIGN KEY (id_paciente)     REFERENCES Paciente(id_paciente),
    FOREIGN KEY (id_profissional) REFERENCES Profissional_Saude(id_profissional),
    FOREIGN KEY (id_unidade_saude)REFERENCES Unidade_Saude(id_unidade_saude)
);
