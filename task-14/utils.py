import urllib.parse
import urllib.robotparser


def normalize_url(base, link):
    return urllib.parse.urljoin(base, link).split("#")[0]


def get_domain(url):
    return urllib.parse.urlparse(url).netloc


def get_robot_parser(seed_url):
    parsed = urllib.parse.urlparse(seed_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
    except:
        pass

    return rp