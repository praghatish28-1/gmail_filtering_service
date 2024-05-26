Feature: Unit test for rule processing

  Scenario Outline: Check if rule is valid or not
    When I pass rule<rule>, it must not throw any error
    Then I should not get any error and get output <output>
    Examples:
        | rule | output |
        | [ { "description": "Rule 1", "if": "all", "conditions": [ { "field_name": "From", "predicate": "contains", "value": "jobalerts-noreply@linkedin.com" }, { "field_name": "Subject", "predicate": "contains", "value": "software engineer" } ], "perform_actions": [ "mark_as_read", "move_to_linkedinjobs" ] }, { "description": "Rule 2", "if": "any", "conditions": [ { "field_name": "Date received", "predicate": "less_than", "value": "2022-01-01" } ], "perform_actions": [ "mark_as_unread" ] } ]  | None  |
        | [ { "description": "Rule 1", "if": "all", "conditions": [ { "field_name": "From", "predicate": "contains", "value": "jobalerts-noreply@linkedin.com" }, { "field_name": "Subject", "predicate": "contains", "value": "software engineer" } ], "perform_actions": [ "mark_as_read", "move_to_linkedinjobs" ] }, { "description": "Rule 2", "if": "any", "conditions": [ { "field_name": "Date received", "predicate": "less_than", "value": "2022-01-01" } ], "perform_tions": [ "mark_as_unread" ] } ]    | "Not a valid rule"  |
        | [ { "description": "Rule 1", "if": "all", "conditions": [ { "field_name": "From", "predicate": "contains", "value": "jobalerts-noreply@linkedin.com" }, { "field_name": "Subject", "predicate": "contains", "value": "software engineer" } ], "perform_actions": [ "mark_as_read", "move_to_linkedinjobs" ] }, { "description": "Rule 2", "if": "any", "conditions": [ { "field_name": "Date received", "predicate": "hello", "value": "2022-01-01" } ], "perform_actions": [ "mark_as_unread" ] } ]      | "Not a valid rule"  |
