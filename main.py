import feedparser
import re
from datetime import datetime

# 配置：RSS 源列表（示例）
RSS_FEEDS = [
    'https://hnrss.org/newest?q=AI',
    'https://www.reddit.com/r/artificial/.rss',
]

# 需要追踪的 AI 术语关键词（可自定义）
KEYWORDS = ['llm', 'agent', 'mcp', 'rag', 'diffusion', 'multimodal']

def extract_terms(text):
    """从文本中提取包含关键词的术语（简化版本，仅示例）"""
    found = set()
    for kw in KEYWORDS:
        matches = re.findall(rf'\b\w*{kw}\w*\b', text, re.IGNORECASE)
        found.update(match.lower() for match in matches if len(match) > 2)
    return found

def main():
    all_terms = set()
    report_lines = [f"AI Term Radar - {datetime.now().strftime('%Y-%m-%d')}", "-" * 40]

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:  # 限制每个源获取条目数
                content = f"{entry.title} {entry.summary if hasattr(entry, 'summary') else ''}"
                terms = extract_terms(content)
                all_terms.update(terms)
                print(f"[*] Scanned: {entry.title[:50]}...")  # 调试输出
        except Exception as e:
            print(f"[!] Failed to parse {feed_url}: {e}")

    # 生成报告
    if all_terms:
        report_lines.append("Detected new terms:")
        for term in sorted(all_terms):
            report_lines.append(f"  - {term}")
    else:
        report_lines.append("No new terms detected.")

    # 输出报告（可重定向到文件）
    print("\n".join(report_lines))

if __name__ == "__main__":
    main()
