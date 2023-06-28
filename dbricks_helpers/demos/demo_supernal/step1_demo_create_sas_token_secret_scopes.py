# Databricks notebook source
# DBTITLE 1,Get Secret Scope Base Functions and Libraries
# MAGIC %run "../../databricks_secret_scope/secret_scope_base"

# COMMAND ----------

# DBTITLE 1,Supernal Variable Declarations
method = "storageaccount" # or adlsgen2

#-------------------------------------NON ADLS GEN 2 METHOD-----------------------------------

if method == "storageaccount":
    
    # ft = flight tech secret scope variables
    scope_name_ft = "flight_tech_secretscope"
    secret_name_ft = "flight-tech-sas-token-dbfsfiles"
    secret_value_ft = "?si=dbfsfilespolicy&spr=https&sv=2022-11-02&sr=c&sig=IFKbYRjZhCxVHvMNfOT%2FQDn5HE5QX1hUpFtCObNPljM%3D" # regular storage account --> container level (dbfs-files)

    # autnav = autonomy / navigation secret scope variables
    scope_name_autnav = "autonomy_nav_secretscope"
    secret_name_autnav = "autonomy-nav-sas-token-dbfsfilesnav"
    secret_value_autnav = "?si=dbfsfilesnavpolicy&spr=https&sv=2022-11-02&sr=c&sig=DyCTY1HUK2L0Bhl5JLo8K9MUWXdIPFjJu%2BcdrFiLx4c%3D" # regular storage account --> container level (dbfs-files-nav)


#-------------------------------------ADLS GEN 2 METHOD -------------------------------------

if method == "adlsgen2":

    # ft = flight tech secret scope variables
    scope_name_ft = "flight_tech_secretscope"
    secret_name_ft_lf = "flight-tech-sas-token-dbfsfiles-listfiles" # list files
    secret_value_ft_lf = "?si=dbfsfileslistpolicy&spr=https&sv=2022-11-02&sr=c&sig=1PdjPvGRFUJSsMHF%2BjjjCWPSJgajxQgOaeZjQpFawPk%3D" # ADLSGEN2 storage account --> list container level (dbfs-files)
    secret_name_ft_rf_pdf = "autonomy-nav-sas-token-dbfsfilesnav-readfiles-pdfs" # read files
    secret_value_ft_rf_pdf = "?si=dbfsfilespolicy&spr=https&sv=2022-11-02&sr=d&sig=XxvzeWdD2N5Xuwzvi91xugLPQCviI6r%2Fnh2TArzD7vo%3D&sdd=1" # ADLSGEN2 storage account --> folder level (dbfs-files-nav/pdfs)


    # autnav = autonomy / navigation secret scope variables
    scope_name_autnav = "autonomy_nav_secretscope"
    secret_name_autnav_lf = "autonomy-nav-sas-token-dbfsfilesnav-listfiles"
    secret_value_autnav_lf = "?si=dbfsfilesnavlistpolicy&spr=https&sv=2022-11-02&sr=c&sig=LkMyEg%2Fq1e09dlxJ5vyTwEW67W3XweoHAZto3AOHIkQ%3D" # ADLSGEN2 storage account --> list container level (dbfs-files-nav)
    secret_name_autnav_rf_matlab = "autonomy-nav-sas-token-dbfsfilesnav-readfiles-matlab" # read files
    secret_value_autnav_rf_matlab = "?si=dbfsfilesnavpolicy&spr=https&sv=2022-11-02&sr=d&sig=l7Ivt%2BBqjSqT81rbUC6YgYxRkrgO8DOIOZ5zZ3apqZc%3D&sdd=1" # ADLSGEN2 storage account --> folder level (dbfs-files-nav/matlab)
    secret_name_autnav_rf_imgs = "autonomy-nav-sas-token-dbfsfilesnav-readfiles-imgs" # read files
    secret_value_autnav_rf_imgs = "?si=dbfsfilesnavpolicy&spr=https&sv=2022-11-02&sr=d&sig=F%2BE0Am0T6Am2ZrxgDss5cOwkAWmI3pr%2Fzh67R%2FXT5nw%3D&sdd=1" # ADLSGEN2 storage account --> folder level (dbfs-files-nav/pdfs)

# COMMAND ----------

# DBTITLE 1,Remove All Secret Scopes
# remove flight tech secret scope
response = delete_secret_scope(databricks_instance, databricks_pat, scope_name_ft)
print(f"response: {response}; response_text: {response.text}")

# remove autonomy and navigation secret scope
response = delete_secret_scope(databricks_instance, databricks_pat, scope_name_autnav)
print(f"response: {response}; response_text: {response.text}")

# COMMAND ----------

# DBTITLE 1,Create Supernal Secret Scope For Storage Account Shared Access Signature (SAS)
# create secret scope for flight tech - regular storage account
response = create_secret_scope(databricks_instance, databricks_pat, scope_name_ft)
print(f"response: {response}; response_text: {response.text}")

# create secret scope for autonomy and navigation - regular storage account
response = create_secret_scope(databricks_instance, databricks_pat, scope_name_autnav)
print(f"response: {response}; response_text: {response.text}")

# COMMAND ----------

# DBTITLE 1,Add SAS Secret Scope Secret for Flight Tech
#-------------------------------------NON ADLS GEN 2 METHOD-----------------------------------

if method == "storageaccount":
    
    # flight tech sas token for container dbfs-files - regular storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_ft, secret_name_ft, secret_value_ft)

    # autonomy navigation sas token for container autonomy-navigation - regular storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_autnav, secret_name_autnav, secret_value_autnav)


#-------------------------------------ADLS GEN 2 METHOD -------------------------------------

if method == "adlsgen2":

    # flight tech sas token for container dbfs-files - ADLSGEN2 storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_ft, secret_name_ft_lf, secret_value_ft_lf)
    # flight tech sas token for container dbfs-files - ADLSGEN2 storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_ft, secret_name_ft_rf_pdf, secret_value_ft_rf_pdf)


    # autonomy navigation sas token for container autonomy-navigation - ADLSGEN2 storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_autnav, secret_name_autnav_lf, secret_value_autnav_lf)
    # autonomy navigation sas token for container autonomy-navigation - ADLSGEN2 storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_autnav, secret_name_autnav_rf_matlab, secret_value_autnav_rf_matlab)
    # autonomy navigation sas token for container autonomy-navigation - ADLSGEN2 storage account
    response = put_secret_in_secret_scope(databricks_instance, databricks_pat, scope_name_autnav, secret_name_autnav_rf_imgs, secret_value_autnav_rf_imgs)

# COMMAND ----------

# DBTITLE 1,Put Permissions on Scope Secret
# add individual permissions
principal = "robert.altmiller@databricks.com"
permission = "READ" # WRITE or MANAGE
response = add_secret_scope_acl(databricks_instance, databricks_pat, scope_name_ft, principal, permission)
print(f"response: {response}; response_text: {response.text}")

# add individual permissions
principal = "chandra.peddireddy@databricks.com"
permission = "READ" # WRITE or MANAGE
response = add_secret_scope_acl(databricks_instance, databricks_pat, scope_name_autnav, principal, permission)
print(f"response: {response}; response_text: {response.text}")


# add local workspace group permissions or AAD
# principal = "altmiller-users"
# permission = "READ" # WRITE or MANAGE
# add_secret_scope_acl(databricks_instance, databricks_pat, scope_name, principal, permission)

# add local workspace group permissions or AAD
# principal = "altmiller-contributors"
# permission = "READ" # WRITE or MANAGE
# add_secret_scope_acl(databricks_instance, databricks_pat, scope_name, principal, permission)

# COMMAND ----------

# DBTITLE 1,Check Secret Scope SAS Setup and Permissions
# secret_scopes_reports
secret_scopes_report = get_secret_scope_report(databricks_instance, databricks_pat, read_scope_user = "robert.altmiller@databricks.com", read_scope_user_perms = "MANAGE", secret_scope_name = None)
print(secret_scopes_report)
