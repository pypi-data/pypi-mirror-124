#改模块配置了django的环境，必须比models先引用
import os,django
from django.conf import settings
from rest_framework.utils import model_meta
from django.db import connection


def add_sql_description(table_name,description,column_name=None):
    table_str="INNER JOIN sys.columns AS c ON t.object_id = c.object_id" if bool(column_name) else ""
    join_str=" AND ep.minor_id = c.column_id " if bool(column_name) else " and ep.minor_id=0 "
    where_str=f"AND C.name= '{column_name}'" if bool(column_name) else ""
    update_str=f""",@level2type = N'Column', @level2name = '{column_name}'""" if bool(column_name) else ""

    sql_str=f"""
IF EXISTS(
SELECT top 1 1
FROM sys.tables AS t
{table_str}
inner JOIN sys.extended_properties AS ep
ON ep.major_id = t.object_id  {join_str} and ep.class =1
WHERE 1=1
AND t.name='{table_name}' 
{where_str}
AND EP.class=1
)
BEGIN
EXEC sp_updateextendedproperty   
@name = N'MS_Description',   
@value = '{description}',  
@level0type = N'Schema', @level0name = 'dbo',  
@level1type = N'Table',  @level1name = '{table_name}'  
{update_str};
END
ELSE
BEGIN
EXEC sp_addextendedproperty   
@name = N'MS_Description',   
@value = '{description}',  
@level0type = N'Schema', @level0name = 'dbo',  
@level1type = N'Table',  @level1name = '{table_name}'
{update_str};
END
 
"""
    # print(sql_str)
    with connection.cursor() as cursor:
        cursor.execute(sql_str)
    

def update_model_description(models):
    data_list=[]
    for key in dir(models):
        model=getattr(models,key)
        try:
            if type(model)==django.db.models.base.ModelBase:
                model_name=key
                model=model
                table_name=model._meta.db_table
                row_dict={"table_name":model._meta.db_table,"field_name":None,"verbose_name":model._meta.verbose_name}
                data_list.append(row_dict)
                model_info=model_meta.get_field_info(model)
                for field_name in model_info.fields:
                    verbose_name=model_info.fields[field_name].verbose_name
                    if model_info.fields[field_name].db_column:
                        db_column=model_info.fields[field_name].db_column
                    else:
                        db_column=model_info.fields[field_name].column
                    row_dict={"table_name":model_info.fields[field_name].model_field.model._meta.db_table,"field_name":db_column,"verbose_name":verbose_name}
                    data_list.append(row_dict)
                for field_name in model_info.forward_relations:
                    verbose_name=model_info.forward_relations[field_name].model_field.verbose_name
                    if model_info.forward_relations[field_name].model_field.db_column:
                        db_column=model_info.forward_relations[field_name].model_field.db_column
                    else:
                        db_column=model_info.forward_relations[field_name].model_field.column  
                    row_dict={"table_name":model_info.forward_relations[field_name].model_field.model._meta.db_table,"field_name":db_column,"verbose_name":verbose_name}              
                    data_list.append(row_dict)
        except:
            pass

    for row_dict in data_list:
        print("正在更新:",row_dict)
        try:
            add_sql_description(row_dict["table_name"],row_dict["verbose_name"],row_dict["field_name"])
        except Exception as error:
            print(error)
    print("更新成功")
    

def update_ms_description(django_core="django_core"):
# 加载django配置
    setting_model_str=f"{django_core}.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_model_str)
    django.setup()
    system_apps=['corsheaders','django_extend', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'rest_framework', 'rest_framework.authtoken', 'django_filters']

    install_apps=settings.INSTALLED_APPS

    user_apps=[app for app in install_apps if app not in system_apps]

    for app in user_apps:
        # print(app)
        app_update = __import__(app)
        update_model_description(app_update.models)