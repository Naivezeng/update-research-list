## 1. Generate Names String in SQL in parameter
* Execute `get_target_names_in()` get NAME_PARA

## 2. Store Information
> SQL: SELECT employee_ID, name, MIN(px) FROM `fudan_research_paper_zwqk` WHERE name in (NAME_PARA) GROUP BY name;
* Export data with 'csv' format, and save to the root directory naming 'teacher_cn_research.csv'
> SQL: SELECT employee_ID, name, MIN(px) FROM `fudan_research_paper_ywqk` WHERE name in (NAME_PARA) GROUP BY name;
* Export data with 'csv' format, and save to the root directory naming 'teacher_en_research.csv'

## 3. Generate SQL Script
* Execute 'generate_sql()'

## 4. Execute SQL in target_sql.txt