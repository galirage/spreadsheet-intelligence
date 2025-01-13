import logging

# ログの設定
logging.basicConfig(filename='results.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_results(result):
    logging.info(f"Result: {result}")

# 既存のコード...

