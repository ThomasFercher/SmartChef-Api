from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    default_limits=["10 per Minute"],
    storage_uri="memory://",
)


blacklist = set()