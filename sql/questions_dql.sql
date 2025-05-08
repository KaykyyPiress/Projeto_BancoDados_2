-- 1. Total de consultas por paciente
SELECT 
  p.id_paciente,
  p.nome,
  COUNT(c.id_consulta) AS total_consultas
FROM Paciente p
LEFT JOIN Consulta c ON p.id_paciente = c.id_paciente
GROUP BY p.id_paciente, p.nome
ORDER BY total_consultas DESC;

-- 2. Total de consultas realizadas por cada profissional
SELECT
  pr.id_profissional,
  pr.nome,
  COUNT(c.id_consulta) AS consultas_realizadas
FROM Profissional_Saude pr
LEFT JOIN Consulta c ON pr.id_profissional = c.id_profissional
GROUP BY pr.id_profissional, pr.nome
ORDER BY consultas_realizadas DESC;

-- 3. Quantidade de consultas por unidade de saúde
SELECT
  u.id_unidade_saude,
  u.nome,
  COUNT(c.id_consulta) AS consultas_unidade
FROM Unidade_Saude u
LEFT JOIN Consulta c ON u.id_unidade_saude = c.id_unidade_saude
GROUP BY u.id_unidade_saude, u.nome
ORDER BY consultas_unidade DESC;

-- 4. Distribuição de exames por tipo
SELECT
  tipo_exame,
  COUNT(*) AS total_exames
FROM Exame
GROUP BY tipo_exame;

-- 5. Pacientes que nunca tiveram consulta
SELECT
  p.id_paciente,
  p.nome
FROM Paciente p
WHERE NOT EXISTS (
  SELECT 1 FROM Consulta c 
   WHERE c.id_paciente = p.id_paciente
);

-- 6. Médias de pressão arterial (sistólica e diastólica)
SELECT
  ROUND(AVG((split_part(pressao_arterial,'/',1))::INT),1) AS media_sistolica,
  ROUND(AVG((split_part(pressao_arterial,'/',2))::INT),1) AS media_diastolica
FROM Consulta;

-- 7. Top 10 pacientes com mais exames
SELECT
  e.id_paciente,
  p.nome,
  COUNT(e.id_exame) AS exames_realizados
FROM Exame e
JOIN Paciente p ON e.id_paciente = p.id_paciente
GROUP BY e.id_paciente, p.nome
ORDER BY exames_realizados DESC
LIMIT 10;

-- 8. Profissionais que mais fizeram exames
SELECT
  e.id_profissional,
  pr.nome,
  COUNT(e.id_exame) AS exames_conduzidos
FROM Exame e
JOIN Profissional_Saude pr ON e.id_profissional = pr.id_profissional
GROUP BY e.id_profissional, pr.nome
ORDER BY exames_conduzidos DESC;

-- 9. Consultas de emergência por profissional
SELECT
  pr.id_profissional,
  pr.nome,
  COUNT(c.id_consulta) AS emergencias
FROM Profissional_Saude pr
JOIN Consulta c 
  ON pr.id_profissional = c.id_profissional
WHERE c.tipo = 'Emergência'
GROUP BY pr.id_profissional, pr.nome
ORDER BY emergencias DESC;

-- 10. Consultas por mês (últimos 12 meses)
SELECT
  date_trunc('month', c.data) AS mes,
  COUNT(*) AS total_consultas
FROM Consulta c
WHERE c.data >= (CURRENT_DATE - INTERVAL '12 months')
GROUP BY mes
ORDER BY mes;

-- 11. Último exame realizado por paciente
SELECT
  e.id_paciente,
  p.nome,
  MAX(e.data_realizacao) AS ultimo_exame
FROM Exame e
JOIN Paciente p ON e.id_paciente = p.id_paciente
GROUP BY e.id_paciente, p.nome
ORDER BY ultimo_exame DESC;

-- 12. Sintomas mais frequentes em consultas
SELECT
  unnest(string_to_array(lower(sintomas), ' ')) AS sintoma,
  COUNT(*) AS ocorrencias
FROM Consulta
GROUP BY sintoma
ORDER BY ocorrencias DESC
LIMIT 20;
