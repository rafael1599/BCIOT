from flask import Flask, Response, request, jsonify
import asyncio
import warnings
import time
import json
import sys
import serial
sys.setrecursionlimit(5000)

warnings.filterwarnings("ignore", category=DeprecationWarning)

serialcom = serial.Serial('COM5', 9600)
serialcom.timeout = 1

app = Flask(__name__)

base = "/api"

import errors.errors
import routes.routes

if __name__ == "__main__":
    app.run()

