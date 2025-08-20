-- Research question 2: 
-- "Kolik je možné si koupit litrů mléka a kilogramů chleba za první 
-- a poslední srovnatelné období v dostupných datech cen a mezd?"
WITH purchasing_power AS (
    SELECT
        t1.year,
        t1.industry_name,
        t1.industry_branch_code,
        t1.average_payroll,
        t1.average_price_value,
        t1.product_name,
        t1.price_unit,
        (average_payroll / average_price_value)::NUMERIC AS affordable_amount
    FROM
    	t_nela_friedlova_project_sql_primary_final AS t1
    WHERE
        t1.year IN (2006, 2018) 
        AND t1.category_code IN (111301, 114201)
    GROUP BY
        t1.year,
        t1.average_payroll,
        t1.industry_branch_code,
        t1.industry_name,
        t1.product_name,
        t1.average_price_value,
        t1.price_unit
)
SELECT
    year,
    industry_name,
    average_payroll,
    average_price_value,
    product_name,
    price_unit,    
    ROUND(affordable_amount) AS affordable_amount
FROM
    purchasing_power
ORDER BY
    year,
    industry_name;