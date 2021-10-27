from functools import wraps
import traceback
from logging import error


def autocommit(func):
    @wraps(func)
    def decorated_function(self, *args, **kwargs):
        try:
            ret = func(self, *args, **kwargs)
        except:
            error(0, traceback.format_exc())
            self.db.rollback()
            raise
        self.db.commit()
        return ret
    return decorated_function