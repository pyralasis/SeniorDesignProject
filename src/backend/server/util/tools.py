# Random tools

def get_routes(app):
    """
    Get all the routes from the app
    """
    return [rule for rule in app.url_map.iter_rules()]
