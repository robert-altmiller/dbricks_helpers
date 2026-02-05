# Row-Level Security (RLS) on Databricks System Tables

This tool implements workspace-level row-level security on Databricks System Tables. It creates filtered views that restrict users to only see system table data for workspaces where they have admin privileges.

## Overview

Databricks System Tables contain sensitive operational data across all workspaces in an account (audit logs, query history, billing, compute usage, etc.). By default, users with access to these tables can see data from **all** workspaces. This tool solves that by:

1. Collecting workspace permission metadata (users, admins, groups) from all workspaces in a Databricks account.
2. Creating dynamic views on system tables that filter rows based on the current user's workspace admin permissions.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Databricks Account                            │
├─────────────────────────────────────────────────────────────────┤
│  Step 1: Collect Workspace Metadata                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │ Workspace 1 │    │ Workspace 2 │    │ Workspace N │          │
│  │ - Users     │    │ - Users     │    │ - Users     │          │
│  │ - Admins    │    │ - Admins    │    │ - Admins    │          │
│  │ - Catalogs  │    │ - Catalogs  │    │ - Catalogs  │          │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘          │
│         └──────────────────┼──────────────────┘                  │
│                            ▼                                     │
│              Delta Tables (permissions metadata)                 │
├─────────────────────────────────────────────────────────────────┤
│  Step 2: Create RLS Views (parallel execution)                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  system.access.audit  ──►  vw_system_access_audit       │    │
│  │  system.compute.*     ──►  vw_system_compute_*          │    │
│  │  system.billing.usage ──►  vw_system_billing_usage      │    │
│  │  ... (18 system tables)                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│         Users only see data for workspaces they admin            │
└─────────────────────────────────────────────────────────────────┘
```

## Files

| File | Description |
|------|-------------|
| `workspace_access_metadata_job.yaml` | Databricks Asset Bundle job definition that orchestrates the pipeline |
| `workspace_access_metadata_step1.py` | Notebook that collects workspace/permission metadata (e.g., users/admins) from all account workspaces |
| `workspace_access_metadata_step2.py` | Notebook that creates filtered views on system tables with RLS |

## Service Principal Requirements

This tool requires a **Service Principal (SP)** with account-level admin privileges. The service principal:

1. **Authenticates** to the Databricks Account API to enumerate workspaces and permissions.
2. **Temporarily elevates itself** to workspace admin on each workspace to retrieve catalog information.
3. **Owns all created views** - When the job runs, the SP's execution context creates the views, making the SP the implicit owner of all RLS views.

### Why Service Principal Ownership Matters

The Service Principal must be the **owner** of the RLS views. This is critical because:

1. **DEFINER Security Context**: Views execute with the owner's permissions. The SP owner has access to **all rows** in the underlying system tables.
2. **Dynamic Filtering**: When a user queries the view, the `SQL_ROW_FILTER_CTE` uses `current_user()` and `is_account_group_member()` to filter rows based on the **invoking user's** workspace admin permissions.
3. **Separation of Concerns**: The SP provides full data access; the CTE provides row-level filtering.

This two-layer approach ensures:
- The view can read all system table data (via SP owner permissions).
- Each user only sees rows for workspaces where they are an admin (via the CTE filter).
- Views remain accessible even if individual users leave the organization.
- Simplified permission management - grant `SELECT` on views to users/groups.

## Supported System Tables

The tool creates filtered views for the following system tables:

| Category | Tables |
|----------|--------|
| **Access** | `assistant_events`, `audit`, `column_lineage`, `outbound_network`, `table_lineage`, `workspaces_latest` |
| **Compute** | `clusters`, `node_timeline`, `warehouse_events`, `warehouses` |
| **Lakeflow** | `job_run_timeline`, `job_task_run_timeline`, `job_tasks`, `jobs` |
| **Query** | `history` |
| **Serving** | `served_entities` |
| **Storage** | `predictive_optimization_operations_history` |
| **Billing** | `usage` |

## How RLS Works

RLS is implemented through a two-layer security model:

### Layer 1: Service Principal Ownership (DEFINER Context)

The Service Principal owns all views and has access to **all rows** in the underlying system tables. When the view is queried, it executes with the SP's permissions, allowing it to read the complete dataset.

### Layer 2: CTE Row Filtering (INVOKER Context)

Each view uses a Common Table Expression (CTE) that dynamically filters rows based on the **querying user's** permissions:

```sql
WITH admin_groups_users AS (
    SELECT DISTINCT workspace_id, workspace_url
    FROM all_workspace_and_catalog_perms_admins
    WHERE 
        (admins.group_name IS NOT NULL OR admins.user_name IS NOT NULL) AND
        (is_account_group_member(admins.group_name) = true 
         OR current_user() = admins.user_name)
)
SELECT x.*
FROM system.access.audit x
JOIN admin_groups_users admins ON x.workspace_id = admins.workspace_id
```

### How It Works Together

1. **User queries the view** → View executes with SP owner permissions (full data access).
2. **CTE evaluates `current_user()`** → Returns the querying user's identity.
3. **CTE evaluates `is_account_group_member()`** → Checks the querying user's group memberships.
4. **JOIN filters rows** → Only rows matching the user's admin workspaces are returned.

This ensures:
- Users only see rows for workspaces where they are a direct admin.
- Users in admin **groups** see rows for workspaces (e.g., workspace_id) where that group has admin access.
- The filter is applied dynamically at query time - no data duplication needed.

## Setup Instructions

### 1. Create a Service Principal

Create an SP in your Databricks account with:
- Account Admin privileges (to enumerate workspaces and assign permissions).
- A client ID and client secret.

### 2. Configure Credentials

Update `workspace_access_metadata_step1.py` with your credentials:

**For Azure:**
```python
"azure": {
    "tenant_id": "YOUR_AZURE_TENANT_ID",
    "account_id": "YOUR_DATABRICKS_ACCOUNT_ID",
    "account_host": "https://accounts.azuredatabricks.net",
    "client_id": "YOUR_SP_CLIENT_ID",
    "client_secret": "YOUR_SP_CLIENT_SECRET",
    "workspace_host": "YOUR_WORKSPACE_HOST",
    "workspace_pat": "YOUR_WORKSPACE_TOKEN"
}
```

**For AWS:**
```python
"aws": {
    "account_id": "YOUR_DATABRICKS_ACCOUNT_ID",
    "account_host": "https://accounts.cloud.databricks.com",
    "client_id": "YOUR_SP_CLIENT_ID",
    "client_secret": "YOUR_SP_CLIENT_SECRET",
    "workspace_host": "YOUR_WORKSPACE_HOST",
    "workspace_pat": "YOUR_WORKSPACE_TOKEN"
}
```

> **Security Note:** Consider using Databricks Secrets instead of hardcoding credentials. The commented code in Step 1 shows how to create a secret scope.

### 3. Configure Catalog and Schema

Update the job parameters in `workspace_access_metadata_job.yaml`:

```yaml
base_parameters:
  iam_catalog: YOUR_CATALOG
  iam_schema: YOUR_SCHEMA
```

### 4. Update Cluster ID

Replace the `existing_cluster_id` in the YAML with your cluster:

```yaml
existing_cluster_id: YOUR_CLUSTER_ID
```

### 5. Deploy and Run

Deploy using Databricks Asset Bundles:

```bash
databricks bundle deploy
databricks bundle run workspace_access_metadata
```

Or manually upload the notebooks and create a workflow in the Databricks UI.

## Output Tables

Step 1 creates three Delta tables:

| Table | Description |
|-------|-------------|
| `all_workspace_and_catalog_perms` | Full nested JSON with all workspace/catalog permissions |
| `all_workspace_and_catalog_perms_admins` | Exploded table with one row per admin assignment |
| `all_workspace_and_catalog_perms_users` | Exploded table with one row per user assignment |

## Output Views

Step 2 creates views named `vw_system_<catalog>_<table>`, for example:
- `vw_system_access_audit`
- `vw_system_compute_clusters`
- `vw_system_billing_usage`

## Granting Access to Users

After the views are created, grant `SELECT` access to users or groups:

```sql
GRANT SELECT ON VIEW catalog.schema.vw_system_access_audit TO `user@example.com`;
GRANT SELECT ON VIEW catalog.schema.vw_system_access_audit TO `data_analysts`;
```

## Scheduling Recommendations

- **Step 1** should run periodically (daily or weekly) to refresh workspace permission metadata.
- **Step 2** only needs to run when new system tables are added or view definitions change.
- The views themselves are dynamic and apply RLS at query time.

## Limitations

- Only filters based on **workspace admin** permissions (not regular user access).
- Requires system tables to have a `workspace_id` column for the join.
- Service principal must have account-level admin access.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Workspace not alive" messages | Some workspaces may be stopped or inaccessible - these are skipped |
| Permission errors | Ensure the SP has account admin privileges |
| Empty views | Verify the current user has workspace admin access somewhere |
| Missing catalogs | The SP needs to be elevated to workspace admin to see catalogs |

