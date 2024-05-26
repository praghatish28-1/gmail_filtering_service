import json
from unittest import mock
from unittest.mock import MagicMock
from behave import *
from hamcrest import equal_to, assert_that
from rule_processor import RuleProcessor


rule_process = RuleProcessor(None, None, None)
@when('I pass rule{rule}, it must not throw any error')
def step_impl(context, rule):
    try:
        context.output = rule_process.validate_rules(json.loads(rule))
    except Exception:
        context.output = "Not a valid rule"

@then('I should not get any error and get output {output}')
def step_impl(context, output):
    if not context.output:
        received_output = "None"
    else:
        received_output = context.output
    assert_that(received_output, output)