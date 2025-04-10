class DEBUG:
    flag = False

    @staticmethod
    def get_flag():
        return DEBUG.flag

    @staticmethod
    def switch_debug():
        DEBUG.flag = not DEBUG.flag