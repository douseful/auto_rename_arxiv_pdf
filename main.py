import requests
from bs4 import BeautifulSoup
import re
import argparse
import os

def rename_arxiv_pdf(pdf_path: str):
    # 获取 PDF 文件名
    pdf_name = os.path.basename(pdf_path)

    url = f"https://arxiv.org/abs/{pdf_name}"

    response = requests.get(url)
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
    parser.add_argument("pdf_path", help="The path to the PDF file.")
    args = parser.parse_args()

    rename_arxiv_pdf(args.pdf_path)