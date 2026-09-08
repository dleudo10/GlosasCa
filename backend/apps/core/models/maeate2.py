from django.db import models
from .maeate import Maeate

class Maeate2(models.Model):
    pk = models.CompositePrimaryKey('MPNFac', 'MATipDoc', 'MACscP')
    mpnfac = models.ForeignKey(Maeate, models.DO_NOTHING, db_column='MPNFac')  # Field name made lowercase.
    matipdoc = models.ForeignKey(Maeate, models.DO_NOTHING, db_column='MATipDoc', related_name='maeate2_matipdoc_set')  # Field name made lowercase.
    macscp = models.IntegerField(db_column='MACscP')  # Field name made lowercase.
    prcodi = models.ForeignKey('Maepro', models.DO_NOTHING, db_column='PRCODI', blank=True, null=True)  # Field name made lowercase.
    mahoncod = models.CharField(db_column='MaHonCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    matipp = models.SmallIntegerField(db_column='MATipP', blank=True, null=True)  # Field name made lowercase.
    madipr = models.CharField(db_column='MADiPr', max_length=7, blank=True, null=True)  # Field name made lowercase.
    viacod = models.CharField(db_column='ViaCod', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mafepr = models.DateTimeField(db_column='MAFePr', blank=True, null=True)  # Field name made lowercase.
    madipp = models.CharField(db_column='MADiPP', max_length=7, blank=True, null=True)  # Field name made lowercase.
    maproc = models.SmallIntegerField(db_column='MAProc', blank=True, null=True)  # Field name made lowercase.
    mapera = models.SmallIntegerField(db_column='MAPerA', blank=True, null=True)  # Field name made lowercase.
    mmcodm = models.CharField(db_column='MMCODM', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mecomm = models.SmallIntegerField(db_column='MECoMM', blank=True, null=True)  # Field name made lowercase.
    madico = models.CharField(db_column='MADiCo', max_length=7, blank=True, null=True)  # Field name made lowercase.
    mavatp = models.DecimalField(db_column='MAVaTP', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    manumas = models.CharField(db_column='MANumAS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    maconp = models.CharField(db_column='MAConP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    msupro = models.CharField(db_column='MSUPro', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maepro = models.SmallIntegerField(db_column='MAEPro', blank=True, null=True)  # Field name made lowercase.
    mafpro = models.DateTimeField(db_column='MAFPro', blank=True, null=True)  # Field name made lowercase.
    mahpro = models.CharField(db_column='MAHPro', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mpdi1s = models.CharField(db_column='MPDi1S', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mpdi2s = models.CharField(db_column='MPDi2S', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mpdi3s = models.CharField(db_column='MPDi3S', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mpcaue = models.SmallIntegerField(db_column='MPCAUE', blank=True, null=True)  # Field name made lowercase.
    mptipd = models.SmallIntegerField(db_column='MPTIPD', blank=True, null=True)  # Field name made lowercase.
    macanpr = models.IntegerField(db_column='MaCanPr', blank=True, null=True)  # Field name made lowercase.
    mpinte = models.DecimalField(db_column='MPInte', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mpopcn = models.SmallIntegerField(db_column='MPOpcn', blank=True, null=True)  # Field name made lowercase.
    mpvias = models.SmallIntegerField(db_column='MPVias', blank=True, null=True)  # Field name made lowercase.
    mpespe = models.SmallIntegerField(db_column='MPEspe', blank=True, null=True)  # Field name made lowercase.
    mpngrp = models.CharField(db_column='MPNGrp', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mpcodi = models.CharField(db_column='MPCodi', max_length=9, blank=True, null=True)  # Field name made lowercase.
    mppcso = models.CharField(db_column='MPpcso', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mpphome = models.DecimalField(db_column='MPpHoMe', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mppinte = models.DecimalField(db_column='MPpInte', max_digits=13, decimal_places=9, blank=True, null=True)  # Field name made lowercase.
    mptipd2 = models.SmallIntegerField(db_column='MPTipD2', blank=True, null=True)  # Field name made lowercase.
    mptipd3 = models.SmallIntegerField(db_column='MPTipD3', blank=True, null=True)  # Field name made lowercase.
    mpvlruvr = models.IntegerField(db_column='MPVLRUVR', blank=True, null=True)  # Field name made lowercase.
    mpuvrcod = models.CharField(db_column='MPUVRCOD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mptpco = models.SmallIntegerField(db_column='MPTpco', blank=True, null=True)  # Field name made lowercase.
    mptpmo = models.SmallIntegerField(db_column='MPTPMo', blank=True, null=True)  # Field name made lowercase.
    mpmhome = models.CharField(db_column='MPmHoMe', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mpvrpu = models.DecimalField(max_digits=17, decimal_places=2, blank=True, null=True)
    mpftrv = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    mpfina = models.CharField(db_column='MPFINA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mppndct = models.CharField(db_column='MPPNDCT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mpncita = models.IntegerField(db_column='MPNCITA', blank=True, null=True)  # Field name made lowercase.
    mpriad = models.SmallIntegerField(db_column='MPRiad', blank=True, null=True)  # Field name made lowercase.
    fcpcodccs = models.CharField(db_column='FcPCodCCs', max_length=9, blank=True, null=True)  # Field name made lowercase.
    fcpcodscc = models.CharField(db_column='FCPCodSCC', max_length=9, blank=True, null=True)  # Field name made lowercase.
    fcptpotrn = models.CharField(db_column='FcPTpoTrn', max_length=1, blank=True, null=True)  # Field name made lowercase.
    manumfol = models.DecimalField(db_column='MaNumFol', max_digits=11, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mausuanl = models.CharField(db_column='MaUsuAnl', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maagrcir = models.IntegerField(db_column='MaAgrCir', blank=True, null=True)  # Field name made lowercase.
    maempcod = models.CharField(db_column='MaEmpCod', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mavlrtot = models.DecimalField(db_column='MaVlrTot', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    manoma = models.CharField(db_column='MaNomA', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mafchreg = models.DateTimeField(db_column='MaFchReg', blank=True, null=True)  # Field name made lowercase.
    maordliq = models.SmallIntegerField(db_column='MaOrdLiq', blank=True, null=True)  # Field name made lowercase.
    maporimpt = models.DecimalField(db_column='MaPorImpt', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    macanpe = models.IntegerField(db_column='MaCanPe', blank=True, null=True)  # Field name made lowercase.
    macnsaqx = models.SmallIntegerField(db_column='MaCnsAQx', blank=True, null=True)  # Field name made lowercase.
    macodpab = models.SmallIntegerField(db_column='MaCodPab', blank=True, null=True)  # Field name made lowercase.
    macodcam = models.CharField(db_column='MaCodCam', max_length=5, blank=True, null=True)  # Field name made lowercase.
    maesparxto = models.SmallIntegerField(db_column='MaEsParXTo', blank=True, null=True)  # Field name made lowercase.
    maesanup = models.CharField(db_column='MaEsAnuP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    macoreca = models.CharField(db_column='MaCoReca', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maconpr = models.SmallIntegerField(db_column='MaConPr', blank=True, null=True)  # Field name made lowercase.
    maindcop = models.CharField(db_column='MaIndCop', max_length=1, blank=True, null=True)  # Field name made lowercase.
    macodcir = models.IntegerField(db_column='MaCodCir', blank=True, null=True)  # Field name made lowercase.
    macodpar = models.IntegerField(db_column='MaCodPar', blank=True, null=True)  # Field name made lowercase.
    maespanup = models.CharField(db_column='MaEsPAnuP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    manumaue = models.IntegerField(db_column='MaNumAuE', blank=True, null=True)  # Field name made lowercase.
    mactvent = models.DecimalField(db_column='MaCtvEnt', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mapppcod = models.CharField(db_column='MaPPPCod', max_length=9, blank=True, null=True)  # Field name made lowercase.
    macanca = models.IntegerField(db_column='MaCanCa', blank=True, null=True)  # Field name made lowercase.
    maordman = models.CharField(db_column='MaOrdMan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    macodcon = models.CharField(db_column='MACodCon', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mapcaue = models.SmallIntegerField(db_column='MAPCauE', blank=True, null=True)  # Field name made lowercase.
    macscsagr = models.IntegerField(db_column='MaCscSAgr', blank=True, null=True)  # Field name made lowercase.
    mapvlrsiv = models.DecimalField(db_column='MapVlrSIv', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mapporiva = models.DecimalField(db_column='MapPorIva', max_digits=12, decimal_places=9, blank=True, null=True)  # Field name made lowercase.
    maecodpqt = models.CharField(db_column='MAECODPQT', max_length=9, blank=True, null=True)  # Field name made lowercase.
    matipliqp = models.CharField(db_column='MATIPLIQP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maprodsc = models.DecimalField(db_column='MAPRODSC', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mffchanu1 = models.DateTimeField(db_column='MFFchAnu1', blank=True, null=True)  # Field name made lowercase.
    macodanup = models.CharField(db_column='MaCodAnuP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mpcodfina = models.CharField(db_column='MPCODFINA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    maimpprc = models.DecimalField(db_column='MAIMPPRC', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    macodimpp = models.CharField(db_column='MACODIMPP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    maetent = models.DecimalField(db_column='MAEtEnT', max_digits=1, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mapcodhom = models.CharField(db_column='MAPCODHOM', max_length=9, blank=True, null=True)  # Field name made lowercase.
    mapctepaq = models.IntegerField(db_column='MAPCTEPAQ', blank=True, null=True)  # Field name made lowercase.
    mapcnspaq = models.DecimalField(db_column='MAPCNSPAQ', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mapidmipr = models.CharField(db_column='MAPIDMIPR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mapautpro = models.CharField(db_column='MAPAUTPRO', max_length=255, blank=True, null=True)  # Field name made lowercase.
    codmate = models.SmallIntegerField(db_column='CodMAte', blank=True, null=True)  # Field name made lowercase.
    mservcod = models.SmallIntegerField(db_column='MServCod', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAEATE2'

