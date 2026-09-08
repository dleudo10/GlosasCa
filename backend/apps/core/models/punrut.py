from django.db import models

class Punrut(models.Model):
    pk = models.CompositePrimaryKey('EMPCOD', 'MCDpto', 'PunRutCod')
    empcod = models.CharField(db_column='EMPCOD', max_length=2)  # Field name made lowercase.
    mcdpto = models.CharField(db_column='MCDpto', max_length=9)  # Field name made lowercase.
    punrutcod = models.CharField(db_column='PunRutCod', max_length=4)  # Field name made lowercase.
    punrutdes = models.CharField(db_column='PunRutDes', max_length=60, blank=True, null=True)  # Field name made lowercase.
    punruttip = models.CharField(db_column='PunRutTip', max_length=1, blank=True, null=True)  # Field name made lowercase.
    depcod = models.CharField(db_column='DepCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    punrutcae = models.CharField(db_column='PunRutCaE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    punrutenc = models.CharField(db_column='PunRutEnC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    punrutest = models.CharField(db_column='PunRutEst', max_length=1, blank=True, null=True)  # Field name made lowercase.
    punaudex = models.CharField(db_column='PunAudEx', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ubiarecod = models.CharField(db_column='UbiAreCod', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PUNRUT'