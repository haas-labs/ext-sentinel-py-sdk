import pytest

from sentinel.utils.message import render_message

VALUES = {"node": "ReportAlertEvidence", "step": "collect_alert_evidence", "attempt": 2}


def test_render_message_fills_known_placeholders():
    assert (
        render_message("{node} ({step}) attempt {attempt}", VALUES)
        == "ReportAlertEvidence (collect_alert_evidence) attempt 2"
    )


def test_render_message_leaves_unknown_placeholders_as_is():
    assert render_message("{node} for {customer}", VALUES) == "ReportAlertEvidence for {customer}"


@pytest.mark.parametrize("template", [None, "", "   ", 42])
def test_render_message_falls_back_to_default(template):
    assert render_message(template, VALUES, default="{node} completed") == "ReportAlertEvidence completed"


def test_render_message_without_default_renders_empty():
    assert render_message(None, VALUES) == ""


@pytest.mark.parametrize(
    "template, expected",
    [
        ("{node", "{node"),
        ("node}", "node}"),
        ("{}", "{}"),
        ("{not a name}", "{not a name}"),
        ("{{node}}", "{ReportAlertEvidence}"),
        ("{attempt:>3}", "{attempt:>3}"),
    ],
)
def test_render_message_never_fails_on_braces(template, expected):
    assert render_message(template, VALUES) == expected


def test_render_message_does_not_fill_a_value_twice():
    values = {**VALUES, "error": "KeyError: '{node}'"}
    assert render_message("{node}: {error}", values) == "ReportAlertEvidence: KeyError: '{node}'"


def test_render_message_none_value_is_empty():
    assert render_message("[{error}]", {"error": None}) == "[]"


def test_render_message_keeps_the_value_length():
    long_error = "x" * 500
    assert render_message("{error}", {"error": long_error}) == long_error
