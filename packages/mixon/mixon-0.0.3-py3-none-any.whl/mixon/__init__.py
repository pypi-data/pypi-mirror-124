__all__ = ["load", "loads", "dump", "dumps"]

import io
import re
import json


def load(fp, **kwargs):
    mode = 'normal'
    text_key = None
    lines = []
    result = {}

    def _collect_normal_data():
        nonlocal lines, result, kwargs
        normal_data = json.loads(''.join(lines), **kwargs)
        result.update(normal_data)
        lines.clear()

    def _collect_text_field():
        nonlocal text_key, lines, result
        result[text_key] = ''.join(lines)
        lines.clear()

    for line in fp:
        m = re.match(r'^#-{3,}:\s*(?P<key>.+?)\s*:-{3,}#\s*$', line)
        if m:
            if mode == 'normal':
                _collect_normal_data()
                mode = 'text'
                text_key = m.group('key')
            else:
                _collect_text_field()
                text_key = m.group('key')
        else:
            if mode == 'normal':
                line = line.strip()
                if line and not line.startswith('#'):
                    lines.append(line)
            else:
                lines.append(line)

    if lines:
        if mode == 'normal':
            _collect_normal_data()
        else:
            _collect_text_field()

    return result


def loads(s, **kwargs):
    return load(io.StringIO(s), **kwargs)

def dump(obj, fp, **kwargs):
    pass

def dumps(obj, **kwargs):
    pass