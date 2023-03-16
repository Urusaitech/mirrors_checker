# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
import asyncio
import datetime
import aiohttp
import time

from bs4 import BeautifulSoup
from configs import mirrors, username, password, timeout, pattern
from countries import choose_port, abbreviatures
from logs_checker import Checks
from prepare_logs import update_today_logs
from logger_setup import setup_logger


def get_date() -> str:
    return str(datetime.datetime.now())[:10]


async_logger = setup_logger("proxy_async", f"{get_date()}_raw.log", mode="w")


async def fetch(proxy, session, url):
    """
    set up proxy here
    :param proxy:
    :param session:
    :param url:
    :return:
    """
    # print(f"proxy: {proxy}, session: {session}, url: {url}")
    # there are errors verifying ssl sometimes, so it's disabled
    async with session.get(url, proxy=proxy, ssl=False, timeout=timeout) as response:
        html = BeautifulSoup(await response.text(), "html.parser")
        if response.status == 407:
            print("No more traffic on balance")
            async_logger.info("No more traffic on balance")
            return

        # <-------check_response()------->
        def check_response():
            """
            checks response for redirects and restrictions
            :return:
            """
            http_url = str(response.url).replace("https", "http")

            country_id = str(proxy).find("@")
            country = str(proxy)[country_id + 1:country_id + 3]
            title = str(html.findAll("title")).lower()
            print(f" title: {title}, url: {response.url}")
            # if url reached
            if http_url == url or http_url[:-1] == url:
                # if your pattern in tag <title>
                if pattern in title:
                    print(f"reached: {url}, {country}")
                    async_logger.info(f"reached: {url}, {country}")
                # if url reached and it blocks access
                elif title == "[]":
                    print(f"Url plug or unreached: {url}, {country}")
                    async_logger.info(f"Url plug / unreached on: {url}, {country}")
                else:
                    print(f"url plug on: {url}, {country}")
                    async_logger.info(f"url plug on: {url}, {country}")

            # if target url wasn't reached
            else:

                if pattern in title:
                    print(f"redirect to: {response.url} from {url}, {country}")
                    async_logger.info(f"redirect to: {response.url} from {url}, {country}")
                elif pattern not in title and http_url in mirrors:
                    if title == "[]":
                        print(f"url plug or unreached: {url}, {country}")
                        async_logger.info(f"url plug on: {url}, {country}")
                    else:
                        print(f"url plug on: {url}, {country}")
                        async_logger.info(f"url plug on: {url}, {country}")
                else:
                    print(f"blocked by: {response.url} from {url}, {country}")
                    async_logger.info(f"blocked by: {response.url} from {url}, {country}")

        # <-------check_response()------->

        return check_response()


async def fetch_all(proxies, loop, target_mirrors) -> None:
    """
    Runs fetch()
    TODO: run all urls at once with workers
    :param target_mirrors:
    :param proxies: list of proxy addresses
    :param loop: asyncio loop
    :return:
    """
    # total = []
    print(f"fetching: {len(proxies)}, {len(target_mirrors)}")
    flag = 0
    for proxy in proxies:
        async with aiohttp.ClientSession(trust_env=True, loop=loop) as session:
            # FIXME: return_exceptions seem to cause skipping some countries, not sure
            await asyncio.gather(
                *[fetch(proxy, session, url) for url in target_mirrors], return_exceptions=True
            )
            print("next country")
            flag += 1
        # uncomment the return to check only the first mirror
        # return
        # total.append(results)
    print(f"check ended with flag: {flag}/{len(target_mirrors)}")
    return  # total


def prepare_proxies_for_countries(abbs) -> list:
    """
    Prepares a list of proxies for all countries with a required port
    :return:
    """
    async_logger.debug("preparing mirrors")
    proxies = []
    for i in abbs:
        proxy = f"http://{username}:{password}@{i}.smartproxy.com:{choose_port(i)}"
        proxies.append(proxy)
    return proxies


def prepare_and_start(countries, target_mirrors) -> None:
    proxies = prepare_proxies_for_countries(countries)
    loop = asyncio.get_event_loop()  # start new loop instead?

    async_logger.debug("Async loop created")
    loop.run_until_complete(fetch_all(proxies, loop, target_mirrors))  # check all the mirrors


def main():
    async_logger.info("Starting")
    start_time = time.time()
    prepare_and_start(abbreviatures, mirrors)
    Checks().check_missed()  # Should be deprecated
    to_check = Checks().check_again()
    # if to_check:
    #     print("Double checking missed mirrors")
    #     prepare_and_start(to_check.keys(), to_check.values())
    print(f"took {'{:.2f}'.format((time.time() - start_time) / 60)} minutes")
    async_logger.info(f"Check ended, took {'{:.2f}'.format((time.time() - start_time) / 60)} minutes")
    update_today_logs()
    Checks().check_logs()


if __name__ == "__main__":
    main()
