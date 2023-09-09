# Databricks notebook source
# DBTITLE 1,Install Libraries
# MAGIC %pip install openpyxl

# COMMAND ----------

# DBTITLE 1,Library Imports
import os
import pandas as pd
import pyspark.sql.functions as F
from pyspark.sql.types import LongType

# COMMAND ----------

# DBTITLE 1,Local Audit Table Parameters (User Defined)
# Define the catalog, schema and table name for the audit metadata table where all the rules will be stored
audit_catalog = "dmp_frm_dev"
audit_schema = "metadata"
audit_table = "audit_rules"

# COMMAND ----------

# DBTITLE 1,Import Masking Data from Excel CSV or XLSX and Create Masking Metadata Delta Table
# # get the current notebook's path
# notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
# # get the parent directory of the notebook's location
# parent_dir_dbfs = os.path.dirname(notebook_path)

# create path for xlsx masking input parameters
input_base_path = "/dbfs/mnt/bronze_stfrmlanding01/col_masking_input"
input_filename = "masking.xlsx" # or masking.csv
input_file_path = f"{input_base_path}/{input_filename}"

# read masking input file into spark df
df_input_file = spark.createDataFrame(pd.read_excel(input_file_path))

# add_last_updated column to 'df_input_file' dataframe
df_input_file = df_input_file \
  .withColumn("id", F.col("id").cast(LongType())) \
  .withColumn("last_updated", F.current_timestamp())

# write masking metadata to delta table
spark.sql(f"DROP TABLE {audit_catalog}.{audit_schema}.{audit_table}")
df_input_file.write.mode("overwrite").saveAsTable(f"{audit_catalog}.{audit_schema}.{audit_table}")

# check masking input filename as a table in UC
SQL = f"""
  SELECT * FROM `{audit_catalog}`.`{audit_schema}`.`{audit_table}`
"""
audit_df = spark.sql(SQL)
display(audit_df)

# COMMAND ----------

audit_df.printSchema()
