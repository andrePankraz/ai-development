"""
This file was created by ]init[ AG 2023.

Module for Generic AI Development Service.
"""
from ai_development.data_model import HealthCheck
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import gc
import logging
import mimetypes
import os
from pathlib import Path
import torch

logger = logging.getLogger(__name__)

LOG_FILENAME = os.environ.get("LOG_FILENAME")
LOG_FOLDER = Path(LOG_FILENAME).parent if LOG_FILENAME else None


async def shutdown():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FastAPI...")

    # Serve static files
    app.mount("/", StaticFiles(directory="src/ai_development/resources/html", html=True), name="static")

    if LOG_FOLDER:
        LOG_FOLDER.mkdir(parents=True, exist_ok=True)

    logger.info("Running FastAPI...")
    yield

    logger.info("Shutting down FastAPI...")
    await shutdown()


app = FastAPI(root_path=os.getenv("BASE_PATH", ""), lifespan=lifespan)
templates = Jinja2Templates(directory="src/ai_development/resources/templates")


# Following ordering is important for overlapping path matches...
@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


def list_files(request: Request, route_prefix: str, subpath: str, folder_path: Path):
    """
    List the contents of a given directory.

    Args:
      request: The HTTP request object.
      route_prefix: The URL prefix for the route.
      subpath: The subpath within the shared folder.
      folder_path: The base path of the shared folder as a Path object.

    Returns:
      An HTML response listing the contents of the directory.
    """
    if subpath and not subpath.startswith("/"):
        raise HTTPException(status_code=404, detail="Path not found")
    clean_subpath = Path(subpath.lstrip("./"))
    current_path = folder_path / subpath.lstrip("./")
    if not current_path.exists():
        raise HTTPException(status_code=404, detail="Path not found")

    if current_path.is_file():
        content_type, _ = mimetypes.guess_type(str(current_path))
        return FileResponse(
            path=str(current_path),
            filename=current_path.name,
            media_type=content_type,
            headers={"Content-Disposition": "inline"},
        )

    # List directory
    files = []
    subdirs = []
    for item in current_path.iterdir():
        if item.is_dir():
            subdirs.append(item.name)
        else:
            files.append(item.name)

    # Relative paths to files and subdirectories
    rel_parent_folder = str(Path(route_prefix) / clean_subpath.parent) if clean_subpath else None
    rel_subdirs = [str(Path(route_prefix) / clean_subpath / item) for item in subdirs]
    rel_files = [str(Path(route_prefix) / clean_subpath / item) for item in files]

    # Pass to template
    return templates.TemplateResponse(
        "list_files.html", {"request": request, "parent": rel_parent_folder, "subdirs": rel_subdirs, "files": rel_files}
    )


if LOG_FOLDER:

    @app.get("/logs{subpath:path}", response_class=HTMLResponse)
    def list_log_files(request: Request, subpath: str = ""):
        return list_files(request, "/logs", subpath, LOG_FOLDER)


gc.collect()
torch.cuda.empty_cache()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "ai_development.service:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8200")),
        reload=True,
        reload_dirs="src",
        workers=1,
    )

#########################################################################
#
# Custom Stuff...
#
#########################################################################

