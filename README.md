Bitclout creator coin seller
===


## 1. Install python requirements.txt
```bash
$ python -m pip install -r requirements.txt
```

## 2. Find your seedHex

Open https://bitclout.com/ > Dev tools > Application > Storage > Local Storage > https://identity.bitclout.com > users > Select the public key with which you want to sell > seedHex

> Note that you should not share seedhex to anyone! Sharing seedhex is equivalent of sharing seed phrase

## 3. Find your public key 

Open https://bitclout.com/wallet > Public key > Copy


## 4. Run python script

```bash
$ python sell_creator_coins.py --seedhex <your_seed_hex> --pubkey <your_pub_key>
INFO::07/25/2021 09:20:36:      Scaning creator coins
INFO::07/25/2021 09:20:36:      Found 3 coin(s)
INFO::07/25/2021 09:20:37:      CreatorCoin(amount=35, owner='BC1YLj4iUraQabhUBT8kS1gCieXhD1GGXeFCcU3qM3MGgf7GwBJ9Va7') solt.
INFO::07/25/2021 09:20:38:      CreatorCoin(amount=7476, owner='BC1YLianxEsskKYNyL959k6b6UPYtRXfZs4MF3GkbWofdoFQzZCkJRB') solt.
INFO::07/25/2021 09:20:39:      CreatorCoin(amount=3210, owner='BC1YLiFNARSWF6qtXM5acrS7q8VWPeeS2gycVBtqLALkE4c1V3kx4US') solt.
```
