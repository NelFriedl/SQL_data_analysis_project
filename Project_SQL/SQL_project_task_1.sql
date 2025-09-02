-- Reserch question 1: "Rostou v průběhu let mzdy ve všech odvětvích, nebo v některých klesají?"
WITH aggregated_salaries AS (	-- data aggregation to handle potential duplicate rows
	SELECT
		year,
		industry_name,
		AVG(average_payroll) AS average_payroll
	FROM
		t_nela_friedlova_project_sql_primary_final
	GROUP BY
		industry_name,
		year
)
SELECT DISTINCT
	t1.year,
	t1.industry_name,
	t1.average_payroll,
	LAG(t1.average_payroll, 1) OVER (PARTITION BY t1.industry_name ORDER BY t1.year) AS previous_year_salary,	
	t1.average_payroll - LAG(t1.average_payroll, 1) OVER (PARTITION BY t1.industry_name ORDER BY t1.year) AS salary_change,
	CASE
		WHEN t1.average_payroll > LAG(t1.average_payroll, 1) OVER (PARTITION BY t1.industry_name ORDER BY t1.year) THEN 'Increasing'
		WHEN t1.average_payroll < LAG(t1.average_payroll, 1) OVER (PARTITION BY t1.industry_name ORDER BY t1.year) THEN 'Decreasing'
		WHEN year = '2006' THEN 'No data'
		ELSE 'No Change'
	END AS payroll_trend
FROM
	aggregated_salaries AS t1
ORDER BY
	t1.year,
	t1.industry_name;