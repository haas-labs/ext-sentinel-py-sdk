from sentinel.db.contract.abi.static import (
    ABI_EVENT_OWNERSHIP_TRANSFERED,
    ABI_EVENT_TRANSFER,
    ABI_EVENT_UPGRADED,
)
from sentinel.models.transaction import LogEntry
from sentinel.utils.transaction import Event, filter_events


def test_filter_events_ownership_transfered():
    logs = [
        LogEntry(
            index=174,
            address="0x1111111254eeb25477b68fb85ed929f73a960582",
            data="0x",
            topics=[
                "0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0",
                "0x0000000000000000000000000000000000000000000000000000000000000000",
                "0x000000000000000000000000ccbdbd9b0309a77fc6a56e087ff2765ff394012e",
            ],
        )
    ]
    events = list(filter_events(log_entries=logs, signatures=[ABI_EVENT_OWNERSHIP_TRANSFERED]))
    assert len(events) == 1, "Incorrect number of ownership transfered events"

    ownership_transfered_event: Event = events[0]
    assert (
        ownership_transfered_event.address == "0x1111111254eeb25477b68fb85ed929f73a960582"
    ), "Incorrect event address value"
    assert ownership_transfered_event.type == "OwnershipTransferred", "Incorrect event type"
    assert ownership_transfered_event.fields == {
        "event_signature_hash": "0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0",
        "previousOwner": "0x0000000000000000000000000000000000000000",
        "newOwner": "0xccbdbd9b0309a77fc6a56e087ff2765ff394012e",
    }, "Incorrect event fields"


def test_filter_events_upgraded():
    logs = [
        LogEntry(
            index=56,
            address="0x68d30f47f19c07bccef4ac7fae2dc12fca3e0dc9",
            data="0x",
            topics=[
                "0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
                "0x00000000000000000000000034f2b21107afe3584949c184a1e6236ffdac4f6f",
            ],
        )
    ]
    events = list(filter_events(log_entries=logs, signatures=[ABI_EVENT_UPGRADED]))
    assert len(events) == 1, "Incorrect number of upgraded events"

    upgraded_event: Event = events[0]
    assert upgraded_event.address == "0x68d30f47f19c07bccef4ac7fae2dc12fca3e0dc9", "Incorrect event address value"
    assert upgraded_event.type == "Upgraded", "Incorrect event type"
    assert upgraded_event.fields == {
        "event_signature_hash": "0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
        "implementation": "0x34f2b21107afe3584949c184a1e6236ffdac4f6f",
    }, "Incorrect event fields"


def test_filter_events_transfer():
    logs = [
        LogEntry(
            index=78,
            address="0xdac17f958d2ee523a2206206994597c13d831ec7",
            data="0x000000000000000000000000000000000000000000000000000000000a652541",
            topics=[
                "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                "0x0000000000000000000000008fca4ade3a517133ff23ca55cdaea29c78c990b8",
                "0x000000000000000000000000df60ba7f7469ff884673dd11361fb66cb06b8560",
            ],
        )
    ]
    events = list(filter_events(log_entries=logs, signatures=[ABI_EVENT_TRANSFER]))
    assert len(events) == 1, "Incorrect number of transfer events"

    transfer_event: Event = events[0]
    assert transfer_event.address == "0xdac17f958d2ee523a2206206994597c13d831ec7", "Incorrect event address value"
    assert transfer_event.type == "Transfer", "Incorrect event type"
    assert transfer_event.fields == {
        "event_signature_hash": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "from": "0x8fca4ade3a517133ff23ca55cdaea29c78c990b8",
        "to": "0xdf60ba7f7469ff884673dd11361fb66cb06b8560",
        "value": 174400833,
    }, "Incorrect event fields"


# def test_filter_events_withdrawal():
#     logs = [
#         LogEntry(
#             index=56,
#             address="0x68d30f47f19c07bccef4ac7fae2dc12fca3e0dc9",
#             data="0x",
#             topics=[
#                 "0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
#                 "0x00000000000000000000000034f2b21107afe3584949c184a1e6236ffdac4f6f",
#             ],
#         )
#     ]
#     events = list(filter_events(log_entries=logs, signatures=[ABI_EVENT_WITHDRAWAL]))
#     assert len(events) == 1, "Incorrect number of upgraded events"

#     withdrawal_event: Event = events[0]
#     assert withdrawal_event.address == "0x68d30f47f19c07bccef4ac7fae2dc12fca3e0dc9", "Incorrect event address value"
#     assert withdrawal_event.type == "Upgraded", "Incorrect event type"
#     assert withdrawal_event.fields == {
#         "event_signature_hash": "0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
#         "implementation": "0x34f2b21107afe3584949c184a1e6236ffdac4f6f",
#     }, "Incorrect event fields"
