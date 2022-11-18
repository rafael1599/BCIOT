from flask import Flask, Response, request, jsonify
import asyncio
import warnings
import time
import json
import sys
sys.setrecursionlimit(5000)

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)

base = "/api"

import errors.errors
import routes.routes

if __name__ == "__main__":
    app.run()

