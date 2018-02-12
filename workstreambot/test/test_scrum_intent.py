import json

import workstreambot.scrum.dictionary as dict
from workstreambot.message_handler import MessageHandler

confidence_level = 0.77


def test_switch_scrum():
    nlu = perform_initial_input("What is Scrum about?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 0

    nlu = perform_initial_input("What's Scrum about?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 0

    nlu = perform_initial_input("What about Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 0

    nlu = perform_initial_input("Tell me more about Scrum")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 0

    nlu = perform_initial_input("Tell me something about Scrum")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 0

    nlu = perform_initial_input("How is this in Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 0


def test_switch_scrum_theme():
    nlu = perform_initial_input("What are the roles in Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_theme(nlu['entities'])
    # TODO assert get_theme_value(nlu['entities']) == 'roles'

    nlu = perform_initial_input("What are the meetings in Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_theme(nlu['entities'])
    assert get_theme_value(nlu['entities']) == 'ceremonies'

    nlu = perform_initial_input("What are the ceremonies in Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_theme(nlu['entities'])
    assert get_theme_value(nlu['entities']) == 'ceremonies'


def test_switch_scrum_detail():
    # TODO
    nlu = perform_initial_input("What is the role of the developers in Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_detail(nlu['entities'])
    assert get_detail_value(nlu['entities']) == 'developers'

    nlu = perform_initial_input("What does the Product Owner in Scrum?")
    assert nlu['intent']['name'] == "switch_scrum"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_detail(nlu['entities'])
    assert get_detail_value(nlu['entities']) == 'product owner'


def test_inform_theme():
    # TODO
    nlu = perform_initial_input("Tell me about the roles")
    assert nlu['intent']['name'] == "inform"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_theme(nlu['entities'])
    # TODO assert get_theme_value(nlu['entities']) == 'roles'


def test_inform_detail():
    # TODO
    nlu = perform_initial_input("Tell me more about the Product Owner")
    assert nlu['intent']['name'] == "inform"
    assert nlu['intent']['confidence'] > confidence_level
    assert len(nlu['entities']) == 1
    assert entities_contain_detail(nlu['entities'])
    assert get_detail_value(nlu['entities']) == 'product owner'


def test_details():
    for detail in get_all_details():
        nlu = perform_inform("Tell me more about " + detail)
        assert nlu['intent']['name'] == "inform", "Expected intent for " + detail + " is incorrect"
        assert nlu['intent']['confidence'] > confidence_level
        assert len(nlu['entities']) == 1, "Expected entities for " + detail + " are incorrect"
        assert entities_contain_detail(nlu['entities']), "Expected entity for " + detail + " is incorrect"
        assert get_detail_value(nlu['entities']) == detail


def test_continue():
    nlu = perform_single_continue("Yes")
    assert nlu['intent']['name'] == "continue"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("Continue")
    assert nlu['intent']['name'] == "continue"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("Ok")
    assert nlu['intent']['name'] == "continue"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("Please yes")
    assert nlu['intent']['name'] == "continue"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("Yes please")
    assert nlu['intent']['name'] == "continue"
    assert nlu['intent']['confidence'] > confidence_level


def test_denys():
    nlu = perform_single_continue("No")
    assert nlu['intent']['name'] == "deny"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("Don't continue")
    assert nlu['intent']['name'] == "deny"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("Stop")
    assert nlu['intent']['name'] == "deny"
    assert nlu['intent']['confidence'] > confidence_level

    nlu = perform_single_continue("No thanks")
    assert nlu['intent']['name'] == "deny"
    assert nlu['intent']['confidence'] > confidence_level


def perform_initial_input(initial_input):
    handler = MessageHandler({"scrum"})
    response = send_message(handler, initial_input, "test_session")
    return response['nlu']


def perform_single_continue(continue_input):
    handler = MessageHandler({"scrum"})
    send_message(handler, "What is Scrum about?", "test_session")

    response = send_message(handler, continue_input, "test_session")
    return response['nlu']


def perform_inform(inform_input):
    handler = MessageHandler({"scrum"})
    send_message(handler, "What is Scrum about?", "test_session")

    response = send_message(handler, inform_input, "test_session")
    return response['nlu']


def send_message(handler, message, session_id):
    return json.loads(handler.converse(message, session_id))


def entities_contain_theme(entities):
    for entity in entities:
        if entity['entity'] == 'theme':
            return True
    return False


def get_theme_value(entities):
    for entity in entities:
        if entity['entity'] == 'theme':
            return entity['value']
    return None


def entities_contain_detail(entities):
    for entity in entities:
        if entity['entity'] == 'detail':
            return True
    return False


def get_detail_value(entities):
    for entity in entities:
        if entity['entity'] == 'detail':
            return entity['value']
    return None


def get_all_details():
    details = []
    for theme in dict.scrum:
        if 'details' in dict.scrum[theme]:
            for detail in dict.scrum[theme]['details']:
                details.append(detail)
    return details
