#!/usr/bin/env python
import requests
import logging
from requests import Response
from configs import username, password, mirrors
from countries import get_domain, choose_port

# logging to file
logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    filemode="a",
    format="%(asctime)s %(message)s",
)


def set_connection(country, url) -> Response:
    proxy = (
        f"http://{username}:{password}@{country}.smartproxy.com:{choose_port(country)}"
    )
    response = requests.get(url, proxies={"http": proxy, "https": proxy})
    return response


# vars for the get_mirror()
country_count = 0
mirror_pointer = 0


def get_mirror() -> str:
    global country_count, mirror_pointer
    if mirror_pointer == 13:
        return "stop"
    if country_count <= 72:
        country_count += 1
        return mirrors[mirror_pointer]
    else:
        logging.info("moving to the next mirror")
        mirror_pointer += 1
        country_count = 0
        try:
            return mirrors[mirror_pointer]
        except IndexError:
            return "stop"


def life_cycle() -> str:
    while True:
        mirror = get_mirror()
        country_prefix = get_domain()
        logging.info(f"connecting {mirror} from {country_prefix.upper()}")
        print(mirror, country_prefix)
        if mirror == "stop":
            logging.info("all mirrors checked: stop")
            return "all mirrors checked stop"
        try:
            answer = set_connection(country_prefix, mirror)
            check_response(answer, country_prefix, mirror)
        except Exception as e:
            logging.info(f"all mirrors checked {e}")
            return "all mirrors checked"
        except BaseException:
            logging.info("interrupted")
            return "interrupted"


def check_response(response, country_prefix, mirror):
    # expected good response
    if 0 < len(response.history) <= 1 and 300 > response.status_code >= 200:
        return logging.info(
            f"country: {country_prefix}, target: {mirror}, mirror reached"
        )
    # redirect used
    if len(response.history) > 1 and 400 > response.status_code >= 300:
        return logging.info(
            f"country: {country_prefix}, target: {mirror}, redirected to: {response.url}"
        )
    # client down
    if 500 > response.status_code >= 400:
        return logging.info(
            f"country: {country_prefix}, target: {mirror}, client error {response.status_code}"
        )
    # server down
    if response.status_code >= 500:
        return logging.info(
            f"country: {country_prefix}, target: {mirror}, server is down: {response.status_code}"
        )
    if response.history == 0:
        return logging.info(
            f"country: {country_prefix}, target: {mirror}, mirror reached http"
        )
    else:
        return logging.error(
            f"unknown error {response.history}=={len(response.history)}, {response.status_code}"
        )


if __name__ == "__main__":
    print(life_cycle())
