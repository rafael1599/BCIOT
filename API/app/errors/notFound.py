from errors.errors import app, json, jsonify

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "message": "Servicio no encontrado",
        "status": False
    }), 404