""" sample test to dry run the dataset """
import json  

import sys
sys.path.append("C:\\Users\\harshit_work\Desktop\\web projects\\rival_assignment")
from main import analyze_api_logs

with open("test_data/sample_large.json", "r") as f:
    logs = json.load(f)

result = analyze_api_logs(logs)

print(json.dumps(result, indent=2))