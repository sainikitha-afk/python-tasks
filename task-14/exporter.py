import json
from xml.etree.ElementTree import Element, SubElement, ElementTree


def save_graph(graph, filename="output/crawl_graph.json"):
    with open(filename, "w") as f:
        json.dump(graph, f, indent=2)


def save_sitemap(urls, filename="output/sitemap.xml"):
    urlset = Element("urlset")

    for url in urls:
        url_el = SubElement(urlset, "url")
        loc = SubElement(url_el, "loc")
        loc.text = url

    tree = ElementTree(urlset)
    tree.write(filename)