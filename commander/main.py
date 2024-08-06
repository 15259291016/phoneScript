'''
Date: 2024-08-05 11:19:02
LastEditors: 牛智超
LastEditTime: 2024-08-06 14:14:15
FilePath: \tbScripte\commander\main.py
'''
# app/start.py
import uvicorn
from app.app import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
