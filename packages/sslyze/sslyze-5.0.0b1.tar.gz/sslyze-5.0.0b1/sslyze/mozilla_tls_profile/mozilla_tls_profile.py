import json
from pathlib import Path
from typing import List, Optional

import pydantic

from sslyze import ServerScanResult


class _MozillaTlsConfigurationAsJson(pydantic.BaseModel):
    certificate_curves: List[str]
    certificate_signatures: List[str]
    certificate_types: List[str]
    ciphersuites: List[str]
    dh_param_size: Optional[int]
    ecdh_param_size: int
    hsts_min_age: int
    maximum_certificate_lifespan: int
    ocsp_staple: bool
    recommended_certificate_lifespan: int
    rsa_key_size: Optional[int]
    server_preferred_order: bool
    tls_curves: List[str]
    tls_versions: List[str]


class _AllMozillaTlsConfigurationsAsJson(pydantic.BaseModel):
    modern: _MozillaTlsConfigurationAsJson
    intermediate: _MozillaTlsConfigurationAsJson
    old: _MozillaTlsConfigurationAsJson


class _MozillaTlsProfileAsJson(pydantic.BaseModel):
    version: str
    href: str
    configurations: _AllMozillaTlsConfigurationsAsJson


class ServerTlsConfigurationNotCompliant(Exception):
    def __init__(self, server_scan_result: ServerScanResult):
        pass


# TODO: Better name
class MozillaTlsProfileChecker:
    def __init__(self, mozilla_tls_profile: _MozillaTlsProfileAsJson):
        self._mozilla_tls_profile = mozilla_tls_profile

    @classmethod
    def get_default(cls) -> "MozillaTlsProfileChecker":
        json_profile_path = Path(__file__).parent.absolute() / "5.6.json"
        json_profile_as_str = json_profile_path.read_text()
        parsed_profile = _MozillaTlsProfileAsJson(**json.loads(json_profile_as_str))
        return cls(parsed_profile)

    def check_result(self, result: ServerScanResult) -> None:
        pass


# OpenSslCipherSuites commands
# Elliptic curves commands
# Certinfo
# HTTP headers
# Plus all vulns: ROBOT, CCS, RENEG, COMPRESSION, SCSV
