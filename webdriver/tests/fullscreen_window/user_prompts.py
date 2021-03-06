import pytest

from tests.support.asserts import assert_error, assert_dialog_handled
from tests.support.inline import inline


def read_global(session, name):
    return session.execute_script("return %s;" % name)


def fullscreen(session):
    return session.transport.send("POST", "session/%s/window/fullscreen" % session.session_id)


def test_handle_prompt_dismiss_and_notify():
    """TODO"""


def test_handle_prompt_accept_and_notify():
    """TODO"""


def test_handle_prompt_ignore():
    """TODO"""


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept"})
def test_handle_prompt_accept(session, create_dialog):
    session.url = inline("<title>WD doc title</title>")
    create_dialog("alert", text="accept #1", result_var="accept1")

    fullscreen(session)

    assert_dialog_handled(session, "accept #1")
    assert read_global(session, "accept1") is None

    read_global(session, "document.title")
    create_dialog("confirm", text="accept #2", result_var="accept2")

    fullscreen(session)

    assert_dialog_handled(session, "accept #2")
    assert read_global(session, "accept2"), True

    create_dialog("prompt", text="accept #3", result_var="accept3")

    fullscreen(session)

    assert_dialog_handled(session, "accept #3")
    assert read_global(session, "accept3") == "" or read_global(session, "accept3") == "undefined"


def test_handle_prompt_missing_value(session, create_dialog):
    session.url = inline("<title>WD doc title</title>")
    create_dialog("alert", text="dismiss #1", result_var="dismiss1")

    response = fullscreen(session)

    assert_error(response, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #1")
    assert read_global(session, "dismiss1") is None

    create_dialog("confirm", text="dismiss #2", result_var="dismiss2")

    response = fullscreen(session)

    assert_error(response, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #2")
    assert read_global(session, "dismiss2") is False

    create_dialog("prompt", text="dismiss #3", result_var="dismiss3")

    response = fullscreen(session)

    assert_error(response, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #3")
    assert read_global(session, "dismiss3") is None
