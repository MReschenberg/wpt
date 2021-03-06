import pytest

from tests.support.asserts import assert_error, assert_dialog_handled
from tests.support.inline import inline


def delete_cookie(session, name):
    return session.transport.send("DELETE", "/session/%s/cookie/%s" % (session.session_id, name))


def test_handle_prompt_dismiss_and_notify():
    """TODO"""


def test_handle_prompt_accept_and_notify():
    """TODO"""


def test_handle_prompt_ignore():
    """TODO"""


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept"})
def test_handle_prompt_accept(session, create_dialog):
    session.url = inline("<title>WD doc title</title>")

    create_dialog("alert", text="dismiss #1", result_var="dismiss1")
    response = delete_cookie(session, "foo")
    assert response.status == 200
    assert_dialog_handled(session, "dismiss #1")

    create_dialog("confirm", text="dismiss #2", result_var="dismiss2")
    response = delete_cookie(session, "foo")
    assert response.status == 200
    assert_dialog_handled(session, "dismiss #2")

    create_dialog("prompt", text="dismiss #3", result_var="dismiss3")
    response = delete_cookie(session, "foo")
    assert response.status == 200
    assert_dialog_handled(session, "dismiss #3")


def test_handle_prompt_missing_value(session, create_dialog):
    session.url = inline("<title>WD doc title</title>")
    create_dialog("alert", text="dismiss #1", result_var="dismiss1")

    response = delete_cookie(session, "foo")

    assert_error(response, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #1")

    create_dialog("confirm", text="dismiss #2", result_var="dismiss2")

    response = delete_cookie(session, "foo")
    assert_error(response, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #2")

    create_dialog("prompt", text="dismiss #3", result_var="dismiss3")

    response = delete_cookie(session, "foo")
    assert_error(response, "unexpected alert open")
    assert_dialog_handled(session, "dismiss #3")
