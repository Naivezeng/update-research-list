## 1. Generate Names String in SQL in parameter
* Execute `get_target_names_in()` get NAME_PARA

## 2. Store Information
> SQL: SELECT employee_ID, name, MIN(px) FROM `fudan_research_paper_zwqk` WHERE name in (NAME_PARA) GROUP BY name;
* Export data with 'csv' format, and save to the root directory naming 'teacher_cn_research.csv'
> SQL: SELECT employee_ID, name, MIN(px) FROM `fudan_research_paper_ywqk` WHERE name in (NAME_PARA) GROUP BY name;
* Export data with 'csv' format, and save to the root directory naming 'teacher_en_research.csv'

## 3. Generate SQL Script
* Execute 'generate_sql()'

## 4. Correct SQL Script if any quota syntax error


## 5. Execute SQL in target_script.sql
* phpmyadmin seems only permit 10 insert at one time, so do it manually in batches.


## Other SQL Note:
> SELECT name, COUNT(DISTINCT(employee_ID)) AS cnt FROM `fudan_basic_info` WHERE 1=1 group by name;
> SELECT name, COUNT(DISTINCT(employee_ID)) AS cnt FROM `fudan_basic_info` WHERE status = '在职' group by name;
> SELECT name, cnt FROM ( SELECT name, COUNT(DISTINCT(employee_ID)) AS cnt FROM `fudan_basic_info` WHERE status = '在职' group by name ) t where cnt > 1;
> INSERT INTO `fudan_research_paper_zwqk` (`ID`, `employee_ID`, `ISI_number`, `name`, `rank`, `subject`, `journal`, `year`, `head`, `end`, `hidden`, `px`) VALUES (NULL, 'aa123', NULL, 'aa123', NULL, '11123', '123123', '123123', NULL, NULL, '0', '0');