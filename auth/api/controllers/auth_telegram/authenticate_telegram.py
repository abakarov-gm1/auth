from controllers.auth.login import create_access_token
from repositories.user_repository import create_user, check_phone_telegram_id, get_user_login_service


def create_token(params):
    user = get_user_login_service(params["phone"])  # получаем пользователя по телефону нужен его id
    return create_access_token(data={"user_id": user.id})


def authenticate(query_params):
    query_params = dict(query_params)

    if query_params.get("user_id") is not None:
        # если id существует значит хотим связать с существующим пользователем пока не реализовано
        pass

    if not check_phone_telegram_id(query_params["phone"], query_params["id"]):

        create_user(
            phone=query_params["phone"],
            name=query_params["first_name"],
            telegram_id=query_params["id"],
            telegram_username=query_params["username"],
            region=query_params["region"]
        )

        return create_token(query_params)

    return create_token(query_params)





