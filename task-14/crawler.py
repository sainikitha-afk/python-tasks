import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from collections import defaultdict
import argparse

from utils import normalize_url, get_domain, get_robot_parser
from exporter import save_graph, save_sitemap


visited = set()
graph = defaultdict(list)
inbound_count = defaultdict(int)


async def fetch(session, url):
    try:
        start = time.time()
        async with session.get(url, timeout=10) as response:
            duration = round(time.time() - start, 2)
            status = response.status

            text = await response.text()

            return url, status, text, duration

    except:
        return url, "ERROR", "", 0


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a in soup.find_all("a", href=True):
        link = normalize_url(base_url, a["href"])
        links.add(link)

    return links


async def crawl(seed, max_depth, concurrency):
    print("\n=== Crawl Started ===")
    print(f"[INFO] Seed: {seed}")
    print(f"[INFO] Max depth: {max_depth} | Concurrency: {concurrency}")

    domain = get_domain(seed)
    rp = get_robot_parser(seed)

    queue = [(seed, 0)]
    visited.add(seed)

    async with aiohttp.ClientSession() as session:

        for depth in range(max_depth + 1):
            tasks = []

            current_level = [url for url, d in queue if d == depth]

            for url in current_level:
                tasks.append(fetch(session, url))

            results = await asyncio.gather(*tasks)

            for url, status, html, duration in results:

                print(f"[DEPTH {depth}] {url:<50} {status} {duration}s")

                if status != 200:
                    continue

                links = extract_links(html, url)

                for link in links:
                    if get_domain(link) != domain:
                        continue

                    if not rp.can_fetch("*", link):
                        continue

                    graph[url].append(link)
                    inbound_count[link] += 1

                    if link not in visited:
                        visited.add(link)
                        queue.append((link, depth + 1))


def report():
    print("\n=== Crawl Complete ===")
    print(f"Pages crawled: {len(graph)}")
    print(f"Unique URLs: {len(visited)}")

    broken = [u for u in visited if inbound_count[u] > 0 and u not in graph]
    orphans = [u for u in visited if inbound_count[u] == 0]

    print("\n=== SEO Audit Report ===")

    print("\nOrphan Pages:")
    for o in orphans[:5]:
        print(f"  - {o}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--concurrency", type=int, default=10)

    args = parser.parse_args()

    start = time.time()

    asyncio.run(crawl(args.seed, args.depth, args.concurrency))

    report()

    save_graph(graph)
    save_sitemap(visited)

    print("\nSaved:")
    print(" - output/crawl_graph.json")
    print(" - output/sitemap.xml")

    print(f"\nTime taken: {round(time.time()-start,2)}s")


if __name__ == "__main__":
    main()