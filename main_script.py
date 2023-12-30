import subprocess

subprocess.run(['python3', 'scripts/first_filtering.py'])

subprocess.run(['python3', 'scripts/second_filtering.py'])

subprocess.run(['python3', 'scripts/grouping.py'])

subprocess.run(['python3', 'scripts/meteo_API_request.py'])

subprocess.run(['python3', 'scripts/converter_time.py'])

subprocess.run(['python3', 'scripts/data_meteo_merge.py'])