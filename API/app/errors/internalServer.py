from errors.errors import app, json, jsonify

@app.errorhandler(500)
def internal_server(error):
    return jsonify({
        "message": "Error Interno",
        "status": False
    }), 500