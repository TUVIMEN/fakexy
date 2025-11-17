#!/usr/bin/env python
# by Dominik Stanisław Suchora <hexderm@gmail.com>
# License: GNU GPLv3

from typing import List, Iterator, Callable
import re

import treerequests
from reliq import RQ

# from curl_cffi import requests
import requests

reliq = RQ(cached="True")


def section(rq: reliq, name: str) -> reliq:
    return rq.filter(
        r"""
        * .box-title; h1 .titleh i@e>'"""
        + name
        + """'; [1] * ancestor@; div .box self@
    """
    )


def section_address(rq: reliq, name: str = " address generator") -> dict:
    return section(rq, name).json(
        r"""
        tr; {
            .street td i@f>"Street"; [0] * ssub@; td c@[0] self@ | "%Di",
            .city td i@f>"City/Town"; [0] * ssub@; td c@[0] self@ | "%Di",
            .region td i@f>"State/Province/Region"; [0] * ssub@; td c@[0] self@ | "%Di",
            .zipcode td i@f>"Zip/Postal Code"; [0] * ssub@; td c@[0] self@ | "%Di",
            .phone td i@f>"Phone Number"; [0] * ssub@; td c@[0] self@ | "%Di",
            .country td i@f>"Country"; [0] * ssub@; td c@[0] self@ | "%Di",
            .latitude td i@f>"Latitude"; [0] * ssub@; td c@[0] self@ | "%Di",
            .longitude td i@f>"Longitude"; [0] * ssub@; td c@[0] self@ | "%Di"
        }
        """
    )


def section_creditcard(rq: reliq, name: str = " Credit Card infomation") -> dict:
    return section(rq, name).json(
        r"""
        tr; {
            .brand td i@f>"Credit card brand"; [0] * ssub@; td c@[0] self@ | "%Di",
            .number td i@f>"Credit card number"; [0] * ssub@; td c@[0] self@ | "%Di",
            .expire td i@f>"Expire"; [0] * ssub@; td c@[0] self@ | "%Di",
            .cvv td i@f>"CVV"; [0] * ssub@; td c@[0] self@ | "%Di"
        }
        """
    )


def section_person(rq: reliq, name: str = " person profile"):
    return section(rq, name).json(
        r"""
        tr; {
            .name td i@f>"Full Name"; [0] * ssub@; td c@[0] self@ | "%Di",
            .gender td i@f>"Gender"; [0] * ssub@; td c@[0] self@ | "%Di",
            .birthday td i@f>"Birthday"; [0] * ssub@; td c@[0] self@ | "%Di",
            .ssn td i@f>"Social Security Number"; [0] * ssub@; td c@[0] self@ | "%Di"
        }
        """
    )


class fakexy:
    def __init__(self, **kwargs):
        settings = {"visited": False}
        settings.update(kwargs)

        self.ses = treerequests.Session(
            requests,
            requests.Session,
            lambda x, y: treerequests.reliq(x, y, obj=reliq),
            **settings,
        )

    @staticmethod
    def _go_through(func: Callable, count: int, maxq: int = 1) -> Iterator:
        while count > 0:
            q = min(count, maxq)
            yield from func()[:q]
            count -= q

    def _animals_url(self, url: str) -> List[dict]:
        rq = self.ses.get_html(url)

        return rq.json(
            r"""
            .r * .container; * .grid child@; div .flex child@; {
                .name [0] div .text-center | "%Dt",
                .image.U [0] img | "%(src)v"
            } |
        """
        )["r"]

    def animals(self, url: str, count: int = 8) -> Iterator[dict]:
        if url is None:
            url = "https://www.fakexy.com/random-animal-generator?quantity=8"
        return self._go_through(lambda: self._animals_url(url), count, maxq=8)

    def _address_url(self, url: str) -> List[dict]:
        rq = self.ses.get_html(url)

        ret = section_address(rq)
        ret["person"] = section_person(rq)
        ret["creditcard"] = section_creditcard(rq)

        return [ret]

    def addresses(self, url: str, count: int = 1) -> Iterator[dict]:
        return self._go_through(lambda: self._address_url(url), count)

    def _name_url(self, url: str) -> List[dict]:
        rq = self.ses.get_html(url)

        ret = section_person(rq, name=" Name generator")
        ret["address"] = section_address(rq)
        ret["creditcard"] = section_creditcard(rq)

        return [ret]

    def names(self, url: str, count: int = 1) -> Iterator[dict]:
        return self._go_through(lambda: self._name_url(url), count)

    def _creditcard_url(self, url: str) -> List[dict]:
        rq = self.ses.get_html(url)

        return [section_creditcard(rq, name="Creditcard generator")]

    def creditcards(self, url: str, count: int = 1) -> Iterator[dict]:
        return self._go_through(lambda: self._creditcard_url(url), count)

    def _phones_url(self, url: str) -> List[dict]:
        rq = self.ses.get_html(url)

        return section(rq, " number generator").json(
            r"""
            .r li; {
                .phone [0] b | "%Di",
                [0] span; {
                    .abbrev @ | "%Di" sed "s/^(//;s/,.*//",
                    .city @ | "%Di" sed "s/)$//;s/^[^,]*, //"
                }
            } |
        """
        )["r"]

    def phones(self, url: str, count: int = 12) -> Iterator[dict]:
        return self._go_through(lambda: self._phones_url(url), count, maxq=12)

    def _zipcodes_url(self, url: str) -> List[dict]:
        rq = self.ses.get_html(url)

        return section(rq, " Zipcode generator").json(
            r"""
            .r li; {
                .zipcode [0] b | "%Di",
                [0] span; {
                    .abbrev @ | "%Di" sed "s/^(//;s/,.*//",
                    .city @ | "%Di" sed "s/)$//;s/^[^,]*, //"
                }
            } |
        """
        )["r"]

    def zipcodes(self, url: str, count: int = 12) -> Iterator[dict]:
        return self._go_through(lambda: self._zipcodes_url(url), count, maxq=12)

    def guess(self, url: str, count: int = 1) -> Iterator[dict]:
        def err():
            raise KeyError("url '{}' doesn't match to anything".format(url))

        r = re.search(r"^https://www\.fakexy\.com(/(.*))", url)
        if r is None:
            err()
        r = r.groups()
        if len(r) == 1:
            return self.addresses(url, count)
        rest = r[1]

        if len(rest) == 0 or re.match(r"([^-]+-)?fake-address-generator-", rest):
            return self.addresses(url, count)
        elif re.match(r"([^-]+-)?fake-name-generator-", rest):
            return self.names(url, count)
        elif re.match(r"fake-creditcard-generator(-[^-]*)?", rest):
            return self.creditcards(url, count)
        elif re.match(r"([^-]+-)?fake-zipcode-generator-", rest):
            return self.zipcodes(url, count)
        elif re.match(r"([^-]+-)?fake-phonenumber-generator-", rest):
            return self.phones(url, count)
        elif re.match(r"random-animal-generator(/|\?quantity=\d+)?", rest):
            return self.animals(url, count)
        else:
            err()
