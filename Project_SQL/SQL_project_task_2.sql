-- Research question 2: 
-- "Kolik je možné si koupit litrů mléka a kilogramů chleba za první 
-- a poslední srovnatelné období v dostupných datech cen a mezd?"
WITH purchasing_power AS (
	SELECT
		t1.year,
		t1.product_name,
		AVG(average_payroll / average_price_value)::NUMERIC AS affordable_amount
	FROM
		t_nela_friedlova_project_sql_primary_final AS t1
	WHERE
		t1.year IN (2006, 2018) 
		AND t1.category_code IN (111301, 114201)
	GROUP BY
		t1.year,
		t1.product_name
)
SELECT
	year,
	product_name,   
	ROUND(affordable_amount) AS affordable_amount
FROM
	purchasing_power
ORDER BY
	year,
	product_name;