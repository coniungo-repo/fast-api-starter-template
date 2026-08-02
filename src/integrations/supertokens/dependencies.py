from typing import Annotated

from fastapi import Depends
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session

AuthSession = Annotated[
    SessionContainer,
    Depends(verify_session()),
]
