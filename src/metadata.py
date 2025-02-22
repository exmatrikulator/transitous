# SPDX-FileCopyrightText: 2023 Jonah Brüchert <jbb@kaidan.im>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import List, Optional


class Maintainer:
    name: str
    email: str

    def __init__(self, parsed: dict):
        self.name = parsed["name"]
        self.email = parsed["email"]


class License:
    spdx_identifier: Optional[str] = None
    url: Optional[str] = None


class Source:
    name: str
    fix: bool = False
    license: License

    def __init__(self, parsed: dict = None):
        self.license = License()
        if parsed:
            if "license" in parsed:
                if "spdx-identifier" in parsed["license"]:
                    self.license.spdx_identifier = parsed["license"]["spdx-identifier"]
                if "url" in parsed["license"]:
                    self.license.url = parsed["license"]["url"]

            self.name = parsed["name"]
            if "fix" in parsed:
                self.fix = bool(parsed["fix"])


class TransitlandSource(Source):
    transitland_atlas_id: str

    def __init__(self, parsed: dict):
        super().__init__(parsed)
        self.transitland_atlas_id = parsed["transitland-atlas-id"]


class HttpSource(Source):
    url: str

    def __init__(self, parsed: dict = None):
        if parsed:
            super().__init__(parsed)
            self.url = parsed["url"]


def sourceFromJson(parsed: dict) -> Source:
    match parsed["type"]:
        case "transitland-atlas":
            return TransitlandSource(parsed)
        case "http":
            return HttpSource(parsed)

    return None


class Region:
    maintainers: List[Maintainer]
    sources: Source

    def __init__(self, parsed: dict):
        self.maintainers = map(Maintainer, parsed["maintainers"])
        self.sources = map(sourceFromJson, parsed["sources"])
