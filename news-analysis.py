#!/usr/bin/env Python
import psycopg2


def get_top_three_articles():
    """Return the most popular three articles of all time."""
    # Set the database name the "news" database.
    db = psycopg2.connect("dbname=news")
    # Set the query - Select the top three most viewed articles in the logs.
    query = """
        select  *
        from    vw_articles_alltime_popularity
        limit   3
    """
    # Create the cursor.
    c = db.cursor()
    # Execute the query.
    c.execute(query)
    # Fetch all of the articles found by the query.
    articles = c.fetchall()
    # Loop through the articles dict and print the titles and view counts.
    for article in articles:
        title = article[0]
        view_count = str(article[1])
        print("\"{}\" -- {} views".format(title.title(), view_count))
    # Close the database connection.
    db.close()


def get_top_authors():
    """Return the most popular article authors of all time."""
    # Set the database name to the "news" database.
    db = psycopg2.connect("dbname=news")
    # Set the query - Select the authors and sort them by overall popularity.
    query = """
        select  au.id
                , au.name
                , sum(aap.cnt) as total_views
        from    authors as au
                left join vw_articles_alltime_popularity as aap
                    on aap.id = au.id
        group by    au.id, au.name
        order by    total_views desc
    """
    # Create the cursor.
    c = db.cursor()
    # Execute the query.
    c.execute(query)
    # Fetch all of the authors and view counts found by the query.
    authors = c.fetchall()
    # Loop through the authors dict and print the author names and view counts.
    for author in authors:
        name = author[1]
        view_count = str(author[2])
        print("{} -- {} views".format(name.title(), view_count))
    # Close the database connection.
    db.close()


def get_error_percentages():
    """Return dates more than 1% of requests lead to errors."""
    # Set the database name the "news" database.
    db = psycopg2.connect("dbname=news")
    # Set the query - Aggregate daily view error rates and display those > 1%.
    query = """
        select  TO_CHAR(a.day, 'FMMonth FMd, FMYYYY') as day
                , ROUND(100 * (
                        cast(e.ErrorCount as numeric(10,4))
                        / cast(TotalViewAttempts as numeric(10,4))
                    ),1) as ErrorPercentage
        from    vw_total_view_attempts_by_day as a
                inner join vw_errors_by_day_404 as e
                    on e.day = a.day
        where   (100 * (
                    cast(e.ErrorCount as numeric(10,4))
                    / cast(TotalViewAttempts as numeric(10,4))
                )) > 1.0
    """
    # Create the cursor.
    c = db.cursor()
    # Execute the query.
    c.execute(query)
    # Fetch all of the dated total view and error counts found by the query.
    dates = c.fetchall()
    # Loop through the dates dictionary and print dates and their error rates.
    for date in dates:
        day = date[0]
        error_percentage = str(date[1])
        print("{} -- {}%".format(day, str(error_percentage)))
    # Close the database connection.
    db.close()


print("Most popular articles of all time:".upper())
get_top_three_articles()

print("\nMost popular article authors of all time:".upper())
get_top_authors()

print("\nDay(s) with error percentage greater than 1%:".upper())
get_error_percentages()
