import pandas as pd
import sqlite3

# 1. Read the CSV file you downloaded
df = pd.read_csv('Bookstore.csv')

# 2. Clean up column names (removes spaces to make SQL queries easier for the AI)
df.columns = df.columns.str.replace(' ', '_')

# 3. Connect to a new local SQLite database file
conn = sqlite3.connect('bookstore.db')

# 4. Save the data to a table named 'books'
df.to_sql('books', conn, if_exists='replace', index=False)
conn.close()

print("Successfully converted Bookstore.csv to bookstore.db!")