import os
from dotenv import load_dotenv
from pathlib import Path
from requests import Session
from .amoapi_basic import *
from .interaction import BaseInteraction
from .tokens import TokenManager, FileTokensStorage

_session = Session

# load token manager
amoapi_directory = Path(__file__).parent.resolve()
load_dotenv(Path(__file__).parent.resolve()/'.env')


default_token_manager = TokenManager()
default_token_manager(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    subdomain=os.environ.get("subdomain"),
    redirect_url=os.environ.get("redirect_url"),
    storage=FileTokensStorage(str(amoapi_directory)),  # by default FileTokensStorage
)
default_token_manager.init(code=os.environ.get("start_code"), skip_error=True)
amo_interaction = BaseInteraction(token_manager=default_token_manager, session=_session)
