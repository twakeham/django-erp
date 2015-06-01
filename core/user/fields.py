from django.db import models as db


class UserField(db.ForeignKey):
    '''
        Allows middleware to find auto user fields in dynamic models
    '''
    pass