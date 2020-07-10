from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class HL7_MESSAGE_LOGS(models.Model):
    # MESSAGE_ID = models.AutoField('消息ID',primary_key=True)
    MESSAGE_BODY= models.CharField('消息主体',max_length=10000, blank=True, default='')
    ACTION_NAME= models.CharField('消息类型',max_length=100, blank=True, default='')
    CREATE_USER= models.CharField('创建人',max_length=100, blank=True, default='')
    CREATE_DATE= models.DateTimeField('创建日期',auto_now_add=True)
    PATIENT_ID= models.CharField('患者ID',max_length=100, blank=True, default='')
    VISIT_ID= models.CharField('住院次',max_length=100, blank=True, default='')
    INP_NO= models.CharField('住院流水号',max_length=100, blank=True, default='')
    ORDER_NO= models.CharField('医嘱主键',max_length=100, blank=True, default='')
    RESULT= models.CharField('处理结果（0：成功  1：失败）',max_length=100, blank=True, default='')
    class Meta:
        ordering = ('CREATE_DATE', )


class JHNIS_CARE_MAIN(models.Model):
    CARE_MAIN_INDEX = models.AutoField('护理主索引',primary_key=True)
    APPLY_ID = models.IntegerField( '该患者是否已经归档', blank=False, null=False, default=0)
    PATIENT_ID= models.CharField('病案号',max_length=100, blank=True, default='')
    VISIT_ID = models.IntegerField( '患者住院次', blank=False, null=False, default=0)
    INP_NO= models.CharField('住院号',max_length=100, blank=True, default='')
    HOSPITAL_NO= models.CharField('医院编码',max_length=100, blank=True, default='')
    BED_ID=  models.IntegerField( '床位ID', blank=False, null=False, default=-1)
    CREATE_USER= models.CharField('创建人',max_length=100, blank=True, default='')
    CREATE_DATE= models.DateTimeField('创建日期',auto_now_add=True)
    IN_DEPT_DATE= models.DateTimeField('入科日期')
    OUT_DEPT_DATE= models.DateTimeField('出科日期', blank=False, null=False)
    STATE = models.IntegerField( '是否有效（0：有效 1：无效）', blank=False, null=False, default=0)
    DOCTOR= models.CharField('住院号',max_length=100, blank=True, default='')
    DEPT_CODE= models.CharField('住院号',max_length=100, blank=True, default='')

    class Meta:
        ordering = ('CARE_MAIN_INDEX', )



