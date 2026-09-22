# from config.settings import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
# def test_postgres_connection():
#     import psycopg2
#     from datetime import datetime,timezone
#     conn = psycopg2.connect(
#         host=POSTGRES_HOST,
#         port=POSTGRES_PORT,
#         user=POSTGRES_USER,
#         password=POSTGRES_PASSWORD,
#         database=POSTGRES_DB
#     )
#     cursor = conn.cursor()
  
#     insert = """INSERT INTO raw_articles (url , url_hash, title,source, content, crawled_at)
#     VALUES (%s,%s,%s,%s,%s,%s) 
#     RETURNING id
#     """
#     time = datetime.now(timezone.utc)
#     values = ("https://example.com/1", "hash1234367777", "Test Title", "Test Source", "Test Content", time)
#     cursor.execute(insert, values)
#     conn.commit()
#     inserted_id = cursor.fetchone()[0]
#     cursor.execute("SELECT " \
#     " url, url_hash, title, source, content, crawled_at FROM raw_articles WHERE id = %s", (inserted_id,))
#     raw = cursor.fetchone()
#     assert raw is not None, "Inserted row should not be None"
#     assert raw[5] == time, "Crawled at does not match"
#     assert raw[0] == "https://example.com/1", "URL does not match"
#     cursor.close()
#     conn.close()
