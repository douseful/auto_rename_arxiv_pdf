import requests
from bs4 import BeautifulSoup
import re
import argparse
import os

def rename_arxiv_pdf(pdf_path: str, config:dict):
    # 获取 PDF 文件名
    pdf_name = os.path.basename(pdf_path)

    url = f"https://arxiv.org/abs/{pdf_name}"

    response = requests.get(url, headers=config)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    # 去掉最开始的中括号和里面的内容
    title = re.sub(r'^\[[^\]]+\]\s*', '', title)

    # 去掉所有标点符号
    title = re.sub(r'[\[\]\'",.:;!?()]', '', title)

    # 用横杠连接各个单词
    title = re.sub(r'\s+', ' ', title.strip())
    new_name = f"{title}.pdf"

    os.rename(pdf_path, new_name)
    print(f"Renamed {pdf_name} to {new_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    config = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    parser.add_argument("pdf_path", help="The path to the PDF file.")
    # parser.add_argument("save_path", default="./",help="The path to save the renamed PDF file.")
    args = parser.parse_args()

    rename_arxiv_pdf(args.pdf_path, config)