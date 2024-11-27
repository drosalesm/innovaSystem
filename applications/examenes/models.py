from django.db import models


class examen_off(models.Model):
    paciente =models.CharField(max_length=500,verbose_name="paciente")


TIPOSANGRE_CHOICES=(
    ('0','A positivo (A +)'),
    ('1','A negativo (A-)'),    
    ('2','B positivo (B +)'),
    ('4','B negativo (B-)'),
    ('5','AB positivo (AB+)'),    
    ('6','AB negativo (AB-)'),
    ('7','O positivo (O+)'),    
    ('8','O negativo (O-)'),
)


OPT_PREG=(
    ('1.85','Si'),
    ('1.07','No'),    
)

class examen_med(models.Model):
    paciente =models.CharField(max_length=500,verbose_name="paciente")
    nombre_orden = models.CharField(max_length=100,verbose_name="Nombre de la Orden")
    cod_orden=models.IntegerField(verbose_name='Orden',blank=True,null=True)
    fecha=models.DateField(null=True)
    dir_pac=models.CharField(max_length=500,verbose_name="Direccion",null=True)
    documento = models.FileField(null=True)
    identif_pac=models.CharField(max_length=500,verbose_name="Identificacion",null=True)
    t_sangre=models.CharField(max_length=200,verbose_name="Tipo de Sangre",null=True,choices=TIPOSANGRE_CHOICES)
    altura=models.FloatField(verbose_name="Altura",null=True)
    peso=models.FloatField(verbose_name="Peso",null=True)
    p_alterial=models.FloatField(verbose_name="P.Arterial",null=True)
    temperatura=models.FloatField(verbose_name="Temperatura",null=True)
    imc=models.FloatField(verbose_name="Mbi",null=True)
    f_r=models.FloatField(verbose_name="r/m",null=True)
    p_a=models.FloatField(verbose_name="mmHG",null=True)
    f_c=models.FloatField(verbose_name="f.c",null=True)
    i_card=models.CharField(max_length=5,blank=True,null=True)
    t_rit=models.CharField(max_length=5,blank=True,null=True) 
    m_desf=models.CharField(max_length=5,blank=True ,null=True) 
    p_val=models.CharField(max_length=5,blank=True,null=True)         
    hi_art=models.CharField(max_length=5,blank=True,null=True) 
    a_gra_va=models.CharField(max_length=5,blank=True,null=True) 
    a_per=models.CharField(max_length=5,blank=True,null=True)
    disnea=models.CharField(max_length=5,blank=True,null=True)
    t_sue=models.CharField(max_length=5,blank=True,null=True)
    o_aff=models.CharField(max_length=5,blank=True,null=True)
    d_melitus=models.CharField(max_length=5,blank=True,null=True)
    c_hip=models.CharField(max_length=5,blank=True,null=True)
    e_tir=models.CharField(max_length=5,blank=True,null=True) 
    e_adre=models.CharField(max_length=5,blank=True,null=True) 
    a_alcohol=models.CharField(max_length=5,blank=True,null=True)
    d_alcohol=models.CharField(max_length=5,blank=True,null=True)
    c_hdalc=models.CharField(max_length=5,blank=True,null=True)
    e_par=models.CharField(max_length=5,blank=True,null=True)
    t_hep=models.CharField(max_length=5,blank=True,null=True)
    p_vera=models.CharField(max_length=5,blank=True,null=True)
    a_leu_tromp=models.CharField(max_length=5,blank=True,null=True)
    t_org=models.CharField(max_length=5,blank=True,null=True)
    neurop=models.CharField(max_length=5,blank=True,null=True) 
    tra_org=models.CharField(max_length=5,blank=True,null=True) 
    o_enfer=models.CharField(max_length=5,blank=True,null=True)
    sis_n_vas=models.CharField(max_length=5,blank=True,null=True)
    e_enc_conv=models.CharField(max_length=5,blank=True,null=True)
    e_cris_conv=models.CharField(max_length=5,blank=True,null=True)
    alt_equ=models.CharField(max_length=5,blank=True,null=True)
    tras_musc=models.CharField(max_length=5,blank=True,null=True)
    ac_isq_trans=models.CharField(max_length=5,blank=True,null=True)
    acc_isq_rec=models.CharField(max_length=5,blank=True,null=True)
    glucometria=models.CharField(max_length=5,blank=True,null=True) 
    pre_mar=models.CharField(max_length=5,blank=True,null=True)
    diagnostico=models.TextField(max_length=500,verbose_name="Diagnostico General",null=True)
#campos del examen psicologico:
    Ag_vis_L_OD=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    Ag_vis_L_OI=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    Ag_vis_L_AM_OJ=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    Ag_vis_C_OD=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    Ag_vis_C_OI=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    Ag_vis_C_AM_OJ=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    vis_noc=models.IntegerField(verbose_name='20/30',blank=True,null=True)
    cam_vis_v_iz=models.IntegerField(verbose_name='°70',blank=True,null=True)
    cam_vis_v_de=models.IntegerField(verbose_name='°70',blank=True,null=True)
    cam_vis_h_iz=models.IntegerField(verbose_name='°120',blank=True,null=True)
    cam_vis_h_de=models.IntegerField(verbose_name='°120',blank=True,null=True)
    cam_vis_bin_hor=models.IntegerField(verbose_name='°120',blank=True,null=True)
    vis_prof_lej=models.IntegerField(verbose_name='°60',blank=True,null=True)
    vis_prof_cer=models.IntegerField(verbose_name='°60',blank=True,null=True)
    Disc_Col=models.IntegerField(verbose_name='4.Num',blank=True,null=True)
    Sens_Cont=models.IntegerField(verbose_name='50%',blank=True,null=True)
    Recup_Enc=models.IntegerField(verbose_name='',blank=True,null=True)
    Phor_Hor_Lej=models.IntegerField(verbose_name='',blank=True,null=True)
    Phor_Ver_Lej=models.IntegerField(verbose_name='',blank=True,null=True)
    Phor_Hor_Cer=models.IntegerField(verbose_name='',blank=True,null=True)
    Phor_Ver_Cer=models.IntegerField(verbose_name='',blank=True,null=True)
    diagPsi=models.TextField(max_length=500,verbose_name="Diagnostico Visual",blank=True,null=True)
    doctor= models.CharField(max_length=100,blank=True,null=True, verbose_name='Atendido por')


class examen_psi(models.Model):
    id_orden=models.IntegerField(verbose_name='Numero de Orden',blank=True,null=True)
    paciente =models.CharField(max_length=500,verbose_name="paciente")
    nombre_orden = models.CharField(max_length=100,verbose_name="Nombre de la Orden")
    fecha=models.DateField(null=True)
    dir_pac=models.CharField(max_length=500,verbose_name="Direccion",null=True)
    documento = models.FileField(null=True)
    identif_pac=models.CharField(max_length=500,verbose_name="Identificacion",null=True)
#item delirium
    items_del_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_del_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_del_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_del_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_del_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems a evaluar Demencia
    items_dem_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dem_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dem_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dem_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dem_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos amnésicos y trastornos cognitivos
    items_trans_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos mentales debido a enfermedades medicas no clasificadas
    items_trans_m_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_m_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_m_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_m_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_m_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar esquizofrenia y otros trastornos psicóticos
    items_ezq_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_ezq_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_ezq_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_ezq_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_ezq_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos del estado de animo
    items_transt_a_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_transt_a_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_transt_a_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_transt_a_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_transt_a_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos disociativos
    items_dis_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dis_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dis_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dis_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_dis_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos del sueño de origen diferente al respiratorio
    items_trans_sue_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_sue_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_sue_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_sue_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_sue_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos del control de impulsos
    items_t_imp_a_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_imp_a_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_imp_a_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_imp_a_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_imp_a_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
# Ítems para evaluar trastornos de la personalidad
    items_t_pers_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_pers_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_pers_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_pers_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_pers_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastorno del desarrollo intelectual
    items_trans_dint_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_dint_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_dint_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_dint_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_trans_dint_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar trastornos por déficit de atención
    items_t_datt_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_datt_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_datt_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_datt_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_t_datt_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
#Ítems para evaluar comportamiento perturbador
    items_com_per_one=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_com_per_two=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_com_per_thre=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_com_per_four=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    items_com_per_five=models.CharField(max_length=10,verbose_name="",null=True,choices=OPT_PREG)
    doctor= models.CharField(max_length=100,blank=True,null=True, verbose_name='Atendido por')
