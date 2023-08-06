import subprocess
from dotenv import load_dotenv
load_dotenv(override=True)

subprocess.run(['flask', 'run'])