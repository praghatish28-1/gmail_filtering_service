# Email Rule Processor

This project is a rule-based system for email processing, where rules are specified in a JSON format with descriptions, conditions, and actions. It allows you to define rules to automatically perform actions on emails based on specified criteria.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/email-rule-processor.git

2. Install dependencies:
    ``pip install -r requirements.txt``

## Obtaining and Storing Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. In the sidebar, navigate to "APIs & Services" > "Credentials".
4. Click on "Create credentials" and select "OAuth client ID".
5. Select "Desktop app" as the application type.
6. Give your OAuth client a name and click "Create".
7. Click on the download icon next to your newly created OAuth client to download the `credentials.json` file.
8. Place the `credentials.json` file in your project directory.

   Update your `config.json` file to include the path to your `credentials.json` file:
   
      ```json
      {
        "db_path": "path/to/database.db",
        "credentials_path": "path/to/credentials.json",
        "token_path": "path/to/token.pickle",
        "rules_path": "path/to/rules.json",
        "scopes": [
          "https://www.googleapis.com/auth/gmail.modify"
        ],
        "log_file": "path/to/logfile.log"
      }
   
## Default Configuration
   By default, the config.json file is expected to be in the same directory as main.py. You can modify the config_file attribute in the ConfigManager class to change the default file name or location.
   
   
   ## Running the App
   
   1. Ensure that you have completed the installation and configuration steps.
   2. Open a terminal or command prompt.
   3. Navigate to the project directory.
   4. Run the application with the following command:
   
      ```sh
      python main.py