from pydantic import BaseModel


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


class VeChainEventTransaction(BaseModel):
    """
    VeChain based Event Transaction
    """


#   addr:String,  // contract address
#   data:String,      // data
#   topics:Array[String] = Array(), // topics


class VeChainTransaction(BaseModel):
    """
    VeChain based Transaction
    """


#   ts:Long,          // timestamp
#   b:Long,           // block number
#   hash:String,      // transaction hash
#   sz:Int,           // size
#   from:String,      // from address
#   to:String,        // to address
#   v: BigInt,        // value
#   nonce:String,     // nonce
#   gas:BigInt,       // gas
#   pric:Int,         // gas coefficient
#   data:String,      // calldata
#   exp:Long,          // expirateion
#   del:Option[String],       // delegator
#   dep:Option[String],       // dependsOn
#   used: Long,       // gas used
#   pay: String,      // gas payer
#   paid: BigInt,     // gas payed
#   rwd: BigInt,      // reward
#   st: Boolean,    // status, 0 - failed
#   logs: Array[EventTx],   // Event logs
#   i:Option[Long] = None,  // transaction index in Block
