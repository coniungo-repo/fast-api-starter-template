from typing import Any, Dict, Optional, Union

from supertokens_python.recipe.passwordless.interfaces import (
    ConsumeCodeOkResult,
    RecipeInterface,
)
from supertokens_python.recipe.session.interfaces import SessionContainer

from src.database.session import AsyncSessionLocal
from src.modules.users.application.schemas import UserCreate
from src.modules.users.dependencies import build_user_service


def override_passwordless_functions(
    original_implementation: RecipeInterface,
) -> RecipeInterface:

    original_consume_code = original_implementation.consume_code

    async def consume_code(
        pre_auth_session_id: str,
        user_input_code: Union[str, None],
        device_id: Union[str, None],
        link_code: Union[str, None],
        session: Optional[SessionContainer],
        should_try_linking_with_session_user: Union[bool, None],
        tenant_id: str,
        user_context: Dict[str, Any],
    ):

        result = await original_consume_code(
            pre_auth_session_id,
            user_input_code,
            device_id,
            link_code,
            session,
            should_try_linking_with_session_user,
            tenant_id,
            user_context,
        )

        if (
            session is None
            and isinstance(result, ConsumeCodeOkResult)
            and len(result.user.login_methods) == 1
            and result.created_new_recipe_user
        ):
            email = result.user.emails[0]

            async with AsyncSessionLocal() as db:
                try:
                    service = build_user_service(db)

                    await service.create_from_supertokens(
                        auth_id=result.user.id,
                        data=UserCreate(
                            email=email,
                        ),
                    )

                    await db.commit()

                except Exception:
                    await db.rollback()
                    raise

        return result

    original_implementation.consume_code = consume_code

    return original_implementation
