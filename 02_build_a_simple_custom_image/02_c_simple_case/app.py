#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 19:28:12 2018

@author: allen
"""
from flask import Flask
import os
import socket


app = Flask(__name__)

@app.route("/")
def hello():
    html = "<h3>Hello {name} </h3>" \
           "<b>Hostname:</b> {hostname}<br/>" 
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
