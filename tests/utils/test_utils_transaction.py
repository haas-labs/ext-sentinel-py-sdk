from sentinel.db.contract.abi.static import (
    ABI_EVENT_OWNERSHIP_TRANSFERED,
    ABI_EVENT_TRANSFER,
    ABI_EVENT_UPGRADED,
    ABI_EVENT_WITHDRAWAL,
)
from sentinel.models.transaction import LogEntry
from sentinel.utils.transaction import Event, filter_events

LOGS = [
    # OwnershipTransferred
    LogEntry(
        index=174,
        address="0x1111111254eeb25477b68fb85ed929f73a960582",
        data="0x",
        topics=[
            "0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0",
            "0x0000000000000000000000000000000000000000000000000000000000000000",
            "0x000000000000000000000000ccbdbd9b0309a77fc6a56e087ff2765ff394012e",
        ],
    ),
    # Upgraded
    LogEntry(
        index=56,
        address="0x68d30f47f19c07bccef4ac7fae2dc12fca3e0dc9",
        data="0x",
        topics=[
            "0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
            "0x00000000000000000000000034f2b21107afe3584949c184a1e6236ffdac4f6f",
        ],
    ),
    # Transafer
    LogEntry(
        index=78,
        address="0xdac17f958d2ee523a2206206994597c13d831ec7",
        data="0x000000000000000000000000000000000000000000000000000000000a652541",
        topics=[
            "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
            "0x0000000000000000000000008fca4ade3a517133ff23ca55cdaea29c78c990b8",
            "0x000000000000000000000000df60ba7f7469ff884673dd11361fb66cb06b8560",
        ],
    ),
    # Withdrawal
    LogEntry(
        index=296,
        address="0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc",
        data="0x0000000000000000000000005eed3381114089ed3f7d80a96c625b1e7695b35f0e0a63d0aa39ebdb80c1fdbc1d9d0a9399805719e89d6f5b053053f0e2deafb8000000000000000000000000000000000000000000000000000da17d7f0c8770",
        topics=[
            "0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
            "0x0000000000000000000000004750bcfcc340aa4b31be7e71fa072716d28c29c5",
        ],
    ),
]


def test_filter_events_ownership_transfered():
    events = list(filter_events(log_entries=LOGS, signatures=[ABI_EVENT_OWNERSHIP_TRANSFERED]))
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
    events = list(filter_events(log_entries=LOGS, signatures=[ABI_EVENT_UPGRADED]))
    assert len(events) == 1, "Incorrect number of upgraded events"

    upgraded_event: Event = events[0]
    assert upgraded_event.address == "0x68d30f47f19c07bccef4ac7fae2dc12fca3e0dc9", "Incorrect event address value"
    assert upgraded_event.type == "Upgraded", "Incorrect event type"
    assert upgraded_event.fields == {
        "event_signature_hash": "0xbc7cd75a20ee27fd9adebab32041f755214dbc6bffa90cc0225b39da2e5c2d3b",
        "implementation": "0x34f2b21107afe3584949c184a1e6236ffdac4f6f",
    }, "Incorrect event fields"


def test_filter_events_transfer():
    events = list(filter_events(log_entries=LOGS, signatures=[ABI_EVENT_TRANSFER]))
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


def test_filter_events_withdrawal():
    events = list(filter_events(log_entries=LOGS, signatures=[ABI_EVENT_WITHDRAWAL]))
    assert len(events) == 1, "Incorrect number of upgraded events"

    withdrawal_event: Event = events[0]
    assert withdrawal_event.address == "0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc", "Incorrect event address value"
    assert withdrawal_event.type == "Withdrawal", "Incorrect event type"
    assert withdrawal_event.fields == {
        "event_signature_hash": "0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
        "fee": 3836735071750000,
        "nullifierHash": b"\x0e\nc\xd0\xaa9\xeb\xdb\x80\xc1\xfd\xbc\x1d\x9d\n\x93\x99\x80W\x19\xe8\x9do[\x050S\xf0\xe2\xde\xaf\xb8",
        "relayer": "0x4750bcfcc340aa4b31be7e71fa072716d28c29c5",
        "to": "0x5eed3381114089ed3f7d80a96c625b1e7695b35f",
    }, "Incorrect event fields"


def test_filter_several_events():
    events = list(filter_events(log_entries=LOGS, signatures=[ABI_EVENT_UPGRADED, ABI_EVENT_TRANSFER]))
    assert len(events) == 2, "Incorrect number of events"
