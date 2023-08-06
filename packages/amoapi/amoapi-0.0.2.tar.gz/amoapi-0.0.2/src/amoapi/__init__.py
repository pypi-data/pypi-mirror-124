import os
from pathlib import Path
from requests import Session
from .interaction import BaseInteraction
from .tokens import TokenManager, FileTokensStorage

_session = Session

# load token manager
token_path = Path.cwd()


default_token_manager = TokenManager()
default_token_manager(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    subdomain=os.environ.get("subdomain"),
    redirect_url=os.environ.get("redirect_url"),
    storage=FileTokensStorage(str(token_path)),  # by default FileTokensStorage
)
default_token_manager.init(code=os.environ.get("start_code"), skip_error=True)
amo_interaction = BaseInteraction(token_manager=default_token_manager, session=_session)
