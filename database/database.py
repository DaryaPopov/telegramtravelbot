from database.models import db, User, Request


def add_new_request_db(username, telegram_id, sent_date, command, result_text) -> None:
    try:
        with db:
            user = User.get_or_create(name=username, telegram_id=telegram_id)
            user_id = user[0].id
            Request.create(sent_date=sent_date, command=command,
                           user_id=user_id, result=result_text)
    except BaseException as err:
        print('Data record error:', err)


def get_requests_history_dict(message):
    """ Возвращает записи из таблицы запросов"""
    try:
        with db:
            user = User.get(User.telegram_id == message.from_user.id and User.name == message.from_user.first_name)
            user_id = user.id
            cur_query = Request.select().where(Request.user_id == user_id).limit(10).order_by(Request.sent_date.desc())
            return cur_query.dicts().execute()
    except BaseException as err:
        print('History sending error', err)
