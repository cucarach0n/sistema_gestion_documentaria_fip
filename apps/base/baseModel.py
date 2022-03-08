from django.db import models
from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
    changed_by = models.ForeignKey('auth.User')
    history = HistoricalRecords(inherit=True)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value