from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.recipe import passwordless, session
from supertokens_python.recipe.passwordless import ContactEmailOnlyConfig

from src.core.config import settings
from src.integrations.supertokens.overrides import override_passwordless_functions


def configure_auth():
    init(
        app_info=InputAppInfo(
            app_name=settings.APP_NAME,
            api_domain=settings.BACKEND_URL,
            website_domain=settings.FRONTEND_URL,
            api_base_path="/auth",
            website_base_path="/auth",
        ),
        supertokens_config=SupertokensConfig(
            connection_uri=settings.SUPER_TOKENS_CONNECTION_URI,
            # api_key: <YOUR_API_KEY>
        ),
        framework="fastapi",
        recipe_list=[
            session.init(),
            passwordless.init(
                override=passwordless.InputOverrideConfig(
                    functions=override_passwordless_functions
                ),
                flow_type="MAGIC_LINK",
                contact_config=ContactEmailOnlyConfig(),
            ),
        ],
    )
