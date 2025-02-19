import os
import json
from datetime import datetime
from finlight_client import FinlightApi

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")

def main():
    config = {
        "api_key": "sk_2d9f507089034e1967299e751cea62d95bdf7cb4e87d5eb8d57fadc91837a358"   }
    client = FinlightApi(config)

    params = {
        "query": os.environ['QUERY'],
        "language": os.environ['LANGUAGE']
    }

    articles = client.articles.get_extended_articles(params)

    # Define articles save path
    articles_dir = os.path.join(".", "artifacts")
    os.makedirs(articles_dir, exist_ok=True)
    output_file = os.path.join(articles_dir, f"{params['query']}_{params['language']}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4, default=json_serial)
    print(f"Articles saved to {output_file}")

    logs_dir = os.path.join(".", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    day = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(logs_dir, f"{day}_log.txt")

    with open(log_file, "w", encoding="utf-8") as log_f:
        log_f.write(f"Articles saved to {output_file} at {datetime.now().isoformat()}\n")
        log_f.write(f"Query: {params['query']}, Language: {params['language']}\n")

    print(f"Logs saved to {log_file}")

if __name__ == "__main__":
    main()



