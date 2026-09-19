from blog.bootstrap.web import build_web
from blog.runtime.config import config_path, load

app = build_web(load(config_path()))