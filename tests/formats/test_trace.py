import json
import pathlib

from sentinel.formats.trace import Trace
from sentinel.formats.trace import AddressMetrics


def test_trace_stats_by_address_trace_0x95c5b177():
    """
    Test Trace Extact
    """
    test_address = "0xa5abfb56a78d2bd4689b25b8a77fd49bb0675874"
    trace_file = pathlib.Path("tests/formats/resources/trace_0x95c5b177.json")
    trace_data = json.load(trace_file.open("r"))

    trace = Trace(data=trace_data)
    trace_stats = trace.stats_by_address(types=["DELEGATECALL", "CALL"])

    assert trace_stats is not {}, "Empty stats"
    assert trace_stats[test_address] == AddressMetrics(
        from_counter=225, to_counter=41
    ), "Incorrect stats for address: 0xa5abfb56a78d2bd4689b25b8a77fd49bb0675874"


def test_trace_stats_by_address_trace_0x6aef8bb5():
    """
    Test Trace Extact
    """
    test_address = "0xa5abfb56a78d2bd4689b25b8a77fd49bb0675874"
    trace_file = pathlib.Path("tests/formats/resources/trace_0x6aef8bb5.json")
    trace_data = json.load(trace_file.open("r"))

    trace = Trace(data=trace_data)
    trace_stats = trace.stats_by_address(types=["DELEGATECALL", "CALL"])

    assert trace_stats is not {}, "Empty stats"
    assert trace_stats[test_address] == AddressMetrics(
        from_counter=440, to_counter=80
    ), "Incorrect stats for address: 0xa5abfb56a78d2bd4689b25b8a77fd49bb0675874"
