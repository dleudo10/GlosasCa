from django.db import models


class Maepro(models.Model):
    prcodi = models.CharField(db_column='PRCODI', primary_key=True, max_length=9)  # Field name made lowercase.
    prnomb = models.CharField(db_column='PrNomb', max_length=240, blank=True, null=True)  # Field name made lowercase.
    prnoop = models.SmallIntegerField(db_column='PrNoOp', blank=True, null=True)  # Field name made lowercase.
    plncod = models.CharField(db_column='PlnCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nivcod = models.CharField(db_column='NivCod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    praltcos = models.CharField(db_column='PrAltCos', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtrmodo = models.CharField(max_length=2, blank=True, null=True)
    impcod = models.CharField(db_column='IMPCOD', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prcpto = models.CharField(max_length=2, blank=True, null=True)
    prfinal = models.CharField(max_length=2, blank=True, null=True)
    tpprcd = models.SmallIntegerField(db_column='TpPrCd', blank=True, null=True)  # Field name made lowercase.
    prmccodi = models.CharField(db_column='PrMCCodi', max_length=9, blank=True, null=True)  # Field name made lowercase.
    pclcod = models.CharField(db_column='PClCod', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prtpo = models.SmallIntegerField(db_column='PrTpo', blank=True, null=True)  # Field name made lowercase.
    finprocod = models.CharField(db_column='FinProCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prsta = models.CharField(db_column='PrSta', max_length=1, blank=True, null=True)  # Field name made lowercase.
    predinc = models.SmallIntegerField(db_column='PrEdInc', blank=True, null=True)  # Field name made lowercase.
    predfnl = models.SmallIntegerField(db_column='PrEdFnl', blank=True, null=True)  # Field name made lowercase.
    prsexo = models.CharField(db_column='PrSexo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prdiagrsl = models.CharField(db_column='PrDiagRsl', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prdister = models.CharField(db_column='PrDisTer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    printres = models.CharField(db_column='PrIntRes', max_length=1, blank=True, null=True)  # Field name made lowercase.
    princoin = models.CharField(db_column='PrInCoIn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prprivez = models.CharField(db_column='PrPriVez', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pratndom = models.CharField(db_column='PrAtnDom', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prconsn = models.CharField(db_column='PrConSN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvalpran = models.CharField(db_column='PrValPrAn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prasigcit = models.CharField(db_column='PrAsigCit', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvacuna = models.CharField(db_column='PrVacuna', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prdosmax = models.SmallIntegerField(db_column='PrDosMax', blank=True, null=True)  # Field name made lowercase.
    prgarpro = models.SmallIntegerField(db_column='PrGarPro', blank=True, null=True)  # Field name made lowercase.
    prprobasl = models.CharField(db_column='PrProBasL', max_length=9, blank=True, null=True)  # Field name made lowercase.
    prsupsop = models.SmallIntegerField(db_column='PrSupSop', blank=True, null=True)  # Field name made lowercase.
    prtipdie = models.CharField(db_column='PrTipDie', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindobt = models.CharField(db_column='PrIndObt', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindapyo = models.CharField(db_column='PrIndApyO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prgarprm = models.SmallIntegerField(db_column='PrGarPrM', blank=True, null=True)  # Field name made lowercase.
    predamen = models.SmallIntegerField(db_column='PrEdaMen', blank=True, null=True)  # Field name made lowercase.
    prindvih = models.CharField(db_column='PrIndVIH', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prplttov = models.CharField(db_column='PrPlTtoV', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prcdhmpr = models.IntegerField(db_column='PrCdHmPr', blank=True, null=True)  # Field name made lowercase.
    prindagr = models.CharField(db_column='PrIndAgr', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindper = models.CharField(db_column='PrIndPer', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindinsc = models.CharField(db_column='PrIndInSC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindhici = models.SmallIntegerField(db_column='PrIndHiCi', blank=True, null=True)  # Field name made lowercase.
    prhom = models.CharField(db_column='PrHom', max_length=128, blank=True, null=True)  # Field name made lowercase.
    prindqxot = models.CharField(db_column='PrIndQxOt', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prressanpe = models.CharField(db_column='PrResSanPe', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prsuresno = models.CharField(db_column='PrSuResNo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prsoresno = models.CharField(db_column='PrSoResNo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prsocamu = models.CharField(db_column='PrSoCaMu', max_length=1, blank=True, null=True)  # Field name made lowercase.
    claagecod = models.CharField(db_column='ClaAgeCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    prmodexa = models.CharField(db_column='PrModExa', max_length=2, blank=True, null=True)  # Field name made lowercase.
    aplproenf = models.CharField(db_column='AplProEnf', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindpaq = models.CharField(db_column='PrIndPaq', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtpoefn = models.CharField(db_column='PRTPOEFN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtpoein = models.CharField(db_column='PRTPOEIN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prexcscl = models.CharField(db_column='PREXCSCL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtcod = models.IntegerField(db_column='PRTCOD', blank=True, null=True)  # Field name made lowercase.
    prsenoof = models.CharField(db_column='PRSENOOF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prindoxg = models.CharField(db_column='PRINDOXG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prrecane = models.CharField(db_column='PRRECANE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prsertra = models.CharField(db_column='PRSERTRA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtipmue = models.CharField(db_column='PRTIPMUE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prpaqser = models.CharField(db_column='PRPAQSER', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prtipatn = models.CharField(db_column='PrTipAtn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prpriori = models.CharField(db_column='PrPriori', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prvalaguvi = models.CharField(db_column='PrValAguVi', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maep_id = models.CharField(db_column='MAEP_ID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    prontape = models.CharField(db_column='PRONTAPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pronasct = models.CharField(db_column='PRONASCT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pronclpr = models.CharField(db_column='PRONCLPR', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pronfrme = models.CharField(db_column='PRONFRME', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pronfrti = models.DecimalField(db_column='PRONFRTI', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pronapes = models.SmallIntegerField(db_column='PRONAPES', blank=True, null=True)  # Field name made lowercase.
    pronores = models.SmallIntegerField(db_column='PRONORES', blank=True, null=True)  # Field name made lowercase.
    prapclihe = models.CharField(db_column='PRAPCLIHE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prappobi = models.CharField(db_column='PrApPoBi', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAEPRO'
