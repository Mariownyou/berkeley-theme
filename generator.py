import json
import os
import time


def change_all_values(d, key, new_val):
    for k, v in d.items():
        if isinstance(v, dict):
            d = change_all_values(v, key, new_val)
        if isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    d = change_all_values(i, key, new_val)
                else:
                    if i == key:
                        d[v.index(i)] = new_val
        else:
            if v == key:
                d[k] = new_val
    return d


def json_with_comments_to_json(json_with_comments):
    json_without_comments = ''
    for line in json_with_comments.splitlines():
        if not line.strip().startswith('//') and '//' not in line:
            json_without_comments += line + '\n'
        if '//' in line:
            json_without_comments += line.split('//')[0] + '\n'
    return json_without_comments


def remove_whitespace(json_string):
    json_string = json_string.replace('\n', '')
    json_string = json_string.replace('\t', '')
    json_string = json_string.replace(' ', '')
    return json_string


def clean_trailing_commas(json_string):
    json_string = json_string.replace(',}', '}')
    json_string = json_string.replace(',]', ']')
    return json_string


def generate():
    with open('themes/light-color-theme.json', 'r') as read_file, open('out/light-color-theme.json', 'w') as write_file:
        data = json_with_comments_to_json(read_file.read())
        data = remove_whitespace(data)
        data = clean_trailing_commas(data)
        data = json.loads(bytes(data, 'utf-8').decode('utf-8-sig'))

        variables = data['vars']
        data.pop('vars', None)

        for name, val in variables.items():
            d = change_all_values(data, name, val)

        json.dump(data, write_file, indent=4)


def watcher():
    file = 'themes/light-color-theme.json'
    last_modified = os.stat(file).st_mtime
    while True:
        if os.stat(file).st_mtime != last_modified:
            generate()
            last_modified = os.stat(file).st_mtime
            print('Theme changed, generating...')
        time.sleep(0.5)


watcher()
