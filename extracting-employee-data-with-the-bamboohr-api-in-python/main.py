from pathlib import Path
import requests
import json

domain = 'your-bamboohr-domain'
base_url = f'https://api.bamboohr.com/api/gateway.php/{domain}/v1'

api_key = 'your-api-key'
auth = (api_key, '')

headers = {
    'Accept': 'application/json'
}


def get_all_employees():
    try:
        response_all_employees = requests.request('GET', f'{base_url}/employees/directory', headers=headers, auth=auth)
        if response_all_employees.status_code == 200:
            return response_all_employees.text
        else:
            print(
                f'Something went wrong when trying to get the requested info from the API server. Status code: {response_all_employees.status_code}. Message: {response_all_employees.reason}')
    except Exception as e:
        print("An error occurred while performing the API call: ", e)


def print_all_employees(employees_json):
    for entry in employees_json:
        print(
            f'{entry["displayName"]}: {entry["jobTitle"]} at {entry["department"]}, based in {entry["location"]} ({entry["division"]})')


def save_all_employees_to_file(employees_json):
    destination_dir = 'data'
    Path(destination_dir).mkdir(parents=True, exist_ok=True)
    json_file = f'{destination_dir}/all_employees.json'
    with open(json_file, 'w', encoding='utf-8') as target_file:
        json.dump(employees_json, target_file, ensure_ascii=False, indent=4)
    print(f"Data saved to {json_file}.")


all_employees = get_all_employees()
if all_employees is not None:
    all_employees_json = json.loads(all_employees)['employees']
    print_all_employees(all_employees_json)
    save_all_employees_to_file(all_employees_json)
