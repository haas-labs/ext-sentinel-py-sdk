# Profile Settings

The Profile settings allows to customize the behavior of Sentinel processes, related to process logic and launching of processes in different infrastructure: local, development, production. 

Profile settings can be populated using different mechanisms:
- Command line options
- Settings in environment or configuration YAML file
- Environment variables
- Default process or channel settings

## The list of predefined variables

### ETH_RPC_URL

The URL address to Ethereum JSON-RPC Interface

### ARB_RPC_URL

The URL address to Arbitrum JSON-RPC Interface

### BSC_RPC_URL

The URL address to BSC (BNB Chain) JSON-RPC Interface

### ETH_WS_URL

The Websocket interface to Ethereum Transactions data

### EXT_HTTP_URL

The Extractor REST Endpoint

### EXT_API_TOKEN

The Extractor API Token

### KAFKA_BOOTSTRAP_SERVERS

The Extractor Kafka Servers list

### KAFKA_INBOUND_TX_TOPIC

The Extractor Kafka Topic for receiving "extended" transactions

### KAFKA_OUTBOUND_EVENT_TOPIC

The Kafka Topic for sending events towards the Extractor


