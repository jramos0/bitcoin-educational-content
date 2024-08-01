---
term: HARDENED DERIVATION
---

The process of generating child keys in HD wallets. Hardened derivation uses the parent private key as input for the `HMAC-SHA512` function, making it impossible to generate child public keys from the parent public key and parent chain code. The process involves concatenating the parent private key and an index greater than or equal to $2^{31}$, followed by the application of `HMAC-SHA512` with the parent chain code. The result is divided into two parts: the first 256 bits are added to the parent private key to obtain the child private key, while the remaining 256 bits form the child chain code. This method ensures that even if an extended public key is compromised, it cannot be used to derive child public keys. In standard derivation, hardened derivation is used at all levels of derivation up to the account depth. In derivation path notations, a hardened derivation is identified with an apostrophe `'` or more rarely with an `h`.
