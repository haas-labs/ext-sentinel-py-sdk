from typing import List, Optional

from pydantic import AliasChoices, BaseModel, Field


class VeChainBlock(BaseModel):
    """
    VeChain based Block
    """


#   ts:Long,      // timestamp
#   i:Long,       // block number
#   hash:String,  // block hash
#   phash:String, // parent hash
#   sz:Int,       // size
#   gas:Long,         // timestamp
#   ben: String,      // beneficiary
#   used: Long,       // gas used
#   scor: Long,        // totalscore
#   troot: String,       // tx root
#   feat: Int,          // tx features
#   sroot: String,      // state root
#   rroot: String,      // receipt root
#   com: Boolean,       // com
#   signr: String,      // signer
#   trnk: Boolean,      // is trunk
#   fin: Boolean,       // is finalized
#   tx:Option[Array[Transaction]], // transactions


class VeChainLogEntry(BaseModel):
    """
    VeChain based Event Transaction
    """

    #   addr:String,  // contract address
    address: str = Field(validation_alias=AliasChoices("addr", "address"))

    #   data:String,      // data
    data: str

    #   topics:Array[String] = Array(), // topics
    topics: List[str] = Field(default_factory=list)


class VeChainTransaction(BaseModel):
    """
    VeChain based Transaction
    """

    # i:Option[Long] = None,  // transaction index in Block
    transaction_index: int = Field(validation_alias=AliasChoices("i", "transaction_index"))

    # ts:Long,          // timestamp
    timestamp: int = Field(validation_alias=AliasChoices("ts", "timestamp"))

    # b:Long,           // block number
    block_nbr: int = Field(validation_alias=AliasChoices("b", "block_nbr"))

    # hash:String,      // transaction hash
    hash: str

    # sz:Int,           // size
    size: int = Field(validation_alias=AliasChoices("sz", "size"))

    # from:String,      // from address
    from_address: str = Field(validation_alias=AliasChoices("from", "from_address"))

    # to:String,        // to address
    to_address: str = Field(validation_alias=AliasChoices("to", "to_address"))

    # v: BigInt,        // value
    value: int = Field(validation_alias=AliasChoices("v", "value"))

    # nonce:String,     // nonce
    nonce: str

    # gas:BigInt,       // gas
    gas: int

    # pric:Int,         // gas coefficient
    gas_coefficient: int = Field(validation_alias=AliasChoices("pric", "gas_coefficient"))

    # used: Long,       // gas used
    gas_used: int = Field(validation_alias=AliasChoices("used", "gas_used"))

    # pay: String,      // gas payer
    gas_payer: str = Field(validation_alias=AliasChoices("pay", "gas_payer"))

    # paid: BigInt,     // gas payed
    gas_payed: int = Field(validation_alias=AliasChoices("paid", "gas_payed"))

    # data:String,      // calldata
    data: str

    # exp:Long,          // expiration
    expiration: int = Field(validation_alias=AliasChoices("exp", "expiration"))

    # del:Option[String],       // delegator
    delegator: Optional[str] = Field(validation_alias=AliasChoices("del", "delegator"), default=None)

    # dep:Option[String],       // dependsOn
    depends_on: Optional[str] = Field(validation_alias=AliasChoices("dep", "depends_on"), default=None)

    # rwd: BigInt,      // reward
    reward: int = Field(validation_alias=AliasChoices("rwd", "reward"))

    # st: Boolean,    // status, 0 - failed
    status: bool = Field(validation_alias=AliasChoices("st", "status"))

    # logs: Array[EventTx],   // Event logs
    logs: List[VeChainLogEntry] = Field(default_factory=list)
