-- Research question 3: 
-- "Která kategorie potravin zdražuje nejpomaleji (je u ní nejnižší percentuální meziroční nárůst)?"
WITH product_prices_by_year AS (
    SELECT
        year,
    	product_name,
        AVG(average_price_value) AS avg_price
    FROM
        "t_nela_friedlova_project_sql_primary_final"
    WHERE
        year IN (2006, 2018)
    GROUP BY
        year,
    	product_name
),
price_comparison AS (	
    SELECT
        p1.product_name,
        p1.avg_price AS price_in_2006,
        p2.avg_price AS price_in_2018
    FROM
        product_prices_by_year AS p1
    JOIN
        product_prices_by_year AS p2	-- joins the 2006 and 2018 prices on the same row for each product
    ON
        p1.product_name = p2.product_name
    WHERE
        p1.year = 2006
        AND p2.year = 2018
)
SELECT
    product_name,
    price_in_2006,
    price_in_2018,
    -- calculates the Compound Annual Growth Rate (CAGR, %)
    CAST((POWER(price_in_2018 / price_in_2006, 1.0 / 12) - 1) * 100 AS NUMERIC(10, 2)) AS cagr_percentage
FROM
    price_comparison
ORDER BY
    cagr_percentage ASC
LIMIT 1;	-- shows only the slowest average annual price increase
