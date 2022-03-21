from app.dao.account_dao import find_list


def user_list(criteria):
    if (criteria.get('page') is None) or (not criteria.get('page').isdigit()):
        criteria['page'] = 1
    else:
        criteria['page'] = int(criteria.get('page'))

    if (criteria.get('per_page') is None) or (not criteria.get('per_page').isdigit()):
        criteria['per_page'] = 10
    else:
        criteria['per_page'] = int(criteria.get('per_page'))

    return find_list(criteria)
