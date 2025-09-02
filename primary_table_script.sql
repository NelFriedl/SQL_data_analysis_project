CREATE TABLE t_Nela_Friedlova_project_SQL_primary_final AS
WITH aggregated_payrolls AS (	-- calculates the average annual payroll from quarterly values
	SELECT
		payroll_year,
		industry_branch_code,
		AVG(value) AS average_payroll
	FROM
		czechia_payroll
	WHERE
		value_type_code = 5958 AND calculation_code = 200	-- filters rows where value refers to calculated salary
	GROUP BY
		payroll_year,
		industry_branch_code        
),
aggregated_prices AS (	-- calculates the average product prices for a given year
	SELECT
		EXTRACT(YEAR FROM cpr.date_from) AS price_year,
		cpr.category_code,
		cpc.name AS product_name,
		cpc.price_value,
		cpc.price_unit,
		AVG(cpr.value) AS average_price_value 
	FROM
		czechia_price AS cpr
	JOIN
		czechia_price_category AS cpc	-- joins price category details
    ON
		cpr.category_code = cpc.code
	GROUP BY
		EXTRACT(YEAR FROM cpr.date_from),
		cpr.category_code,              
    	cpc.name,
    	cpc.price_value,
    	cpc.price_unit
)
SELECT	-- joins the payroll and price data to create the final primary table
	cpay.payroll_year AS year,
	cpay.average_payroll,
	cpib.name AS industry_name,
	cpay.industry_branch_code,
	ap.category_code,
	ap.product_name,
	ap.average_price_value,
	ap.price_value,
	ap.price_unit
FROM
	aggregated_payrolls AS cpay
JOIN
	czechia_payroll_industry_branch AS cpib -- joins industry branch name
ON
	cpay.industry_branch_code = cpib.code 
JOIN
	aggregated_prices AS ap
ON
    cpay.payroll_year = ap.price_year
ORDER BY
	cpay.payroll_year,
	cpib.name;
