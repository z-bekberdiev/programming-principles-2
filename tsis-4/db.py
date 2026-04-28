import psycopg2
from datetime import datetime
from typing import List, Tuple
from config import DB_CONFIG


def get_connection():
    """Create and return a new database connection"""
    return psycopg2.connect(**DB_CONFIG)


def ensure_table():
    """Create the leaderboard table if it doesn't exist"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    score INT NOT NULL,
                    level INT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            """)
        conn.commit()


def save_score(username: str, score: int, level: int):
    """Insert a new score for a user"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO leaderboard (username, score, level, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (username, score, level, datetime.now()))
        conn.commit()


def top_scores(limit: int = 10) -> List[Tuple[str, int, int, datetime]]:
    """Return the top scores up to the specified limit"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT username, score, level, timestamp
                FROM leaderboard
                ORDER BY score DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()


def personal_best(username: str) -> int:
    """Return the highest score for a given username"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(score)
                FROM leaderboard
                WHERE username = %s
            """, (username,))
            result = cur.fetchone()[0]
            return result or 0