
* Dockerfile
  * RUN pip-cache activated: Don't download >2GB torch with each build
  * See [Cache Mounts](https://docs.docker.com/build/guide/mounts/#:~:text=Cache%20mounts%20are%20created%20using,to%20mount%20into%20the%20container)
  * Requires Docker setting DOCKER_BUILDKIT=1
