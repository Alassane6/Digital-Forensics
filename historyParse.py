#!/usr/bin/env python3

import sys
import os
import sqlite3
from datetime import datetime

def chrome_time_to_datetime(chrome_time):
    """Convert Chrome WebKit timestamp to human-readable datetime."""
    if chrome_time:
        return datetime.utcfromtimestamp(chrome_time / 1000000 - 11644473600)
    return None

def main():
    # Handle missing arguments
    if len(sys.argv) != 2:
        print("Error! - No History File Specified!")
        sys.exit(1)

    db_path = sys.argv[1]

    # Handle file not existing or not being openable
    if not os.path.isfile(db_path):
        print(f"Error! - File Not Found!")
        sys.exit(1)

    print(f"Source File: {db_path}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # -------- DOWNLOADS --------
        cursor.execute("""
            SELECT target_path, total_bytes, (end_time - start_time) AS duration
            FROM downloads
            WHERE total_bytes > 0
        """)
        downloads = cursor.fetchall()
        print(f"Total Downloads: {len(downloads)}")

        if downloads:
            longest = max(downloads, key=lambda x: x[2])
            filename = longest[0].replace("\\", "/").split("/")[-1]
            filesize = longest[1]
            print(f"File Name: {filename}")
            print(f"File Size: {filesize}")
        else:
            print("File Name: N/A")
            print("File Size: 0")

        # -------- SEARCH TERMS --------
        cursor.execute("SELECT term, url_id FROM keyword_search_terms")
        search_terms = cursor.fetchall()
        unique_terms = set(term for term, _ in search_terms)
        print(f"Unique Search Terms: {len(unique_terms)}")

        # Get the most recent search
        cursor.execute("""
            SELECT k.term, v.last_visit_time
            FROM keyword_search_terms k
            JOIN urls v ON k.url_id = v.id
            ORDER BY v.last_visit_time DESC
            LIMIT 1
        """)
        latest = cursor.fetchone()
        if latest:
            recent_term = latest[0]
            recent_time = chrome_time_to_datetime(latest[1])
            formatted_time = recent_time.strftime("%Y-%b-%d %H:%M:%S") if recent_time else "N/A"
            print(f"Most Recent Search: {recent_term}")
            print(f"Most Recent Search Date/Time: {formatted_time}")
        else:
            print("Most Recent Search Term: N/A")
            print("Most Recent Search Date/Time: N/A")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        sys.exit(1)

    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
