# Random tools


import urllib

from quart import Quart


def get_routes(app: Quart):
    """
    Get all the routes from the app
    """
    return [rule for rule in app.url_map.iter_rules()]


def print_routes(app: Quart):
    output = []
    for rule in app.url_map.iter_rules():
        methods = ",".join(rule.methods)  # type: ignore
        line = urllib.parse.unquote("{:32s} {:20s} {}".format(str(rule), methods, rule.endpoint))  # type: ignore
        output.append(line)

    for line in sorted(output):
        print(line)
