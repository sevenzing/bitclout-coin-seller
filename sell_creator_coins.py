import argparse
import logging
import concurrent.futures
import time


from src.bitclout import getCoinsList, sellCoin


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s::%(asctime)s:\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO)

    logger = logging.getLogger('creator_coin')

    
    parser = argparse.ArgumentParser(description='Sell account creator coin')
    parser.add_argument('-s', '--seedhex', help='seed hex of your account', required=True)
    parser.add_argument('-p', '--pubkey', help='your public key.', required=True)
    parser.add_argument('-t', '--timesleep', help='sleep between requests', default=5, type=int)

    args = parser.parse_args()

    pubkey, seedhex, sleep_time = args.pubkey, args.seedhex, args.timesleep

    logger.info("Scaning creator coins")

    coins = getCoinsList(pubkey)
    coins.sort(key=lambda c: c.amount, reverse=True)

    logger.info(f"Found {len(coins)} coin(s)")

    while coins:
        coin = coins.pop(0)
        try:
            sellCoin(coin, seedhex, pubkey)
        except Exception as e:
            logger.error("%r generated an exception: %s" % (coin, e))
            coins.append(coin)
        else:
            logger.info("%s solt." % (coin,))

        time.sleep(sleep_time)
