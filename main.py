import logging
from config_manager import ConfigManager
from database_manager import DatabaseManager
from gmail_service import GmailService
from rule_processor import RuleProcessor
from logging_config import setup_logging


def main():
    config_file = 'config.json'
    config = ConfigManager(config_file)

    db_path = config.get('db_path')
    credentials_path = config.get('credentials_path')
    token_path = config.get('token_path')
    rules_path = config.get('rules_path')
    scopes = config.get('scopes')
    log_file = config.get('log_file')

    setup_logging(log_file)

    db_manager = DatabaseManager(db_path)
    db_manager.create_tables()
    gmail_service = GmailService(credentials_path, token_path, scopes)

    logging.info('Fetching emails...')
    emails = gmail_service.fetch_emails()
    logging.info('Emails fetched...')
    logging.info('Storing into db')
    for email in emails:
        db_manager.store_email(*email)
    logging.info('Successfully written into db')

    rule_processor = RuleProcessor(db_manager, gmail_service, rules_path)
    logging.info('Processing rules')
    rule_processor.apply_rules()


if __name__ == '__main__':
    main()
