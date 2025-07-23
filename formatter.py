
from tabulate import tabulate

def format_movies(data):
    headers = ["Title", "Year", "Rating", "Genre"]
    return tabulate(data, headers=headers, tablefmt="grid")

def format_logs(logs):
    return "\n".join([
        f"{log['timestamp']} | {log['search_type']} | {log.get('params')} | results: {log['results_count']}"
        for log in logs
    ])


