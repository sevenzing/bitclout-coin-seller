import argparse
import logging
import concurrent.futures

from src.bitclout import getCoinsList, sellCoin


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s::%(asctime)s:\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S', level=logging.INFO)

    logger = logging.getLogger('creator_coin')

    
    parser = argparse.ArgumentParser(description='Sell account creator coin')
    parser.add_argument('-s', '--seedhex', help='seed hex of your account', required=True)
    parser.add_argument('-p', '--pubkey', help='your public key.', required=True)

    args = parser.parse_args()

    pubkey, seedhex = args.pubkey, args.seedhex

    logger.info("Scaning creator coins")

    coins = getCoinsList(pubkey)
    
    logger.info(f"Found {len(coins)} coin(s)")

    with concurrent.futures.ThreadPoolExecutor(max_workers = 1) as executor:
        future_to_coin = {executor.submit(sellCoin, coin, seedhex, pubkey): coin for coin in coins}
        for future in concurrent.futures.as_completed(future_to_coin):
            coin = future_to_coin[future]
            try:
                future.result()
            except Exception as exc:
                logger.error("%r generated an exception: %s" % (coin, exc))
            else:
                logger.info("%s solt." % (coin,))
