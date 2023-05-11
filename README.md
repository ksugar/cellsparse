# Cellsparse

## Getting started

### Clone repository

```
git clone --recurse-submodules git@github.com:ksugar/cellsparse.git
cd cellsparse
```

### Build Docker image

```
docker build -t cellsparse .
```

### Run Docker container

```
docker run --rm --gpus all -v $(pwd)/src:/src -p 8888:8888 cellsparse
```