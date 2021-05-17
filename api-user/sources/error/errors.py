def handle_401_error(_):
    return '사용자 인증에 실패 하였습니다.', 401


def handle_404_error(_):
    return '그런 URL은 존재하지 않습니다.', 404


def handle_500_error(_):
    return '무언가 잘못 되었습니다.. :(', 500
