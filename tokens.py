class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value


def token_end():
    return Token('END', '$')


def token_non_term():
    return Token('NON_TERM', 'N')
