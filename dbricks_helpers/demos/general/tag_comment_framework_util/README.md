# Tag & Comment Framework - Class-Based Implementation

A modular, class-based framework for managing Unity Catalog tags, table descriptions, and column descriptions using AI-powered generation.

## Project Structure

```
tag_comment_framework_util/
├── utils/
│   ├── __init__.py                        # Package initialization
│   ├── tag_processor.py                   # Tag application logic
│   ├── column_description_processor.py    # Column description generation & import
│   └── table_description_processor.py     # Table description generation & import
├── tags_comments_analysis.py              # Main orchestration notebook
├── requirements.txt                        # Python dependencies
└── README.md                              # Documentation
```

## Excel Input File Format

The framework expects an Excel file (`.xlsx`) with the following structure:

### Required Columns

| Column Name | Description | Example |
|------------|-------------|---------|
| `table_catalog` | Unity Catalog catalog name | `dna_dev` |
| `table_schema` | Schema name within the catalog | `raltmil` |
| `table_name` | Table name | `customer_master` |
| `Tag_Name: domain` | Domain tag value | `Marketing` |
| `Tag_Name: project` | Project tag value | `Loyalty2.0` |
| `Tag_name: {customer_privacy: True\|NA}` | Privacy tag (boolean) | `True`, `False`, or `NA` |
| `Add Table Description (Y/N)` | Generate table description? | `Y` or `N` |
| `Add Column Description (Y/N)` | Generate column descriptions? | `Y` or `N` |
| `Reference Notebook` | Link to documentation | `/notebooks/etl_pipeline` |
| `Override Descriptions (Y/N)` | Use manual descriptions? | `Y` or `N` |
| `Override JSON` | Manual description overrides (see below) | JSON string |
| `Exceptions(if any)` | Notes about exceptions | `Skip audit columns` |
| `Source SQL:` | Source query reference | `SELECT * FROM...` |

### Override JSON Format

When `Override Descriptions (Y/N)` is set to `Y`, provide a JSON structure in the `Override JSON` or `Override Description JSON` column.

The framework supports **two JSON schema formats** for backward compatibility:

#### **New Schema (Recommended)**

```json
{
  "table_desc": "Manual table description here or null to use AI",
  "columns_desc": {
    "column_name_1": "Manual description for this column",
    "column_name_2": "Manual description for this column",
    "column_name_3": null
  },
  "audit_columns_desc": {
    "created_date": "Timestamp when the record was created in the database",
    "updated_date": "Timestamp when the record was last modified",
    "created_by": "Username of the person who created this record",
    "updated_by": "Username of the person who last updated this record"
  }
}
```

#### **Legacy Schema (Still Supported)**

```json
{
  "table": "Manual table description here or null to use AI",
  "columns": {
    "column_name_1": "Manual description for this column",
    "column_name_2": "Manual description for this column",
    "column_name_3": null
  },
  "audit_columns": {
    "created_date": "Timestamp when the record was created in the database",
    "updated_date": "Timestamp when the record was last modified",
    "created_by": "Username of the person who created this record",
    "updated_by": "Username of the person who last updated this record"
  }
}
```

**JSON Structure Explanation:**

- **`table_desc` **: 
  - Provide a string for manual table description
  - Set to `null` or empty string to generate with AI
  
- **`columns_desc`**: 
  - Key-value pairs where key = column name, value = description
  - Set value to `null` or empty string for specific columns to use AI generation
  - Omit columns entirely to use AI for them
  - Set to `"ALL"` to force AI generation for all columns (except audit columns)
  
- **`audit_columns_desc`**: 
  - Definitions for common audit/metadata columns
  - These descriptions will be applied to ANY column with matching name across this table
  - Useful for standardized columns like timestamps, user IDs, etc.
  - **Highest priority** - always applied if column name matches

> **Note:** The framework automatically supports both schema formats. If both are present, the new schema (`table_desc`, `columns_desc`, `audit_columns_desc`) takes precedence.

### Sample Excel Data

**Row 1 - With Override:**

| Column | Value |
|--------|-------|
| `table_catalog` | `dna_dev` |
| `table_schema` | `raltmil` |
| `table_name` | `customer_master` |
| `Tag_Name: domain` | `Marketing` |
| `Tag_Name: project` | `Loyalty2.0` |
| `Tag_name: {customer_privacy: True\|NA}` | `True` |
| `Add Table Description (Y/N)` | `Y` |
| `Add Column Description (Y/N)` | `Y` |
| `Reference Notebook` | `/notebooks/customer_etl` |
| `Override Descriptions (Y/N)` | `Y` |
| `Override JSON` | See JSON example below |

**Row 1 - Override JSON Example (New Schema):**
```json
{
  "table_desc": "Customer master data table containing member information including demographics and contact details",
  "columns_desc": {
    "customer_id": "Unique identifier for each customer in the system",
    "customer_name": "Full legal name of the customer",
    "email_address": null,
    "phone_number": null
  },
  "audit_columns_desc": {
    "created_date": "Timestamp when the record was created in the database",
    "updated_date": "Timestamp when the record was last modified",
    "created_by": "Username of the person who created this record",
    "updated_by": "Username of the person who last updated this record"
  }
}
```

**Row 2 - Without Override (Standard AI Generation):**

| Column | Value |
|--------|-------|
| `table_catalog` | `dna_dev` |
| `table_schema` | `raltmil` |
| `table_name` | `product_inventory` |
| `Tag_Name: domain` | `Operations` |
| `Tag_Name: project` | `Loyalty2.0` |
| `Tag_name: {customer_privacy: True\|NA}` | `NA` |
| `Add Table Description (Y/N)` | `Y` |
| `Add Column Description (Y/N)` | `Y` |
| `Reference Notebook` | _(empty)_ |
| `Override Descriptions (Y/N)` | `N` |
| `Override JSON` | _(empty)_ |

### Override JSON Examples

#### **Example 1: Force AI for All Columns (New Schema)**
```json
{
  "table_desc": "Product inventory table",
  "columns_desc": "ALL",
  "audit_columns_desc": {
    "created_date": "Record creation timestamp",
    "updated_date": "Record last update timestamp"
  }
}
```
**Result:** All columns use AI except audit columns use standard descriptions

#### **Example 2: Mix Manual, AI, and Audit (New Schema)**
```json
{
  "table_desc": "Customer master data",
  "columns_desc": {
    "customer_id": "Unique customer identifier",
    "customer_name": "Full legal name",
    "email_address": null
  },
  "audit_columns_desc": {
    "created_date": "Record creation timestamp"
  }
}
```
**Result:**
- `customer_id`: Manual description
- `customer_name`: Manual description
- `email_address`: AI generated (null = use AI)
- `created_date`: Audit description
- Other columns: AI generated

#### **Example 3: Only Audit Columns (New Schema)**
```json
{
  "audit_columns_desc": {
    "created_date": "Record creation timestamp",
    "updated_date": "Record last update timestamp",
    "created_by": "User who created the record",
    "updated_by": "User who last updated the record"
  }
}
```
**Result:** Only audit columns use standard descriptions, all others use AI

#### **Example 4: Legacy Schema (Still Works)**
```json
{
  "table": "Product inventory table",
  "columns": "ALL",
  "audit_columns": {
    "created_date": "Record creation timestamp",
    "updated_date": "Record last update timestamp"
  }
}
```
**Result:** Same behavior as Example 1, using the older schema format

### Processing Logic

The framework processes each row with the following logic:

#### **1. Apply Tags**
All tag columns are applied to the table

#### **2. Table Description**
- If `Override Descriptions = Y` and `Override JSON["table_desc"]` (or `["table"]`) has a value → Use manual description
- If `Override Descriptions = Y` and `Override JSON["table_desc"]` (or `["table"]`) is `null` or empty → Generate with AI
- If `Override Descriptions = N` → Generate with AI (if `Add Table Description = Y`)

#### **3. Column Descriptions**

**Priority Order (Highest to Lowest):**
1. **Audit columns** (always highest priority if column name matches)
2. **Specific column overrides** (from "columns_desc" or "columns" object)
3. **"ALL" flag** (forces AI for all non-audit columns)
4. **Default AI generation** (if not specified)

**Detailed Logic:**
- If `columns_desc` (or `columns`) = "ALL":
  - Check if column in `audit_columns_desc` (or `audit_columns`) → Use audit description
  - Else → Generate with AI
- Else, check if column name in `audit_columns_desc` (or `audit_columns`) → Use audit column description
- Else, check if column in `columns_desc` (or `columns`) object:
  - If value is not null/empty → Use manual description
  - If value is null/empty → Generate with AI
- Else (column not specified) → Generate with AI (if `Add Column Description = Y`)

### Notes

- Tag column names can be customized - the framework auto-detects columns starting with `Tag_Name:` or `Tag_name:`
- Boolean tag values support: `True`, `False`, `1`, `0`, `NA`, or empty
- JSON in `Override JSON` must be valid JSON format (will error out if invalid)
- If `Override Descriptions = N`, the `Override JSON` column is ignored
- Audit columns are matched by exact column name (case-sensitive)
- If table doesn't have audit columns defined in JSON, they are simply skipped (no error)

### Safety Features

The framework includes robust safety checks:

- **Null Value Handling**: If `audit_columns` or `columns` is `null`, empty string, or wrong data type, it's treated as empty `{}`
- **JSON Validation**: Invalid JSON will error out immediately with clear error message
- **Missing Keys**: Missing `table`, `columns`, or `audit_columns` keys are handled gracefully
- **Type Safety**: Validates data types before processing to prevent runtime errors

## Features

- **Modular Design**: Reusable Python classes for each operation
- **Multithreaded Processing**: Parallel execution for improved performance
- **AI-Powered**: Leverages Databricks AI endpoints for intelligent descriptions
- **Override Capability**: Manual control over descriptions via JSON overrides
- **Audit Column Support**: Standardized descriptions for common audit columns
- **Safety Checks**: Robust handling of null/invalid JSON values
- **Enhanced Logging**: Detailed breakdown showing AI vs Manual vs Audit sources
- **Source Tracking**: Every description is tagged with its source (ai/manual/audit)
- **Error Handling**: Clear error messages and failure tracking
- **Progress Tracking**: Real-time status updates during processing

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Import Classes

```python
from utils import (
    TagProcessor,
    ColumnDescriptionGenerator,
    ColumnDescriptionImporter,
    TableDescriptionGenerator,
    TableDescriptionImporter
)
```

### 3. Run the Main Notebook

Open `tags_comments_analysis.py` in Databricks and configure:
- **file_path**: Path to Excel file with table metadata
- **base_volume_path**: Volume path for storing output files
- **model_endpoint**: AI model to use for description generation

## Usage Examples

### Apply Tags

```python
tag_processor = TagProcessor(
    spark=spark,
    tag_column_mapping={"tag_domain": "domain", "tag_project": "project"},
    verbose=False
)
results = tag_processor.execute(df_pandas, max_workers=10)
```

### Generate Column Descriptions

```python
generator = ColumnDescriptionGenerator(
    spark=spark,
    catalog="catalog_name",
    schema="schema_name",
    table="table_name",
    output_path="/Volumes/path/",
    dbutils=dbutils,
    endpoint_name="databricks-meta-llama-3-3-70b-instruct",
    verbose=False
)
descriptions = generator.execute()
generator.save_comments(descriptions)
```

### Import Column Descriptions

```python
importer = ColumnDescriptionImporter(
    spark=spark,
    input_path="/Volumes/path/bulk_comments/columns/json",
    verbose=False
)
importer.execute()
```

### Generate Table Descriptions

```python
generator = TableDescriptionGenerator(
    spark=spark,
    catalog="catalog_name",
    schema="schema_name",
    table="table_name",
    output_path="/Volumes/path/",
    dbutils=dbutils,
    endpoint_name="databricks-meta-llama-3-3-70b-instruct",
    verbose=False
)
descriptions = generator.execute()
generator.save_descriptions(descriptions)
```

### Import Table Descriptions

```python
importer = TableDescriptionImporter(
    spark=spark,
    input_path="/Volumes/path/bulk_comments/tables/json",
    verbose=False
)
importer.execute()
```

## Classes Overview

### TagProcessor
**Purpose**: Apply tags to Unity Catalog tables

**Features**:
- Handles boolean conversions (1/0 → true/false)
- Skips NA/null values
- Catches policy violations
- Returns detailed success/failure status

**Key Parameters**:
- `tag_column_mapping`: Dictionary mapping Excel columns to tag names
- `verbose`: Enable detailed logging (default: False)
- `max_workers`: Number of parallel threads

### ColumnDescriptionGenerator
**Purpose**: Generate AI-powered descriptions for table columns

**Features**:
- Fetches column metadata from information_schema
- Retrieves sample data for context
- Generates descriptions using AI
- Supports manual overrides via JSON
- Tracks source of each description (ai/manual/audit)
- Saves results to storage

**Key Parameters**:
- `endpoint_name`: AI model endpoint
- `data_limit`: Number of sample rows (default: 5)
- `max_cell_chars`: Max characters per cell (default: 1000)
- `prompt_return_length`: Max words in description (default: 40)
- `always_update`: Overwrite existing comments (default: True)
- `override_json`: Optional JSON with manual descriptions (default: None)

### ColumnDescriptionImporter
**Purpose**: Apply generated column descriptions to Unity Catalog

**Features**:
- Reads descriptions from storage
- Groups by table for efficient processing
- Updates Unity Catalog with ALTER TABLE commands
- Tracks success/failure for each column

### TableDescriptionGenerator
**Purpose**: Generate AI-powered descriptions for tables

**Features**:
- Fetches table schema and metadata
- Includes sample data for context
- Generates comprehensive table descriptions
- Supports manual overrides via JSON
- Tracks source of each description (ai/manual)
- Saves results to storage

**Key Parameters**:
- `endpoint_name`: AI model endpoint
- `data_limit`: Number of sample rows (default: 2)
- `max_cell_chars`: Max characters per cell (default: 1000)
- `prompt_return_length`: Max words in description (default: 200)
- `always_update`: Overwrite existing comments (default: True)
- `override_json`: Optional JSON with manual description (default: None)

### TableDescriptionImporter
**Purpose**: Apply generated table descriptions to Unity Catalog

**Features**:
- Reads descriptions from storage
- Batch processing for multiple tables
- Updates Unity Catalog with COMMENT ON TABLE commands
- Returns count of processed tables

## Configuration

### AI Model Endpoints

The framework supports multiple AI models:
- `databricks-meta-llama-3-3-70b-instruct` (default)
- `databricks-claude-sonnet-4-5`
- `databricks-gemini-2-5-pro`

### Storage Format

Generated descriptions are saved in JSON format (CSV also supported) to Unity Catalog Volumes:
```
/Volumes/<catalog>/<schema>/<volume>/bulk_comments/
├── columns/
│   └── json/
│       ├── table1/
│       └── table2/
└── tables/
    └── json/
        ├── table1/
        └── table2/
```

### Parallelism

The framework automatically calculates optimal parallelism:
```python
default_parallelism = spark.sparkContext.defaultParallelism / 2
# Fallback: (4 * os.cpu_count()) - 1
```

You can override this when calling `execute()`:
```python
processor.execute(df, max_workers=15)
```

## Error Handling

The framework provides clear error messages for common issues:

- **Table not found**: "Table not found: catalog.schema.table"
- **Permission denied**: "Permission denied on /Volumes/..."
- **AI endpoint failure**: "AI endpoint unavailable"
- **Tag policy violation**: "Invalid tag value for policy"
- **Save failure**: "Save failed: PathIOException"

All errors are logged and included in the final execution report.

## Best Practices

1. **Use verbose=False**: When running multithreaded operations, disable verbose logging for cleaner output
2. **Pass dbutils**: Always pass dbutils to generators for proper file cleanup
3. **Review results**: Check the detailed status report for any failures
4. **Adjust parallelism**: Set max_workers based on cluster size and workload
5. **Monitor AI costs**: Be mindful of the number of AI calls when processing large datasets

## Dependencies

Required Python packages (see `requirements.txt`):
```
openpyxl  # For reading Excel files
```

PySpark and Databricks utilities are provided by the Databricks runtime.

## Workflow

The main notebook follows this workflow:

1. **Load Excel** → Read table metadata from Excel file
2. **Apply Tags** → Apply tags to tables using TagProcessor
3. **Identify Tables** → Determine which tables need descriptions
4. **Column Descriptions** → Generate and import column descriptions (multithreaded)
5. **Table Descriptions** → Generate and import table descriptions (multithreaded)
6. **Final Report** → Display execution summary with success/failure counts

## Troubleshooting

### Issue: "PathIOException: Input/output error"
**Solution**: The framework automatically cleans old files before saving. Ensure dbutils is passed to generators.

### Issue: "DATATYPE_MISMATCH.FILTER_NOT_BOOLEAN"
**Solution**: This has been fixed in the current version. Ensure you're using the latest code.

### Issue: "Table not found in system.information_schema"
**Solution**: Verify the table exists and you have permissions to access it.

### Issue: "AI endpoint unavailable"
**Solution**: Check that the model endpoint name is correct and the endpoint is running.

## License

Internal use only.
