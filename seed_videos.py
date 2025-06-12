import sqlite3

# Connect to the SQLite DB
conn = sqlite3.connect("streaming.db")
cur = conn.cursor()

# Sample videos
videos = [
    ("Love Story", "romance", "love_story.mp4"),
    ("Standup Comedy", "comedy", "comedy_show.mp4"),
    ("Jump scenes", "thriller", "jump_scenes.mp4"),
]

# Insert into videos table
for title, category, filename in videos:
    cur.execute("INSERT INTO videos (title, category, filename) VALUES (?, ?, ?)",
                (title, category, filename))

conn.commit()
conn.close()

print("Sample videos inserted successfully!")
