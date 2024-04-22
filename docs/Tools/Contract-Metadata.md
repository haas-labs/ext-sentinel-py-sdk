# Contract Metadata

The compiler currently by default appends the IPFS hash (in CID v0) of the canonical metadata file and the compiler version to the end of the bytecode. 

Optionally, a Swarm hash instead of the IPFS, or an experimental flag is used. Below are all the possible fields:

```json
{
  "ipfs": "<metadata hash>",
  // If "bytecodeHash" was "bzzr1" in compiler settings not "ipfs" but "bzzr1"
  "bzzr1": "<metadata hash>",
  // Previous versions were using "bzzr0" instead of "bzzr1"
  "bzzr0": "<metadata hash>",
  // If any experimental features that affect code generation are used
  "experimental": true,
  "solc": "<compiler version>"
}
```
This information is stored [CBOR](https://tools.ietf.org/html/rfc7049)-encoded. The last two bytes in the bytecode indicate the length of the CBOR encoded information. By looking at this length, the relevant part of the bytecode can be decoded with a CBOR decoder.


## Solidity Metadata

When solidity generates the bytecode for the smart contract to be deployed, it appends metadata about the compilation at the end of the bytecode (by default), which gets stored to the blockchain when the constructor finishes executing. 

```
...22e2c375079c74dab80b9c0492dc8a9a57c332c6364736f6c63430008120033
```
The last two bytes `0033` (51 decimal) mean “look backward 0x33 bytes, that is the metadata.” This refers to all the code between the leading fe (which is the INVALID opcode) and the ending 0033.

## Vyper Metadata

To be described later

- https://github.com/vyperlang/vyper/
- https://ethereum.stackexchange.com/questions/155272/determine-compiler-used-to-create-a-given-bytecode

## IPFS

- https://ipfs.tech/
- https://docs.ipfs.tech/concepts/content-addressing/#cid-versions


## Swarm

to be descsribed later

- https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-vi-the-swarm-hash-70f069e22aef

## References

- [Contract Metadata](https://docs.soliditylang.org/en/latest/metadata.html)
- [Understanding smart contract metadata](https://www.rareskills.io/post/solidity-metadata)
- [Ethereum smart contract creation code](https://www.rareskills.io/post/ethereum-contract-creation-code)
- [RFC7049: Concise Binary Object Representation (CBOR)](https://datatracker.ietf.org/doc/html/rfc7049)
- [RFC8949: Concise Binary Object Representation (CBOR)](https://www.rfc-editor.org/rfc/rfc8949)
- [Python CBOR (de)serializer with extensive tag support](https://github.com/agronholm/cbor2), read [the docs](https://cbor2.readthedocs.io/en/latest/) to learn more
- [CBOR playground](https://cbor.me/)
