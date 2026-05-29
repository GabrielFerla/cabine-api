-- 1. Leituras de uma cabine no ultimo dia
SELECT r.id, s.type, r.value, s.unit, r.read_at
FROM readings r JOIN sensors s ON s.id = r.sensor_id
WHERE s.cabin_id = 1 AND r.read_at >= NOW() - INTERVAL 1 DAY
ORDER BY r.read_at DESC;

-- 2. Top 5 cabines com mais alertas criticos
SELECT c.name, COUNT(*) AS criticos
FROM alerts a JOIN cabins c ON c.id = a.cabin_id
WHERE a.severity = 'critical'
GROUP BY c.id, c.name ORDER BY criticos DESC LIMIT 5;

-- 3. Ultima leitura de cada sensor de uma cabine
SELECT s.type, r.value, r.read_at
FROM sensors s JOIN readings r ON r.id = (
    SELECT r2.id FROM readings r2 WHERE r2.sensor_id = s.id
    ORDER BY r2.read_at DESC LIMIT 1)
WHERE s.cabin_id = 1;

-- 4. Culturas ativas por especie
SELECT species, COUNT(*) AS qtd FROM crops
WHERE status IN ('germinacao', 'crescimento') GROUP BY species;

-- 5. Alertas nao resolvidos por severidade
SELECT severity, COUNT(*) AS qtd FROM alerts
WHERE resolved = 0 GROUP BY severity;
