from django.db import models as db


class Template(db.Model):

    def __unicode__(self):
        return self.name

    id = db.CharField(max_length=255, primary_key=True)
    name = db.CharField(max_length=255)
    template = db.TextField(blank=True, null=True)






