def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Auth-Token'
    response.headers['Access-Control-Expose-Headers'] = 'X-Auth-Token'
    return response
