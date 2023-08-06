from configparser import ConfigParser

# Initialize the Parser.
config = ConfigParser()

# Add the Section.
config.add_section('main')

# Set the Values.
config.set('main', 'client_id', 'MSAZYYHPW3A64OOVBVXUDVBBJC3DOEFG')
config.set('main', 'redirect_uri', 'https://127.0.0.1:5000/login/callback')
config.set('main', 'credentials_path', 'C:/Users/Alex/OneDrive/Desktop/td_state.json')
config.set('main', 'account_number', '426494881')
config.set('main', 'ira_account_number', '426496649')

# Write the file.
with open(file='config/config.ini', mode='w+') as f:
    config.write(f)
