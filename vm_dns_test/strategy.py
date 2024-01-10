from typing import Set
from yapapi.strategy import SCORE_REJECTED, SCORE_TRUSTED, MarketStrategy

from script.dns_tester import ResultSummary

class ScanStrategy(MarketStrategy):

    def __init__(self, summary: ResultSummary):
        self.summary = summary
        super().__init__()

    async def score_offer(self, offer):
        node_address = offer.issuer

        modifier = 1.0

        # discourage nodes that we have already scanned
        if node_address in self.summary.node_results:
            modifier = 0.9 ** len(self.summary.node_results[node_address].results)

        return modifier * SCORE_TRUSTED
