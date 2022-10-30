from errors.errors import app, json, jsonify

@app.errorhandler(ValueError)
def value_error(error):
    strError = json.loads(str(error).replace("'", '"'))
    res = {
        "message": strError.get('message'),
        "code": strError.get('code'),
        "success": False,
        "error": "ValueError"
    }
    return jsonify(res), 500