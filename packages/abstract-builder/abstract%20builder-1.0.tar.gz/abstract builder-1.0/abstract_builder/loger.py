
class Loger:

    @staticmethod
    def log_str(module_name, location, text):
        log = "({0}): <{1}> {2}".format(module_name, location, text)

        print(log)

