CREATE TABLE t_nela_friedlova_project_SQL_secondary_final AS
SELECT 
	tnf.*,
	e.gdp
FROM 
	economies AS e
JOIN
	t_nela_friedlova_project_sql_primary_final AS tnf
ON
	e.year = tnf.year
WHERE
	e.country = 'Czech Republic'
ORDER BY 
	tnf.year;