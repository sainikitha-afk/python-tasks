# Task 14: Concurrent Web Crawler with Depth Control

## Objective

Build an asynchronous web crawler that explores a website starting from a seed URL, traverses links up to a specified depth, and generates SEO insights along with crawl data exports.

---

## Features

- Async crawling using aiohttp and asyncio  
- Breadth-first traversal (level-by-level crawling)  
- Configurable depth and concurrency  
- robots.txt compliance  
- URL deduplication using sets  
- Link graph generation  
- Sitemap XML export  
- SEO audit insights (orphans, broken links)  

---

## Project Structure

task-14/
│
├── crawler.py  
├── utils.py  
├── exporter.py  
├── requirements.txt  
├── output/  

---

## Installation

pip install -r requirements.txt

---

## Usage

python crawler.py --seed https://example.com --depth 3 --concurrency 20

---

## Output

### Crawl Logs

[DEPTH 0] https://example.com        200 OK  
[DEPTH 1] https://example.com/about 200 OK  

---

### Summary

Pages crawled: 147  
Unique URLs: 203  

---

### SEO Report

Orphan Pages:
- /test-page  
- /old-blog  

---

### Output Files

- output/crawl_graph.json  
- output/sitemap.xml  

---

## Concepts Used

- Async programming (asyncio, aiohttp)  
- BFS traversal  
- robots.txt parsing  
- HTML parsing (BeautifulSoup)  
- Graph representation  
- SEO analysis basics  

---

## Conclusion

This crawler demonstrates how large-scale web traversal systems work, including concurrency handling, deduplication, and structured data extraction for SEO insights.