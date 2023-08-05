import environ


class MrEnv(environ.Env):
    def __init__(self, prefix, **scheme):
        self.prefix = prefix
        super(MrEnv, self).__init__(**scheme)

    def get_value(self, var, cast=None, default=environ.Env.NOTSET, parse_default=False):
        var = '{}_{}'.format(self.prefix, var)
        return super(MrEnv, self).get_value(var, cast, default, parse_default)
