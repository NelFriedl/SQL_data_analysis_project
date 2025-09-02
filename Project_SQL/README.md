# SQL data analysis project: Czech payroll and prices

## Project overview
This project uses SQL to analyze official Czech Republic payroll and product price data from 2006 to 2018. The repository contains the SQL scripts used for data preparation, the resulting tables in .csv format, and the specific queries created to test several hypotheses.

## Methodology and results 
The project begins by joining multiple provided tables into a single, comprehensive primary table named t_nela_friedlova_project_SQL_primary_final. This primary table was used for all subsequent analysis and hypothesis testing.

1. **Are payrolls increasing across all industry branches, or are they decreasing in some?**
   - **Methodology**: A Common Table Expression (CTE) was used to aggregate data and calculate the average payroll per industry. The LAG window function was then applied to compare each year's payroll to the previous year. This allowed for the calculation of an absolute change and a descriptive trend. 
   - **Finding**: Generally, payrolls in most industries increased from 2007 to 2018. However, some sectors, such as 'těžba a dobývání', showed a descending trend. A general decrease in payroll was observed across the majority of industries in 2013.

2. **How many liters of milk and kilograms of bread could be purchased during the first and last comparable periods?**
   - **Methodology**: A CTE was used to calculate the average affordable quantity of bread (in kg) and milk (in l) across industry branches in the first (2006) and the last (2018) available years, storing the results in a new affordable_amount column.
   - **Finding**: Overall, the number of affordable kilograms of bread did not change significantly. This reflects a corresponding increase in both payroll and bread prices. In contrast, the average affordability of liters of milk increased in 2018 compared to 2006, likely reflecting its slower price growth. The absolute values are provided in the table below:

      |year|product_name|affordable_amount|
      |----|------------|-----------------|
      |2006|Bread|1313 kg|
      |2018|Bread|1365 kg|
      |2006|Milk|1466 l|
      |2018|Milk|1670 l|

3. **Which product category had the slowest price increase (lowest percentage year-on-year change)?**
   - **Methodology**: Average prices for individual product categories in 2006 and 2018 were calculated using a CTE. The Compound annual growth rate (CAGR) formula was then applied to determine the yearly percentage change, identifying the product with the slowest price increase.
   - **Finding**: The product whose price is increasing the slowest, is granulated sugar (cukr krystalový), whose price even decreased during the observed period.

4. **Was there a year where the year-on-year increase in product prices was significantly higher (more than 10%) than the increase in payrolls?**
   - **Methodology**: CTEs were used to calculate the average annual price and payroll. These values were joined with data from the previous year to calculate the year-on-year percentage change. The percentage difference between the two was then calculated.
   - **Finding**: The analysis showed that the price of no product increased by more than 10% compared to the change in payroll in the corresponding year. The largest difference recorded was in 2013, with a 6,65% price increase over the payroll change.
   
A secondary table, t_nela_friedlova_project_SQL_secondary_final, was created by joining the primary table with GDP data (economies table) to answer the final question.

5. **Does the level of GDP affect changes in payrolls and product prices? Specifically, if GDP increases, is there a corresponding increase in prices and payrolls in the same or following year?**
   - **Methodology**: A CTE was used to calculate the average annual values for GDP, prices, and payrolls. Year-on-year percentage changes were then calculated. The LEAD function was used to analyze changes in the following year.
   - **Finding**: The analysis showed no general correlation between changes in GDP and changes in payrolls or prices in either the same year or the following year.

## Conclusion
The SQL scripts and generated tables address the initial research questions. For enhanced data exploration and clarity, the results would benefit from visualization using business intelligence tools. 