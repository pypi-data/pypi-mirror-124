class KrakenTransactionResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict, message: EntityMessage) -> Transaction:
        if len(response["error"]) != 0:
            logging.error(response["error"])
            raise ResponseError("Kraken Parser: Response had errors")
        if response["result"] == {}:
            raise ResponseError("Kraken Parser: Response had no data")
        try:
            currency_name, pair_currency_name = message.market.split("/")
            currency_name = currencies.KRAKEN_RENAME_COINS[currency_name]
            pair_currency_name = currencies.KRAKEN_RENAME_COINS[pair_currency_name]
            transaction = Transaction.parse_obj(
                {
                    "id": message.id,
                    "currency_name": currency_name,
                    "pair_currency_name": pair_currency_name,
                    "market": f"{currency_name}/{pair_currency_name}",
                    "time": response["result"][message.id]["closetm"],
                    "exchange": "kraken",
                    "type": response["result"][message.id]["descr"]["type"],
                    "fee": response["result"][message.id]["fee"],
                    "currency_value": response["result"][message.id]["vol"],
                    "pair_currency_value": float(response["result"][message.id]["vol"])
                    * (
                        float(response["result"][message.id]["price"])
                        * (1 + currencies.KRAKEN_FEE)
                    ),
                }
            )

            return transaction
        except Exception as err:
            logging.error(err)
            raise ParserError("Kraken Parser: Could not parse Transaction.")


class KrakenTradeHistoryResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict):
        if len(response["error"]) != 0:
            logging.error(response["error"])
            raise ResponseError("Kraken Parser: Response had errors")
        try:
            transaction_data = []
            for _, tx in response["result"]["trades"].items():
                market = currencies.KRAKEN_RENAME_PAIRS[tx["pair"]]
                currency_name, pair_currency_name = market.split("/")
                data = {
                    "id": tx["ordertxid"],
                    "time": tx["time"],
                    "exchange": "kraken",
                    "type": tx["type"],
                    "market": market,
                    "fee": float(tx["fee"]),
                    "currency_name": currency_name,
                    "pair_currency_name": pair_currency_name,
                    "currency_value": float(tx["vol"]),
                    "pair_currency_value": float(tx["vol"])
                    * (float(tx["price"]) * (1 + currencies.KRAKEN_FEE)),
                }
                transaction_data.append(data)
            transactions = pydantic.parse_obj_as(
                List[Transaction], transaction_data)
            return transactions

        except Exception as err:
            logging.debug(err)
            raise ParserError("Kraken Parser: Could not parse Trade History")


class KrakenWalletResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict) -> List[Wallet]:
        if len(response["error"]) != 0:
            logging.error(response["error"])
            raise ResponseError("Kraken Parser: Response had errors")
        try:
            wallet_data = {
                "exchange": "kraken",
                "coins": {
                    currencies.KRAKEN_RENAME_COINS[key]: {
                        "name": currencies.KRAKEN_RENAME_COINS[key],
                        "amount": round(
                            float(value),
                            currencies.CEROS[currencies.KRAKEN_RENAME_COINS[key]],
                        ),
                    }
                    for key, value in response["result"].items()
                    if currencies.KRAKEN_RENAME_COINS[key] in currencies.BALANCE_COINS
                },
                "sign": 1,
                "time": time.time(),
                "date": datetime.now(),
            }

            wallet = [Wallet.parse_obj(wallet_data)]
            return wallet
        except Exception as err:
            logging.debug(err)
            raise ParserError("Kraken Parser: Could not parse Balance")


class KrakenTickerResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict, message: EntityMessage) -> float:
        if len(response["error"]) != 0:
            logging.error(response["error"])
            raise ResponseError("Kraken Parser: Response had errors.")
        try:
            market = message.market.replace("/", "")
            bid_price = float(response["result"][market]["b"][0])
            return bid_price
        except Exception as err:
            logging.debug(err)
            raise ParserError("Kraken Parser: Could not parse bid price.")


class OrionXOrderResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict, message: EntityMessage) -> Order:
        if response["data"]["order"] == None:
            raise ResponseError("OrionX Parser: No Order data received.")
        if "errors" in response:
            logging.error(response["errors"])
            raise ResponseError("OrionX Parser: Found errors in response")

        try:
            transaction_data = [
                {
                    "id": data["id"],
                    "currency_name": data["currency"]["code"],
                    "pair_currency_name": data["pairCurrency"]["code"],
                    "market": f"{data['currency']['code']}/{data['pairCurrency']['code']}",
                    "exchange": "orionX",
                    "time": data["date"] / 1000,
                    "type": data["type"],
                    "fee": data["commission"]
                    / 10 ** currencies.CEROS[data["currency"]["code"]],
                    "currency_value": data["cost"]
                    / 10 ** currencies.CEROS[data["pairCurrency"]["code"]],
                    "pair_currency_value": data["amount"]
                    / 10 ** currencies.CEROS[data["currency"]["code"]],
                }
                for data in response["data"]["order"]["transactions"]
                if data["type"] == "trade-in"
            ]

            transactions = pydantic.parse_obj_as(
                List[Transaction], transaction_data)
            order_data = {
                "id": message.id,
                "amount": message.amount,
                "exchange": "orionX",
                "type": response["data"]["order"]["type"],
                "market": message.market,
                "status": message.status,
                "transactions": transactions,
            }
            order = Order.parse_obj(order_data)
            return order
        except Exception as err:
            logging.error(err)
            logging.debug(response)
            raise ParserError("OrionX Parser: Could not parse Order.")


class OrionXTransactionFromOrderResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict) -> Order:
        if response["data"]["order"] == None:
            raise ResponseError("OrionX Parser: No Order data received.")
        if "errors" in response:
            logging.error(response["errors"])
            raise ResponseError("OrionX Parser: Found errors in response")

        try:
            transaction_data = [
                {
                    "id": data["id"],
                    "currency_name": data["currency"]["code"],
                    "pair_currency_name": data["pairCurrency"]["code"],
                    "market": f"{data['currency']['code']}/{data['pairCurrency']['code']}",
                    "exchange": "orionX",
                    "time": data["date"] / 1000,
                    "type": data["type"],
                    "fee": data["commission"]
                    / 10 ** currencies.CEROS[data["currency"]["code"]],
                    "currency_value": data["cost"]
                    / 10 ** currencies.CEROS[data["pairCurrency"]["code"]],
                    "pair_currency_value": data["amount"]
                    / 10 ** currencies.CEROS[data["currency"]["code"]],
                }
                for data in response["data"]["order"]["transactions"]
                if data["type"] == "trade-in" or data["type"] == "trade-out"
            ]

            transactions = pydantic.parse_obj_as(
                List[Transaction], transaction_data)
            return transactions
        except Exception as err:
            logging.debug(err)
            raise ParserError(
                "OrionX Parser: Could not parse Transactions From Order Response."
            )


class OrionXWalletResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict) -> List[Wallet]:
        if response["data"]["me"] == None:
            raise ResponseError("OrionX Parser: No Order data received.")
        if "errors" in response:
            logging.error(response["errors"])
            raise ResponseError("OrionX Parser: Found errors in response")

        try:
            coins = {}
            available = {}
            loans = {}
            for wallet_data in response["data"]["me"]["wallets"]:
                currency = wallet_data["currency"]["code"]
                available_balance = round(
                    wallet_data["availableBalance"] /
                    10 ** currencies.CEROS[currency],
                    currencies.CEROS[currency],
                )
                balance = round(
                    wallet_data["balance"] / 10 ** currencies.CEROS[currency],
                    currencies.CEROS[currency],
                )
                if wallet_data["loanUsedAmount"]:
                    loan = round(
                        wallet_data["loanUsedAmount"]
                        / 10 ** currencies.CEROS[currency],
                        currencies.CEROS[currency],
                    )
                else:
                    loan = 0
                coins[currency] = {"name": currency, "amount": balance}
                available[currency] = {
                    "name": currency, "amount": available_balance}

                loans[currency] = {"name": currency, "amount": loan}

            wallets = pydantic.parse_obj_as(
                List[Wallet],
                [
                    {
                        "exchange": "orionX",
                        "coins": coins,
                        "sign": 1,
                        "time": time.time(),
                        "date": datetime.now(),
                    },
                    {
                        "exchange": "orionX-available",
                        "coins": available,
                        "sign": 0,
                        "time": time.time(),
                        "date": datetime.now(),
                    },
                    {
                        "exchange": "Loans",
                        "coins": loans,
                        "sign": -1,
                        "time": time.time(),
                        "date": datetime.now(),
                    },
                ],
            )

            return wallets
        except Exception as err:
            logging.debug(err)
            raise ParserError("OrionX Parser: Could not parse Balances")


class OrionXTradeHistoryResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict) -> List[Transaction]:
        if response["data"]["orders"] == None:
            raise ResponseError(
                "OrionX Parser: No Trade History data received.")
        if "errors" in response:
            logging.error(response["errors"])
            raise ResponseError("OrionX Parser: Found errors in response")

        try:

            for order_data in response["data"]["orders"]["items"]:

                transaction_data = order_data["transactions"]
                transaction_obj = [
                    {
                        "id": tx["_id"],
                        "currency_name": tx["currency"]["code"],
                        "pair_currency_name": tx["pairCurrency"]["code"],
                        "market": f"{tx['currency']['code']}/{tx['pairCurrency']['code']}",
                        "time": tx["date"] / 1000,
                        "exchange": "orionX",
                        "type": tx["type"],
                        "fee": tx["commission"]
                        / 10 ** currencies.CEROS[tx["currency"]["code"]],
                        "currency_value": tx["cost"]
                        / 10 ** currencies.CEROS[tx["pairCurrency"]["code"]],
                        "pair_currency_value": tx["amount"]
                        / 10 ** currencies.CEROS[tx["currency"]["code"]],
                        "taker": tx["adds"],
                        "order_id": tx["orderId"],
                    }
                    for tx in transaction_data
                ]

            transactions = pydantic.parse_obj_as(
                List[Transaction], transaction_obj)

            return transactions
        except Exception as err:
            logging.error(err)
            logging.debug(response)
            # raise ParserError("OrionX Parser: Could not parse Trade History.")


class KrakenTransactionResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict, message: EntityMessage) -> Transaction:
        if len(response["error"]) != 0:
            logging.error(response["error"])
            raise ResponseError("Kraken Parser: Response had errors")
        if response["result"] == {}:
            raise ResponseError("Kraken Parser: Response had no data")
        try:
            currency_name, pair_currency_name = message.market.split("/")
            currency_name = currencies.KRAKEN_RENAME_COINS[currency_name]
            pair_currency_name = currencies.KRAKEN_RENAME_COINS[pair_currency_name]
            transaction = Transaction.parse_obj(
                {
                    "id": message.id,
                    "currency_name": currency_name,
                    "pair_currency_name": pair_currency_name,
                    "market": f"{currency_name}/{pair_currency_name}",
                    "time": response["result"][message.id]["closetm"],
                    "exchange": "kraken",
                    "type": response["result"][message.id]["descr"]["type"],
                    "fee": response["result"][message.id]["fee"],
                    "currency_value": response["result"][message.id]["vol"],
                    "pair_currency_value": float(response["result"][message.id]["vol"])
                    * (
                        float(response["result"][message.id]["price"])
                        * (1 + currencies.KRAKEN_FEE)
                    ),
                }
            )

            return transaction
        except Exception as err:
            logging.error(err)
            raise ParserError("Kraken Parser: Could not parse Transaction.")


class KrakenTradeHistoryResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict):
        if len(response["error"]) != 0:
            logging.error(response["error"])
            raise ResponseError("Kraken Parser: Response had errors")
        try:
            transaction_data = []
            for _, tx in response["result"]["trades"].items():
                market = currencies.KRAKEN_RENAME_PAIRS[tx["pair"]]
                currency_name, pair_currency_name = market.split("/")
                data = {
                    "id": tx["ordertxid"],
                    "time": tx["time"],
                    "exchange": "kraken",
                    "type": tx["type"],
                    "market": market,
                    "fee": float(tx["fee"]),
                    "currency_name": currency_name,
                    "pair_currency_name": pair_currency_name,
                    "currency_value": float(tx["vol"]),
                    "pair_currency_value": float(tx["vol"])
                    * (float(tx["price"]) * (1 + currencies.KRAKEN_FEE)),
                }
                transaction_data.append(data)
            transactions = pydantic.parse_obj_as(
                List[Transaction], transaction_data)
            return transactions

        except Exception as err:
            logging.debug(err)
            raise ParserError("Kraken Parser: Could not parse Trade History")


class KrakenWalletResponseParser(AbstractResponseParser):
    def parse_response(self, response: dict) -> List[Wallet]:
        if len(response["error"]) != 0:
            logging.error(response["error"])
