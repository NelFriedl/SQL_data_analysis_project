-- Research question 5: 
-- "Má výška HDP vliv na změny ve mzdách a cenách potravin? Neboli, pokud HDP vzroste 
-- výrazněji v jednom roce, projeví se to na cenách potravin či mzdách ve stejném nebo 
-- následujícím roce výraznějším růstem?"
WITH average_values AS (	-- calculates average values for every year
	SELECT DISTINCT
		year,
		AVG(CAST(gdp AS NUMERIC)) AS gdp,
		AVG(CAST(average_price_value AS NUMERIC)) AS avg_price,
		AVG(CAST(average_payroll AS NUMERIC)) AS avg_payroll
   	FROM
		t_nela_friedlova_project_sql_secondary_final
   	GROUP BY
   		year
   	ORDER BY
		year
  ),
yearly_changes AS (	-- generates values from current and previous year
	SELECT
		year,
      	gdp AS current_gdp,
      	LAG(gdp, 1) OVER (ORDER BY year) AS prev_gdp,
      	avg_price AS current_price,
      	LAG(avg_price, 1) OVER (ORDER BY year) AS prev_price,
      	avg_payroll AS current_payroll,
      	LAG(avg_payroll, 1) OVER (ORDER BY year) AS prev_payroll
    FROM
      	average_values
    ORDER BY
      	year
  ),
 percentage_change AS (	-- calculates percentage changes of prices and payroll
	SELECT
		year,
      	((current_gdp - prev_gdp) / prev_gdp) * 100 AS gdp_change,
      	((current_price - prev_price) / prev_price) * 100 AS price_change,
      	((current_payroll - prev_payroll) / prev_payroll) * 100 AS payroll_change
    FROM
      	yearly_changes
   	WHERE
		prev_gdp IS NOT NULL
  )
SELECT
	year,
  	ROUND(gdp_change, 2) AS "GDP_change_(%)",
  	ROUND(price_change, 2) AS "price_change_current_year_(%)",
  	ROUND(payroll_change, 2) AS "payroll_change_current_year_(%)",
  	-- change in following year (using LEAD)
  	ROUND(LEAD(price_change, 1) OVER (ORDER BY year), 2) AS "price_change_following_year_(%)",
  	ROUND(LEAD(payroll_change, 1) OVER (ORDER BY year), 2) AS "payroll_change_following_year_(%)"
FROM
	percentage_change
ORDER BY
  	year;