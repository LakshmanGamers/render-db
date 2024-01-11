import psycopg2

conn = psycopg2.connect(
    database="my_demo_db_98nb",
    user="my_demo_db_98nb_user",
    host="dpg-cmg068mn7f5s73cair20-a.ohio-postgres.render.com",
    password="WQAFv6317Di1rgb8WQoyO7QRyrpLITr6",
    port=5432
)

try:
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Retrieve data from "user" table
    cur.execute("SELECT username FROM \"user\"")
    rows = cur.fetchall()

    # Print the usernames
    print("Usernames:")
    for row in rows:
        print(row[0])

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close cursor and communication with the database
    cur.close()
    conn.close()
