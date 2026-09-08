from django.db import models

class Tipproc(models.Model):
    tiprcod = models.SmallIntegerField(db_column='TiPrCod', primary_key=True)  # Field name made lowercase.
    tiprdes = models.CharField(db_column='TiPrDes', max_length=60, blank=True, null=True)  # Field name made lowercase.
    gpripscd = models.CharField(db_column='GPRIPSCd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tiprordpo = models.CharField(db_column='TIPRORDPO', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TIPPROC'