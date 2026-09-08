from django.db import models


class Maeate(models.Model):
    pk = models.CompositePrimaryKey('MPNFac', 'MATipDoc')
    mpnfac = models.DecimalField(db_column='MPNFac', max_digits=15, decimal_places=0)  # Field name made lowercase.
    matipdoc = models.DecimalField(db_column='MATipDoc', max_digits=15, decimal_places=0)  # Field name made lowercase.
    facdscprf = models.CharField(db_column='FacDscPrf', max_length=7, blank=True, null=True)  # Field name made lowercase.
    mpcedu = models.ForeignKey('Maepac', models.DO_NOTHING, db_column='MPCedu', to_field='MPTDoc', blank=True, null=True)  # Field name made lowercase.
    mptdoc = models.ForeignKey('Tipdocasi', models.DO_NOTHING, db_column='MPTDoc', blank=True, null=True)  # Field name made lowercase.
    mpclpr = models.CharField(db_column='MPClPr', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mpmeni = models.ForeignKey('Maepac', models.DO_NOTHING, db_column='MPMeNi', to_field='MPTDoc', related_name='maeate_mpmeni_set', blank=True, null=True)  # Field name made lowercase.
    mafchi = models.DateTimeField(db_column='MAFchI', blank=True, null=True)  # Field name made lowercase.
    mahori = models.CharField(db_column='MAHorI', max_length=8, blank=True, null=True)  # Field name made lowercase.
    maviai = models.SmallIntegerField(db_column='MAViaI', blank=True, null=True)  # Field name made lowercase.
    madi1i = models.CharField(db_column='MADi1I', max_length=7, blank=True, null=True)  # Field name made lowercase.
    madi2i = models.CharField(db_column='MADi2I', max_length=7, blank=True, null=True)  # Field name made lowercase.
    madi3i = models.CharField(db_column='MADi3I', max_length=7, blank=True, null=True)  # Field name made lowercase.
    mamein = models.CharField(db_column='MAMeIn', max_length=5, blank=True, null=True)  # Field name made lowercase.
    maesmi = models.SmallIntegerField(db_column='MAEsMI', blank=True, null=True)  # Field name made lowercase.
    maesms = models.SmallIntegerField(db_column='MAEsMS', blank=True, null=True)  # Field name made lowercase.
    mameeg = models.CharField(db_column='MaMeEg', max_length=5, blank=True, null=True)  # Field name made lowercase.
    madi1s = models.CharField(db_column='MADi1S', max_length=7, blank=True, null=True)  # Field name made lowercase.
    madi2s = models.CharField(db_column='MADi2S', max_length=7, blank=True, null=True)  # Field name made lowercase.
    madi3s = models.CharField(db_column='MaDi3S', max_length=7, blank=True, null=True)  # Field name made lowercase.
    masege = models.SmallIntegerField(db_column='MASeGe', blank=True, null=True)  # Field name made lowercase.
    macopr = models.CharField(db_column='MACoPr', max_length=1, blank=True, null=True)  # Field name made lowercase.
    matipa = models.CharField(db_column='MATiPa', max_length=1, blank=True, null=True)  # Field name made lowercase.
    matian = models.CharField(db_column='MATiAn', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mafchm = models.DateTimeField(db_column='MAFchM', blank=True, null=True)  # Field name made lowercase.
    macamu = models.CharField(db_column='MACaMu', max_length=7, blank=True, null=True)  # Field name made lowercase.
    maquia = models.CharField(db_column='MAQuiA', max_length=5, blank=True, null=True)  # Field name made lowercase.
    maests = models.SmallIntegerField(db_column='MAEstS', blank=True, null=True)  # Field name made lowercase.
    macaue = models.SmallIntegerField(db_column='MACauE', blank=True, null=True)  # Field name made lowercase.
    maccom = models.CharField(db_column='MACCom', max_length=7, blank=True, null=True)  # Field name made lowercase.
    maestp = models.SmallIntegerField(db_column='MAEstP', blank=True, null=True)  # Field name made lowercase.
    mamots = models.CharField(db_column='MAMotS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mafche = models.DateTimeField(db_column='MAFchE', blank=True, null=True)  # Field name made lowercase.
    mahore = models.CharField(db_column='MAHorE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mahoro = models.SmallIntegerField(db_column='MAHorO', blank=True, null=True)  # Field name made lowercase.
    mafchs = models.DateTimeField(db_column='MAFchS', blank=True, null=True)  # Field name made lowercase.
    macmad = models.CharField(db_column='MACMAD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    matotp = models.DecimalField(db_column='MATotP', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    matots = models.DecimalField(db_column='MATotS', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    micodi = models.IntegerField(db_column='MICodI', blank=True, null=True)  # Field name made lowercase.
    matotf = models.DecimalField(db_column='MATotF', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mavals = models.DecimalField(db_column='MAValS', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mavaab = models.DecimalField(db_column='MAVaAb', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mavapu = models.DecimalField(db_column='MAVAPU', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mavpau = models.DecimalField(db_column='MAVPaU', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mavdsc = models.DecimalField(db_column='MAVDsc', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mavnpu = models.DecimalField(db_column='MAVNPU', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maulcn = models.SmallIntegerField(db_column='MAUlCN', blank=True, null=True)  # Field name made lowercase.
    maulcp = models.IntegerField(db_column='MAUlCP', blank=True, null=True)  # Field name made lowercase.
    maulcs = models.IntegerField(db_column='MAUlCS', blank=True, null=True)  # Field name made lowercase.
    maccfc = models.SmallIntegerField(db_column='MACCFC', blank=True, null=True)  # Field name made lowercase.
    msuing = models.CharField(db_column='MSUIng', max_length=10, blank=True, null=True)  # Field name made lowercase.
    msusal = models.CharField(db_column='MSUSal', max_length=10, blank=True, null=True)  # Field name made lowercase.
    msufac = models.CharField(db_column='MSUFac', max_length=10, blank=True, null=True)  # Field name made lowercase.
    msuafa = models.CharField(db_column='MSUAFa', max_length=10, blank=True, null=True)  # Field name made lowercase.
    macoan = models.CharField(db_column='MACoAn', max_length=10, blank=True, null=True)  # Field name made lowercase.
    maestf = models.SmallIntegerField(db_column='MAEstF', blank=True, null=True)  # Field name made lowercase.
    mpfria = models.SmallIntegerField(db_column='MPFria', blank=True, null=True)  # Field name made lowercase.
    mpnuma = models.CharField(db_column='MPnuma', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mafcfa = models.IntegerField(db_column='MAFCFA', blank=True, null=True)  # Field name made lowercase.
    mptucod = models.CharField(db_column='MPTUCod', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mptcodp = models.CharField(db_column='MPTCodP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mpptcodi = models.CharField(db_column='MPPTCodi', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mpcsubp = models.SmallIntegerField(db_column='MPCSubP', blank=True, null=True)  # Field name made lowercase.
    mpmsubp = models.SmallIntegerField(db_column='MPMSubP', blank=True, null=True)  # Field name made lowercase.
    maviva = models.DecimalField(db_column='MAViva', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    maidpc = models.CharField(db_column='MAIDPC', max_length=60, blank=True, null=True)  # Field name made lowercase.
    mafces = models.DateTimeField(db_column='MAFCES', blank=True, null=True)  # Field name made lowercase.
    mpnume = models.CharField(db_column='MPNume', max_length=14, blank=True, null=True)  # Field name made lowercase.
    mpcomp = models.CharField(db_column='MPComp', max_length=30, blank=True, null=True)  # Field name made lowercase.
    facfch = models.DateTimeField(db_column='FacFch', blank=True, null=True)  # Field name made lowercase.
    manomaut = models.CharField(db_column='MANomAut', max_length=30, blank=True, null=True)  # Field name made lowercase.
    matpeaut = models.DecimalField(db_column='MATpeAut', max_digits=10, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    mavlraut = models.DecimalField(db_column='MAVlrAut', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    macpgpgo = models.CharField(db_column='MACpgPgo', max_length=1, blank=True, null=True)  # Field name made lowercase.
    macpglqd = models.CharField(db_column='MaCpgLqd', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scccod = models.CharField(db_column='SCCCod', max_length=9, blank=True, null=True)  # Field name made lowercase.
    sccemp = models.CharField(db_column='SccEmp', max_length=2, blank=True, null=True)  # Field name made lowercase.
    faccodpab = models.SmallIntegerField(db_column='FacCodPab', blank=True, null=True)  # Field name made lowercase.
    faccodcam = models.CharField(db_column='FacCodCam', max_length=5, blank=True, null=True)  # Field name made lowercase.
    turcod = models.DecimalField(db_column='TurCod', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    facsnume = models.CharField(db_column='FacSNume', max_length=20, blank=True, null=True)  # Field name made lowercase.
    facsnitasg = models.CharField(db_column='FacSNitAsg', max_length=15, blank=True, null=True)  # Field name made lowercase.
    facsfchvin = models.DateTimeField(db_column='FacSFchVIn', blank=True, null=True)  # Field name made lowercase.
    facsvepl = models.CharField(db_column='FacSVePl', max_length=10, blank=True, null=True)  # Field name made lowercase.
    facsvema = models.CharField(db_column='FacSVeMa', max_length=20, blank=True, null=True)  # Field name made lowercase.
    facsveti = models.CharField(db_column='FacSVeTi', max_length=20, blank=True, null=True)  # Field name made lowercase.
    facsvemo = models.CharField(db_column='FacSVeMo', max_length=2, blank=True, null=True)  # Field name made lowercase.
    facsvecl = models.CharField(db_column='FacSVeCl', max_length=20, blank=True, null=True)  # Field name made lowercase.
    facscndacc = models.CharField(db_column='FacSCndAcc', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facssitacc = models.CharField(db_column='FacSSitAcc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    facsfchacc = models.DateTimeField(db_column='FacSFchAcc', blank=True, null=True)  # Field name made lowercase.
    facscodd = models.CharField(db_column='FacSCodD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    facscodm = models.IntegerField(db_column='FacSCodM', blank=True, null=True)  # Field name made lowercase.
    facsrulurb = models.CharField(db_column='FacSRulUrb', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facsindasg = models.CharField(db_column='FacSIndAsg', max_length=1, blank=True, null=True)  # Field name made lowercase.
    facsfchvfi = models.DateTimeField(db_column='FacSFchVFi', blank=True, null=True)  # Field name made lowercase.
    facstpicnd = models.CharField(db_column='FacSTpICnd', max_length=3, blank=True, null=True)  # Field name made lowercase.
    facscedcnd = models.CharField(db_column='FacSCedCnd', max_length=15, blank=True, null=True)  # Field name made lowercase.
    facsnomcnd = models.CharField(db_column='FacSNomCnd', max_length=73, blank=True, null=True)  # Field name made lowercase.
    facsmcodfc = models.CharField(db_column='FacSMCodFC', max_length=5, blank=True, null=True)  # Field name made lowercase.
    facsnomsuc = models.CharField(db_column='FacSNomSuc', max_length=45, blank=True, null=True)  # Field name made lowercase.
    facstpoec = models.SmallIntegerField(db_column='FacSTpoEC', blank=True, null=True)  # Field name made lowercase.
    facsdesec = models.CharField(db_column='FacSDesEC', max_length=50, blank=True, null=True)  # Field name made lowercase.
    facsnomemp = models.CharField(db_column='FacSNomEmp', max_length=45, blank=True, null=True)  # Field name made lowercase.
    facscodde = models.CharField(db_column='FacSCodDE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    facscodme = models.IntegerField(db_column='FacSCodME', blank=True, null=True)  # Field name made lowercase.
    facscoddcn = models.CharField(db_column='FacSCodDCn', max_length=2, blank=True, null=True)  # Field name made lowercase.
    facscodmcn = models.IntegerField(db_column='FacSCodMCn', blank=True, null=True)  # Field name made lowercase.
    malugexp = models.CharField(db_column='MaLugExp', max_length=30, blank=True, null=True)  # Field name made lowercase.
    madocdcl = models.CharField(db_column='MaDocDcl', max_length=11, blank=True, null=True)  # Field name made lowercase.
    madecla = models.CharField(db_column='MaDecla', max_length=73, blank=True, null=True)  # Field name made lowercase.
    maluexcnd = models.CharField(db_column='MaLuExCnd', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mainfacc = models.TextField(db_column='MaInfAcc', blank=True, null=True)  # Field name made lowercase.
    madircnd = models.CharField(db_column='MaDirCnd', max_length=50, blank=True, null=True)  # Field name made lowercase.
    matelcnd = models.CharField(db_column='MaTelCnd', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mactving = models.SmallIntegerField(db_column='MaCtvIng', blank=True, null=True)  # Field name made lowercase.
    matidodc = models.CharField(db_column='MaTiDoDc', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mavlrimpt = models.DecimalField(db_column='MaVlrImpt', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    manrnotcr = models.DecimalField(db_column='MaNrNotCr', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mafchnot = models.DateTimeField(db_column='MaFchNot', blank=True, null=True)  # Field name made lowercase.
    maestnot = models.CharField(db_column='MaEstNot', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maucnaqx = models.SmallIntegerField(db_column='MaUCnAqx', blank=True, null=True)  # Field name made lowercase.
    maultcci = models.IntegerField(db_column='MaUltCci', blank=True, null=True)  # Field name made lowercase.
    manrcerd = models.CharField(db_column='MaNrCerD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    maubifac = models.CharField(db_column='MaUbiFac', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mausufac = models.CharField(db_column='MaUsuFac', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mactvact = models.SmallIntegerField(db_column='MaCtvAct', blank=True, null=True)  # Field name made lowercase.
    mainddev = models.CharField(db_column='MaIndDev', max_length=1, blank=True, null=True)  # Field name made lowercase.
    maestenv = models.CharField(db_column='MaEstEnv', max_length=2, blank=True, null=True)  # Field name made lowercase.
    maestcan = models.CharField(db_column='MaEstCan', max_length=1, blank=True, null=True)  # Field name made lowercase.
    masalcxc = models.DecimalField(db_column='MaSalCXC', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    maclsdoc = models.CharField(db_column='MaClsDoc', max_length=2, blank=True, null=True)  # Field name made lowercase.
    maobsfac = models.TextField(db_column='MaObsFac', blank=True, null=True)  # Field name made lowercase.
    macodcaj = models.CharField(db_column='MaCodCaj', max_length=5, blank=True, null=True)  # Field name made lowercase.
    madocfac = models.CharField(db_column='MaDocFac', max_length=3, blank=True, null=True)  # Field name made lowercase.
    masedpun = models.CharField(db_column='MaSedPun', max_length=9, blank=True, null=True)  # Field name made lowercase.
    mavpocon = models.DecimalField(db_column='MaVPOCon', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mavlrtiv = models.DecimalField(db_column='MaVlrTIv', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    matipfagr = models.DecimalField(db_column='MaTipFAgr', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    manumfagr = models.DecimalField(db_column='MaNumFAgr', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    matipope = models.IntegerField(db_column='MaTipOpe', blank=True, null=True)  # Field name made lowercase.
    facfchhor = models.CharField(db_column='FacFchHor', max_length=8, blank=True, null=True)  # Field name made lowercase.
    maconcap = models.TextField(db_column='MACONCAP', blank=True, null=True)  # Field name made lowercase.
    maecodpaq = models.CharField(db_column='MAECODPAQ', max_length=9, blank=True, null=True)  # Field name made lowercase.
    madi4s = models.CharField(db_column='MADI4S', max_length=7, blank=True, null=True)  # Field name made lowercase.
    matipter = models.CharField(db_column='MATIPTER', max_length=3, blank=True, null=True)  # Field name made lowercase.
    macodter = models.CharField(db_column='MACODTER', max_length=15, blank=True, null=True)  # Field name made lowercase.
    maclafac = models.CharField(db_column='MACLAFAC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    idprc0010 = models.BigIntegerField(db_column='IDPRC0010', blank=True, null=True)  # Field name made lowercase.
    maecodved = models.CharField(db_column='MAECODVED', max_length=10, blank=True, null=True)  # Field name made lowercase.
    manumpgp = models.CharField(db_column='MANUMPGP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    maea_id = models.CharField(db_column='MAEA_ID', max_length=36, blank=True, null=True)  # Field name made lowercase.
    mavalbas = models.DecimalField(db_column='MAVALBAS', max_digits=17, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mapopla = models.CharField(db_column='MaPoPla', max_length=100, blank=True, null=True)  # Field name made lowercase.
    marfacres = models.CharField(db_column='MarFacRes', max_length=1)  # Field name made lowercase.
    facncdoc = models.CharField(db_column='FacNCDoc', max_length=3, blank=True, null=True)  # Field name made lowercase.
    facncprf = models.CharField(db_column='FacNCPrf', max_length=7, blank=True, null=True)  # Field name made lowercase.
    maerecpag = models.CharField(db_column='MAERECPAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    preplacns = models.DecimalField(db_column='PrePlaCns', max_digits=15, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MAEATE'