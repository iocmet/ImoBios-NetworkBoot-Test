import sys
import os
import pathlib

def toLuaDict(dictionary):
    result = '{ '
    for k, v in dictionary.items():
        if v.__class__ == str:
            result += f'[\'{k}\'] = \'{v}\', '
        elif v.__class__ == dict:
            result += f'[\'{k}\'] = {toLuaDict(v)}, '
        elif v.__class__ == list:
            _result = f'[\'{k}\'] = {{ '
            for v in v:
                _result += f'\'{v}\', '
            if len(v) > 0:
                _result = _result[:-2]
            _result += ' }, '
            if len(v) < 1:
                _result = _result.replace('  ', '')
            result += _result
    result = result[:-2]
    result += ' }'
    result = result.replace('} }', '}}').replace('{ {', '{{')
    return result
excludes = ['.git', 'README.md', 'generateConfig.py']
result = { 'initFile': sys.argv[1], 'fileList': {} }
for directory, _, files in os.walk(sys.argv[2]):
    path = pathlib.Path(directory.replace(os.sep, '/').lstrip('.'))
    if (path.parts[1] if path.parts[1:] else None) not in excludes:
        directories = list(path.parts[1:] if path.parts[0:] else [])
        result['fileList'][str.join('/', directories)] = files

print(toLuaDict(result))