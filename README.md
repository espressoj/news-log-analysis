Views Created:

VIEW 1 - Queries the log table to sum the number of views of each article, its author, and the author's unique ID.

	create view vw_articles_alltime_popularity as 
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
        order by    cnt desc


VIEW 2 - Queries the log table to sum the total 404 errors for each day.

	create view vw_errors_by_day_404 as 
	select  date_trunc('day', time) as day
		, count(*) as ErrorCount
	from    log
	where   status like '404%'
	group by	day
	order by	day;


VIEW 3 - Queries the log table to sum the total page view attempts reach day

	create view vw_total_view_attempts_by_day as 
	select  date_trunc('day', time) as day
		, count(*) as TotalViewAttempts
	from    log
	group by	day
	order by	day;
