from typing import Iterable

import logging
import requests
from asn1crypto import crl, x509, pem

from ... import errors
from .util import RequestsFetcherMixin
from ..api import CRLFetcher
from ..common_utils import crl_job_results_as_completed


logger = logging.getLogger(__name__)


class RequestsCRLFetcher(CRLFetcher, RequestsFetcherMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._by_cert = {}

    async def fetch(self, cert: x509.Certificate, *, use_deltas=True):
        try:
            return self._by_cert[cert.issuer_serial]
        except KeyError:
            pass

        results = []
        async for fetched_crl in self._fetch(cert, use_deltas=use_deltas):
            results.append(fetched_crl)
        self._by_cert[cert.issuer_serial] = results
        return results

    async def _fetch_single(self, url):
        async def task():
            logger.info(f"Requesting CRL from {url}...")
            try:
                response = await self._get(
                    url, acceptable_content_types=('application/pkix-crl',)
                )
                data = response.content
                if pem.detect(data):
                    _, _, data = pem.unarmor(data)
                return crl.CertificateList.load(data)
            except (ValueError, requests.RequestException) as e:
                raise errors.CRLFetchError(
                    f"Failure to fetch CRL from URL {url}"
                ) from e
        return await self._perform_fetch(url, task)

    async def _fetch(self, cert: x509.Certificate, *, use_deltas):

        # FIXME: Same as corresponding aiohttp FIXME note
        sources = cert.crl_distribution_points
        if use_deltas:
            sources.extend(cert.delta_crl_distribution_points)

        if not sources:
            return

        def _fetch_jobs():
            for distribution_point in sources:
                url = distribution_point.url
                # Only fetch CRLs over http
                #  (or https, but that doesn't really happen all that often)
                # In particular, don't attempt to grab CRLs over LDAP
                if url.startswith('http'):
                    yield self._fetch_single(url)

        async for result in crl_job_results_as_completed(_fetch_jobs()):
            yield result

    def fetched_crls(self) -> Iterable[crl.CertificateList]:
        return {crl_ for crl_ in self.get_results()}

    def fetched_crls_for_cert(self, cert) -> Iterable[crl.CertificateList]:
        return self._by_cert[cert.issuer_serial]
