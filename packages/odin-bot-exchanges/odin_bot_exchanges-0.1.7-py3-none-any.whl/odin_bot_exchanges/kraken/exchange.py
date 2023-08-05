@dataclass
class KrakenExchange(ExchangeService):
    exchange: str = "kraken"

    def __init__(self, credentials):
        self.credentials = credentials
        self.client = KrakenClient(credentials=credentials)
        self.wallet_parser: AbstractResponseParser = KrakenWalletResponseParser()
        self.transaction_parser: AbstractResponseParser = (
            KrakenTransactionResponseParser()
        )
        self.ticker_parser: AbstractResponseParser = KrakenTickerResponseParser()
        self.trade_history_parser: AbstractResponseParser = (
            KrakenTradeHistoryResponseParser()
        )

    async def get_transaction_response(
        self, message: EntityMessage, session: aiohttp.ClientSession
    ) -> Transaction:
        try:
            payload = {
                "nonce": str(int(time.time() * 1000)),
                "txid": message.id,
            }

            response = await self.client.request(
                "POST", "/0/private/QueryOrders", session, payload
            )

            transaction = self.transaction_parser.parse_response(
                message=message, response=response
            )
            return transaction
        except Exception as err:
            logging.debug(err)
            raise err

    async def get_wallet_response(self, session: aiohttp.ClientSession) -> List[Wallet]:
        try:
            payload = {
                "nonce": str(int(time.time() * 1000)),
            }

            response = await self.client.request(
                "POST", "/0/private/Balance", session, payload
            )
            balance = self.wallet_parser.parse_response(response=response)
            return balance
        except Exception as err:
            logging.error(err)
            raise err

    async def get_trades_history_response(
        self, start: float, end: float, session: aiohttp.ClientSession
    ) -> List[Transaction]:
        try:

            offset = 0
            transactions = []

            while True:
                logging.info(offset)
                await asyncio.sleep(2)
                payload = {
                    "nonce": str(int(time.time() * 1000)),
                    "trades": True,
                    "start": str(int(start)),
                    "end": str(int(end)),
                    "ofs": offset,
                }
                response = await self.client.request(
                    "POST", "/0/private/TradesHistory", session, payload
                )

                if len(response["error"]) != 0:
                    logging.debug(response)
                    logging.info("Rate Limit Reached- Sleeping")
                    await asyncio.sleep(30)
                else:

                    count = response["result"]["count"]
                    transactions += self.trade_history_parser.parse_response(
                        response=response
                    )
                    if offset <= count:
                        offset += 50
                    else:
                        break

            return transactions
        except Exception as err:
            logging.debug(err)
            raise err

    async def get_order_response(self):
        return await super().get_order_response()

    async def get_ticker_price_response(
        self, message: EntityMessage, session: aiohttp.ClientSession
    ) -> float:
        try:
            payload = {
                "pair": message.market.replace("/", ""),
            }

            response = await self.client.get_public(
                "/0/public/Ticker", session, payload
            )
            ticker = self.ticker_parser.parse_response(
                response=response, message=message
            )
            return ticker
        except Exception as err:
            logging.error(err)
            raise err


@
