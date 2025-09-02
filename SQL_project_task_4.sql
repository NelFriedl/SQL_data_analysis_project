-- Research question 4: 
-- "Existuje rok, ve kterém byl meziroční nárůst cen potravin výrazně vyšší než růst mezd (větší než 10 %)?"
WITH average_prices AS (	-- calculates the average product price per year
	SELECT
		year AS price_year,
      	AVG(CAST(average_price_value AS NUMERIC)) AS avg_price
    FROM
      	t_nela_friedlova_project_sql_primary_final
    GROUP BY
      	year
    ORDER BY
      	price_year
  ),
average_payroll AS (	-- calculates the average payroll across all industries per year
	SELECT
		year AS payroll_year,
      	AVG(CAST(average_payroll AS NUMERIC)) AS avg_payroll
    FROM
      	t_nela_friedlova_project_sql_primary_final
    GROUP BY
      	year
    ORDER BY
      	payroll_year
  ),
yearly_changes AS (	-- joins payroll and product price data from current and previous year
	SELECT
		pay.payroll_year,
      	pr.avg_price AS current_price,
     	LAG(pr.avg_price, 1) OVER (ORDER BY pay.payroll_year) AS prev_price,
      	pay.avg_payroll AS current_payroll,
      	LAG(pay.avg_payroll, 1) OVER (ORDER BY pay.payroll_year) AS prev_payroll
    FROM
      	average_payroll AS pay
    JOIN
      	average_prices AS pr
    ON 
    	pr.price_year = pay.payroll_year
    ORDER BY
      	payroll_year
  ),
percentage_change AS (	-- calculates year-on-year percentage change for both payroll and prices
	SELECT
		payroll_year,
      	((current_price - prev_price) / prev_price) * 100 AS price_change,
      	((current_payroll - prev_payroll) / prev_payroll) * 100 AS payroll_change
    FROM
      	yearly_changes
    WHERE
      	prev_price IS NOT NULL AND prev_payroll IS NOT NULL -- excludes years that have no previous year data for comparison
  )
SELECT	-- selects only years when the difference between price and payroll changes is greater than 10%
	payroll_year AS year,
  	ROUND(price_change, 2) AS "price_change_(%)",
  	ROUND(payroll_change, 2) AS "payroll_change_(%)",
  	ROUND(price_change - payroll_change, 2) AS "difference_(%)"
FROM
  	percentage_change
WHERE
	price_change - payroll_change > 10
ORDER BY
  	payroll_year;