from flask import Flask, Response, request, jsonify
import asyncio, warnings, time, json, sys, serial, psutil

sys.setrecursionlimit(5000)

warnings.filterwarnings("ignore", category=DeprecationWarning)

serialcom = serial.Serial('COM7', 9600)
serialcom.timeout = 1

app = Flask(__name__)

base = "/api"

import errors.errors
import routes.routes

if __name__ == "__main__":
    app.run()

