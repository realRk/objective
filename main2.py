import psycopg2

query_1 = (
    "select authors.name ,count(log.path) as num from authors,log,"
    "articles where log.path like concat('%',articles.slug,'%') and "
    "log.status like ('%OK%') and authors.id = articles.author  group by"
    " authors.name order by num desc")


query_2 = (
    "select articles.title, count(log.path) as num from articles,"
    "authors,log where log.status like('%OK%') and log.path like "
    "concat('%',articles.slug,'%') and articles.author = authors.id"
    " group by articles.title order by num desc limit 3")


query_3 = (
    "select day, perc from ("
    "select day, round((sum(requests)/("
    "select count(*) from log where substring(cast(log.time as text), 0, 11) "
    "= day) * 100),2) as perc from ("
    "select substring(cast(log.time as text), 0, 11) as day, count(*) as "
    "requests from log where status like '%NOT%' group by day)as"
    " log_percentage group by day order by perc desc) as final_query "
    "where perc >= 1")


def connect(db_nm="news"):
    db = psycopg2.connect("dbname={}".format(db_nm))
    """format field is replaced by using the objects passed into the .format(
    ) function"""
    cursor = db.cursor()
    return db, cursor


def get_results(query):
    db, cursor = connect()
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def print_results(rslt):
    for row in rslt:
        print("{}. {} - {}".format(rslt.index(row)+1, row[0], row[1]))


if __name__ == "__main__":
    print("What are the most popular three articles of all time?")
    print_results(get_results(query_2))
    print("")
    print("Who are the most popular article authors of all time?")
    print_results(get_results(query_1))
    print("")
    print("On which days did more than 1% of requests lead to errors?")
    print_results(get_results(query_3))
