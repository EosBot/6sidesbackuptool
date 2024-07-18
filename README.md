## Dependencies
[borgbackup](https://borgbackup.readthedocs.io/en/stable/installation.html#dependencies)

```bash
sudo apt-get install python3 python3-dev python3-pip python3-virtualenv python3-wheel \
libacl1-dev libacl1 libssl-dev liblz4-dev libzstd-dev libxxhash-dev \
build-essential pkg-config python3-pkgconfig

sudo apt-get install libfuse-dev fuse    # needed for llfuse
sudo apt-get install libfuse3-dev fuse3  # needed for pyfuse3
sudo apt-get install borgbackup
```
[borgapi](https://pypi.org/project/borgapi/)

```bash
python3 -m virtualenv env
source env/bin/activate
pip install python-dotenv
pip install borgapi
```
[fastapi](https://fastapi.tiangolo.com/)
```bash
pip install fastapi
```
## Usage

```bash
fastapi dev main.py
```

### Docker Build

```bash
docker build --build-arg GITHUB_TOKEN=TOKEN_GERADO -t 6sides-backup .
```
### Docker run
```bash
docker run -d -p 8000:8000 6sides-backup
```
