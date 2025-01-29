# Random tools


from quart import Quart


def get_routes(app: Quart):
    """
    Get all the routes from the app
    """
    return [rule for rule in app.url_map.iter_rules()]
