# News Log Analysis
This python application analyzes logs in a database provided by Udacity.com for the Logs Analysis Project as part of the Full Stack Web Developer Nanodegree program. The results of the analysis will present the top three articles successfully accessed (STATUS 200 OK) over the life of the log files, the names of the authors of all known articles ordered by popularity (total views) in descending order, and the day(s) on which users received a non-"200 OK" response from the server more than 1% of the time.

## Requirements
This is a python program and thus, you will need a python interpreter.  For more information, head on over to [https://www.python.org/about/](https://www.python.org/about/). The **News Log Analysis** program has been tested in the following Python versions:
*  3.5.2
* 2.7.12

One the following library(ies) must be installed to appropriately connect to the PostgreSQL database.
* psycopg2
* psycopg2-binary

**Library(ies) for Python2 install code**
```
pip install psycopg2
pip install psycopg2-binary
```
**Library(ies) for Python3 install code**
```
pip3 install psycopg2
pip3 install psycopg2-binary
```
**Note:**  *If installing the library(ies) on a virtual machine, you may need to include `--user` at the end of the pip/pip3 line(s) above.*

## Directions
From a console program use the following code to run the program and display the results.  The results will display in the console.
$  ```python news-analysis.py``` or $  ```python3 news-analysis.py```
*(depending on the version of Python you want to use.)*

## Database Views
The following views were created to make accessing the aggregated data a little simpler.
### View 1
**View Name:** w_articles_alltime_popularity
**View Description:** Queries the log table to sum the number of views of each article, its author, and the author's unique ID.
```
CREATE VIEW vw_articles_alltime_popularity AS
select  a.Title
        , count(l.id) as cnt
        , au.name
        , au.id
from    log as l
        inner join articles as a
            on a.slug = right(l.path, length(l.path) - 9)
        inner join authors as au
            on au.id = a.author
where   path like '/article/%'
        and status like '200%'
group by    a.title, au.name, au.id
order by    cnt desc;
```

### View 2
**View Name:** vw_errors_by_day_404
**View Description:** Queries the log table to sum the total 404 errors for each day.
```
CREATE VIEW vw_errors_by_day_404 AS
select  date_trunc('day', time) as day
		, count(*) as ErrorCount
from    log
where   status like '404%'
group by	day
order by	day;
```

### View 3
**View Name:** vw_total_view_attempts_by_day
**View Description:** Queries the log table to sum the total page view attempts each day
```
CREATE VIEW vw_total_view_attempts_by_day AS
select  date_trunc('day', time) as day
		, count(*) as TotalViewAttempts
from    log
group by	day
order by	day;
```
## License
[MIT License](https://opensource.org/licenses/MIT, "MIT License")
