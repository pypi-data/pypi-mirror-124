import aiohttp
import logging
from typing import List


from odin_bot_entities.trades import Order, Transaction
from odin_bot_entities.balances import Wallet

from odin_bot_exchanges.binance.client import BinanceClient
from odin_bot_exchanges.binance.responses import BinanceWalletResponseParser, BinanceTransactionResponseParser
from odin_bot_exchanges.exchange import ExchangeService


class BinanceExchange(ExchangeService):
    exchange: str = "binance"

    def __init__(self, api_key: str, secret_key: str):
        self.client = BinanceClient(api_key=api_key, secret_key=secret_key)
        self.wallet_parser = BinanceWalletResponseParser()
        self.transaction_parser = BinanceTransactionResponseParser()

    async def get_order_response(self, order_id: str, market_code: str) -> Order:
        response = self.client.get_order_response(
            order_id=order_id, market_code=market_code)
        order: Order = self.order_parser.parse_response(response=response)
        return order

    async def get_transaction_response(self, order_id: str, market_code: str) -> Order:
        response = self.client.get_transaction_response(
            order_id=order_id, market_code=market_code)
        transaction: Transaction = self.order_parser.parse_response(
            response=response)
        return transaction

    async def get_wallet_response(self) -> List[Wallet]:
        response = self.client.get_wallet_response()
        wallets = self.wallet_parser.parse_response(response=response)
        return wallets
