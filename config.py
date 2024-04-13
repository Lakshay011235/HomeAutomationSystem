import os

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths to specific directories and files
config_dir = os.path.join(base_dir, 'config')
logs_dir = os.path.join(base_dir, 'logs')
src_dir = os.path.join(base_dir, 'src')
tests_dir = os.path.join(base_dir, 'tests')

# Import files from the config directory
config_file_path = os.path.join(config_dir, 'loggingConfig.json')

# Import files from the logs directory
logs_file_path = os.path.join(logs_dir, 'server.log')

# Import files from the src directory
client_file_path = os.path.join(src_dir, 'client.py')
demo2_file_path = os.path.join(src_dir, 'demo2.py')
helper_file_path = os.path.join(src_dir, 'helper.py')
server_file_path = os.path.join(src_dir, 'server.py')

# Import files from the tests directory
server_tests_file_path = os.path.join(tests_dir, 'serverTests.log')
test_demo_file_path = os.path.join(tests_dir, 'test_demo.py')
test_server_file_path = os.path.join(tests_dir, 'test_server.py')