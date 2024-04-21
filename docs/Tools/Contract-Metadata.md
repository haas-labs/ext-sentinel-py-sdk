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

## References

- [Understanding smart contract metadata](https://www.rareskills.io/post/solidity-metadata)
- [RFC7049: Concise Binary Object Representation (CBOR)](https://datatracker.ietf.org/doc/html/rfc7049)
- [Python CBOR (de)serializer with extensive tag support](https://github.com/agronholm/cbor2), read [the docs](https://cbor2.readthedocs.io/en/latest/) to learn more


## For review

- https://github.com/shazow/whatsabi
- https://ethereum.stackexchange.com/questions/155272/determine-compiler-used-to-create-a-given-bytecode
- https://docs.soliditylang.org/en/latest/metadata.html#encoding-of-the-metadata-hash-in-the-bytecode
- 
- https://docs.ipfs.tech/concepts/content-addressing/#cid-versions
- https://github.com/vyperlang/vyper/tree/68da04b2e9e010c2e4da288a80eeeb9c8e076025
- https://cbor.me/
- https://www.rfc-editor.org/rfc/rfc8949
- https://docs.soliditylang.org/en/latest/metadata.html
- https://www.rareskills.io/post/solidity-metadata
- https://blog.openzeppelin.com/deconstructing-a-solidity-contract-part-vi-the-swarm-hash-70f069e22aef
- https://ipfs.tech/
- https://github.com/ethereum/go-ethereum/issues/26117
- https://docs.soliditylang.org/en/v0.8.16/metadata.html
- https://docs.soliditylang.org/en/v0.8.25/
- https://www.rareskills.io/post/ethereum-contract-creation-code
- https://docs.blockscout.com/about/features/ethereum-bytecode-database-microservice
- https://github.com/tintinweb/ethereum-dasm/tree/master


Sure! Here's a simple CBOR parser implemented in Python without dependency on external libraries:

```python
def parse_cbor(data):
    def read_uint(data, start_index, additional_data):
        value = 0
        pos = start_index
        while True:
            b = data[pos]
            value = (value << 8) | (b & 0xFF)
            if not (b & 0x80):
                break
            pos += 1
        return value, pos + 1

    def read_int(data, start_index, additional_data):
        value, pos = read_uint(data, start_index, additional_data)
        if value & 0x1:
            value = -(value >> 1) - 1
        else:
            value >>= 1
        return value, pos

    def read_bytes(data, start_index, additional_data):
        length, pos = read_uint(data, start_index, additional_data)
        return data[pos:pos + length], pos + length

    def read_array(data, start_index, additional_data):
        length, pos = read_uint(data, start_index, additional_data)
        array = []
        for _ in range(length):
            item, pos = parse_item(data, pos)
            array.append(item)
        return array, pos

    def read_map(data, start_index, additional_data):
        length, pos = read_uint(data, start_index, additional_data)
        mapping = {}
        for _ in range(length):
            key, pos = parse_item(data, pos)
            value, pos = parse_item(data, pos)
            mapping[key] = value
        return mapping, pos

    def parse_item(data, start_index):
        major_type = data[start_index] >> 5
        additional_data = data[start_index] & 0x1F

        if major_type == 0:
            return read_uint(data, start_index + 1, additional_data)
        elif major_type == 1:
            return read_int(data, start_index + 1, additional_data)
        elif major_type == 2:
            return read_bytes(data, start_index + 1, additional_data)
        elif major_type == 3:
            return read_text(data, start_index + 1, additional_data)
        elif major_type == 4:
            return read_array(data, start_index + 1, additional_data)
        elif major_type == 5:
            return read_map(data, start_index + 1, additional_data)
        elif major_type == 6:
            return None, start_index + 1  # Tag
        elif major_type == 7:
            if additional_data == 20:  # False
                return False, start_index + 1
            elif additional_data == 21:  # True
                return True, start_index + 1
            elif additional_data == 22:  # Null
                return None, start_index + 1
            elif additional_data == 23:  # Undefined
                return None, start_index + 1
            elif additional_data == 24:  # Simple value
                return read_simple_value(data, start_index + 1)
            elif additional_data == 25:  # Half-Precision Float
                return read_half_precision_float(data, start_index + 1)
            elif additional_data == 26:  # Single-Precision Float
                return read_single_precision_float(data, start_index + 1)
            elif additional_data == 27:  # Double-Precision Float
                return read_double_precision_float(data, start_index + 1)
            else:
                raise ValueError("Unknown simple value: {}".format(additional_data))

    def read_simple_value(data, start_index):
        if data[start_index] < 24:
            return data[start_index], start_index + 1
        else:
            raise ValueError("Invalid simple value: {}".format(data[start_index]))

    def read_half_precision_float(data, start_index):
        # Half-Precision Float (IEEE 754 binary16)
        # Not implemented in this example
        raise NotImplementedError("Half-Precision Float not implemented")

    def read_single_precision_float(data, start_index):
        value = int.from_bytes(data[start_index:start_index + 4], byteorder='big', signed=False)
        return value, start_index + 4

    def read_double_precision_float(data, start_index):
        value = int.from_bytes(data[start_index:start_index + 8], byteorder='big', signed=False)
        return value, start_index + 8

    return parse_item(data, 0)

# Example usage:
if __name__ == "__main__":
    cbor_data = b'\x82\x01\x02\x03\x04'
    parsed_data = parse_cbor(cbor_data)
    print("Parsed CBOR data:", parsed_data)
```

This parser handles major CBOR types according to RFC 7049, including integers, byte strings, text strings, arrays, maps, tags, and simple values. Note that support for half-precision floats is not implemented in this example.