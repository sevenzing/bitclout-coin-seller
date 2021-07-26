import dataclasses
import typing
import logging

from src.crypto import signTransaction
from src.network import buyOrSellCreatorCoinTx, submitTransaction, getUsersStateless, CoinOperationType


@dataclasses.dataclass
class CreatorCoin:
    amount: int
    owner: str


def getCoinsList(pubKey: str) -> typing.List[CreatorCoin]:
    user_info = getUsersStateless([pubKey]).json()["UserList"][0]
    
    raw_coins = user_info.get("UsersYouHODL", [])
    if not raw_coins:
        raise ValueError(f"Cannot find tokens for user with public key '{pubKey}'")

    coins: typing.List[CreatorCoin] = []

    for raw_coin in raw_coins:
        creator_coin = CreatorCoin(
                amount=raw_coin["BalanceNanos"],
                owner=raw_coin["CreatorPublicKeyBase58Check"]
            )
        if creator_coin.amount:
            coins.append(creator_coin)
        else:
            logging.warning(f"{creator_coin} has zero amount")
        
    return coins

def generateBuyOrSellCreatorCoinTx(senderPubKey: str, creatorPubKey: str, opType: CoinOperationType, nanos: int) -> str:
    return buyOrSellCreatorCoinTx(senderPubKey, creatorPubKey, opType, nanos).json()["TransactionHex"]

def generateSellCreatorCoinTx(senderPubKey: str, creatorPubKey: str, amount: int) -> str:
    return generateBuyOrSellCreatorCoinTx(
        senderPubKey,
        creatorPubKey,
        CoinOperationType.SELL,
        amount,
    )

def signAndSendTransaction(seedHex: str, txHex: str):
    signedTxHex = signTransaction(seedHex, txHex)
    return submitTransaction(signedTxHex)

def sellCoin(coin: CreatorCoin, seedhex: str, senderPubKey: str):
    response = signAndSendTransaction(
            seedHex=seedhex,
            txHex=generateSellCreatorCoinTx(
                senderPubKey=senderPubKey,
                creatorPubKey=coin.owner,
                amount=coin.amount,
            ),
        )

    return response.json()