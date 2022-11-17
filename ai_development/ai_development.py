'''
This file was created by ]init[ AG 2022.

Module for Speech Service.
'''
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    log.info("Startup...")
    app.mount('/', StaticFiles(directory='resources/html', html=True), name='static')


@app.on_event("shutdown")
def shutdown_event():
    log.info("Shutting down...")

# Following ordering is important for overlapping path matches...


def main():
    import uvicorn
    os.chdir('ai_development')
    # just 1 worker, or models will be loaded multiple times!
    uvicorn.run('ai_development:app', host='0.0.0.0', port=8200)


if __name__ == '__main__':
    main()
