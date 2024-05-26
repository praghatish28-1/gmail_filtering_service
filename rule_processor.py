import json
import logging

logger = logging.getLogger(__name__)

class RuleProcessor:
    def __init__(self, db_manager, gmail_service, rules_file):
        self.db_manager = db_manager
        self.gmail_service = gmail_service
        self.rules_file = rules_file
        self.predicate_strategies = {
            "contains": self.contains,
            "does_not_contain": self.does_not_contain,
            "equals": self.equals,
            "does_not_equal": self.does_not_equal,
            "less_than": self.less_than,
            "greater_than": self.greater_than
        }
        self.field_validators = {
            "description": self.validate_description,
            "if": self.validate_condition_type,
            "conditions": self.validate_conditions,
            "perform_actions": self.validate_actions
        }

    def load_rules(self):
        try:
            with open(self.rules_file, 'r') as f:
                rules = json.load(f)
                self.validate_rules(rules)
                return rules
        except Exception as e:
            logger.error(f"Error loading rules file: {e}")
            return []

    def validate_rules(self, rules):
        if not isinstance(rules, list):
            raise ValueError("Rules file must contain a list of rules.")

        for rule in rules:
            for field, validator in self.field_validators.items():
                if field not in rule:
                    raise ValueError(f"Rule is missing '{field}' field.")
                validator(rule[field])

    def validate_description(self, description):
        if not isinstance(description, str):
            raise ValueError("Description must be a string.")

    def validate_condition_type(self, condition_type):
        if condition_type not in ["all", "any"]:
            raise ValueError("Condition type must be 'all' or 'any'.")

    def validate_conditions(self, conditions):
        if not isinstance(conditions, list):
            raise ValueError("Conditions must be a list of dictionaries.")

        for condition in conditions:
            if not isinstance(condition, dict):
                raise ValueError("Each condition must be a dictionary.")

            if "field_name" not in condition or not isinstance(condition["field_name"], str):
                raise ValueError("Each condition must have a 'field_name' string.")

            if "predicate" not in condition or not isinstance(condition["predicate"], str):
                raise ValueError("Each condition must have a 'predicate' string.")

            if "value" not in condition:
                raise ValueError("Each condition must have a 'value' field.")

    def validate_actions(self, actions):
        if not isinstance(actions, list):
            raise ValueError("Actions must be a list of strings.")

        for action in actions:
            if not isinstance(action, str):
                raise ValueError("Each action must be a string.")

    # Predicate functions...


    def apply_rules(self):
        rules = self.load_rules()
        if not rules:
            logger.info("No rules found.")
            return

        emails = self.db_manager.get_emails()
        for email in emails:
            for rule in rules:
                if self.evaluate_rule(rule, email):
                    self.apply_actions(rule, email)

    def evaluate_rule(self, rule, email):
        condition_type = rule.get("if", "all")
        conditions = rule.get("conditions", [])
        match_all = condition_type.lower() == "all"

        for condition in conditions:
            field_name = condition.get("field_name")
            predicate = condition.get("predicate")
            value = condition.get("value")
            predicate_strategy = self.predicate_strategies.get(predicate)

            if not predicate_strategy:
                logger.error(f"Invalid predicate: {predicate}")
                return False

            email_value = email.get(field_name)
            if email_value is None:
                logger.error(f"Invalid field name: {field_name}")
                return False

            if not predicate_strategy(email_value, value):
                if match_all:
                    return False
            elif not match_all:
                return True

        return match_all

    def apply_actions(self, rule, email):
        actions = rule.get("perform_actions", [])
        for action in actions:
            if action == "mark_as_read":
                self.gmail_service.modify_email_labels(email['id'], [], ['UNREAD'])
            elif action == "mark_as_unread":
                self.gmail_service.modify_email_labels(email['id'], ['UNREAD'], [])
            elif action.startswith("move_to_"):
                label = action.replace("move_to_", "")
                label_id = self.gmail_service.get_label_id(label)
                if label_id:
                    self.gmail_service.modify_email_labels(email['id'], [label_id], [])
                else:
                    logger.error(f"Label not found: {label}")

    # Predicate functions
    def contains(self, value, substring):
        return substring.lower() in value.lower()

    def does_not_contain(self, value, substring):
        return substring.lower() not in value.lower()

    def equals(self, value, target):
        return value.lower() == target.lower()

    def does_not_equal(self, value, target):
        return value.lower() != target.lower()

    def less_than(self, value, target):
        return value < target

    def greater_than(self, value, target):
        return value > target
