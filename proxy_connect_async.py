# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from configs import mirrors, username, password
from countries import choose_port, abbreviatures
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    filemode="a",
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def fetch(proxy, session, url):
    """
    set up proxy here
    :param proxy:
    :param session:
    :param url:
    :return:
    """
    # there are errors verifying ssl sometimes, so it's disabled
    async with session.get(url, proxy=proxy, ssl=False) as response:
        def check_response():
            """
            checks response for redirects and restrictions
            :return:
            """
            http_url = str(response.url).replace("https", "http")[:-1]
            country_id = str(proxy).find("@")
            country = str(proxy)[country_id+1:country_id+3]
            if http_url == url:
                print(f"reached: {url}", end=", ")
                logging.info(f"reached: {url}, {country}")
            else:
                print(f"redirect to: {response.url} from {url}", end=", ")
                logging.info(f"redirect to: {response.url} from {url}, {country}")

            print(country)

        # html = BeautifulSoup(await response.text(), "html.parser")

        return check_response()


async def fetch_all(proxies, loop):
    # total = []
    for proxy in proxies:
        async with aiohttp.ClientSession(trust_env=True, loop=loop) as session:
            results = await asyncio.gather(
                *[fetch(proxy, session, url) for url in mirrors], return_exceptions=True
            )
            # total.append(results)

    return  # total


def prepare_proxies_for_countries() -> list:
    proxies = []
    for i in abbreviatures:
        proxy = f"http://{username}:{password}@{i}.smartproxy.com:{choose_port(i)}"
        proxies.append(proxy)
    return proxies


if __name__ == "__main__":
    proxies = prepare_proxies_for_countries()
    loop = asyncio.get_event_loop()
    start_time = time.time()
    htmls = loop.run_until_complete(fetch_all(proxies, loop))
    # print(htmls[0][0].find_all("title"))
    # for i in htmls[0]:
    #     try:
    #         if "access" in str(i.find_all("title")).lower():
    #             print("fine")
    #             pass
    #         else:
    #             print(f"bad")
    #             print(i.find_all("title"))
    #     except Exception as e:
    #         print(f"error: {i}")
    # htmls[0][0] == bs4.BeautifulSoup
    print(f"took {time.time()-start_time / 60} minutes")
