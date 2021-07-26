import requests
import enum
import typing


class CoinOperationType(enum.Enum):
    SELL = 'sell'
    BUY = 'buy'


def safePost(url, payload, *args, **kwargs):
    response = requests.post(url, json=payload, *args, **kwargs)
    if not response.ok:
        try:
            error = response.json()["error"]
        except:
            error = response.content
        
        raise ValueError(f"response error: {error}")

    return response


def buyOrSellCreatorCoinTx(senderPubKey: str, creatorPubKey: str, opType: CoinOperationType, nanos: int):
    payload = {
        "BitCloutToAddNanos": 0,
        "BitCloutToSellNanos": nanos if opType == CoinOperationType.BUY else 0,
        "CreatorCoinToSellNanos": nanos if opType == CoinOperationType.SELL else 0,
        "CreatorPublicKeyBase58Check": creatorPubKey,
        "MinCreatorCoinExpectedNanos": 0,
        "MinFeeRateNanosPerKB": 1000,
        "OperationType": opType.value,
        "UpdaterPublicKeyBase58Check": senderPubKey,
    }
    return safePost(
        url='https://bitclout.com/api/v0/buy-or-sell-creator-coin',
        payload=payload
    )


def getUsersStateless(pubKeys: typing.List[str]):
    payload = {
        "PublicKeysBase58Check": pubKeys
    }
    return safePost(
        url="https://bitclout.com/api/v0/get-users-stateless",
        payload=payload
    )
    

def submitTransaction(signedTxHex):
    payload = {
        "TransactionHex": signedTxHex
    }
    return safePost(
        url="https://bitclout.com/api/v0/submit-transaction", 
        payload=payload,
    )
