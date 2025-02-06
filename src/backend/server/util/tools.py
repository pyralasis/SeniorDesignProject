# Random tools


from quart import Quart
import urllib

def get_routes(app: Quart):
    """
    Get all the routes from the app
    """
    return [rule for rule in app.url_map.iter_rules()]

def print_routes(app: Quart):
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:32s} {:20s} {}".format(str(rule), methods, rule.endpoint))
        output.append(line)

    for line in sorted(output):
        print(line)