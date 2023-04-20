# Databricks notebook source
# DBTITLE 1,Get Databricks Rest 2.0 Initial Configuration and Base Functions
# MAGIC %run "../general/base"

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - List All Groups in Entire Organization
def list_all_groups(dbricks_instance = None, dbricks_pat = None):
  """list all groups in entire organization"""
  try:
    jsondata = {}
    response = execute_rest_api_call(get_request, get_api_config(dbricks_instance, "groups", "list"), dbricks_pat, jsondata)
    groups = []
    for group in json.loads(response.text)["group_names"]:
      groups.append(group)
    return groups
  except: return None


# groups = list_all_groups(databricks_instance, databricks_pat)
# print(groups)

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - Create a Group 
def create_group(dbricks_instance = None, dbricks_pat = None, group_name = None):
  """create a group in an organization"""
  jsondata = {"group_name": group_name}
  response = execute_rest_api_call(post_request, get_api_config(dbricks_instance, "groups", "create"), databricks_pat, jsondata)
  return response


# group_name = "reporting-department"
# response = create_group(databricks_instance, databricks_pat, group_name)
# print(f"response: {response}; response_text: {response.text}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - List Group Members
def list_group_members(dbricks_instance = None, dbricks_pat = None, group_name = None):
  """list members in a group"""
  try:
    jsondata = {'group_name': group_name}
    response = execute_rest_api_call(get_request, get_api_config(dbricks_instance, "groups", "list-members"), dbricks_pat, jsondata)
    groupmembers = []
    for groupmember in json.loads(response.text)["members"]:
      groupmembers.append(groupmember)
    return groupmembers
  except: return None


# group_name = "ANALYST_USA"
# groupmembers = list_group_members(databricks_instance, databricks_pat, group_name)
# print(f"{groupmembers}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - Add User to a Group
def add_user_to_group(dbricks_instance = None, dbricks_pat = None, user_name = None, parent_name = None):
  """
  add a user to group
  order is 'user_name' user is added to 'parent_name' group
  """
  jsondata = {'user_name': user_name, 'parent_name': parent_name}
  response = execute_rest_api_call(post_request, get_api_config(dbricks_instance, "groups", "add-member"), databricks_pat, jsondata)
  return response


# user_name = "robert.altmiller@databricks.com"
# parent_name = "cody_dataanalytics"
# response = add_user_to_group(databricks_instance, databricks_pat, user_name, parent_name)
# print(f"username '{user_name}' added to group '{parent_name}': {response}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - Remove User From a Group
def remove_user_from_group(dbricks_instance = None, dbricks_pat = None, user_name = None, parent_name = None):
  """
  remove a user from a group
  order is 'user_name' user  is removed from 'parent_name' group
  """
  jsondata = {'user_name': user_name, 'parent_name': parent_name}
  response = execute_rest_api_call(post_request, get_api_config(dbricks_instance, "groups", "remove-member"), databricks_pat, jsondata)
  return response


# user_name = "robert.altmiller@databricks.com"
# parent_name = "cody_dataanalytics"
# response = remove_user_from_group(databricks_instance, databricks_pat, user_name, parent_name)
# print(f"username '{user_name}' removed from group '{parent_name}': {response}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - Add Group to a Group
def add_group_to_group(dbricks_instance = None, dbricks_pat = None, group_name = None, parent_name = None):
  """
  add a group to group
  order is 'group_name' group is added to 'parent_name' group
  """
  jsondata = {'group_name': group_name, 'parent_name': parent_name}
  response = execute_rest_api_call(post_request, get_api_config(dbricks_instance, "groups", "add-member"), databricks_pat, jsondata)
  return response  


# group_name = "ANALYST_USA"
# parent_name = "cody_dataanalytics"
# response = add_group_to_group(databricks_instance, databricks_pat, group_name, parent_name)
# print(f"group_name '{group_name}' added to group '{parent_name}': {response}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - Remove a Group From a Group
def remove_group_from_group(dbricks_instance = None, dbricks_pat = None, group_name = None , parent_name = None):
  """
  remove a group from a group
  order is 'group_name' group is removed from 'parent_name' group
  """
  jsondata = {'group_name': group_name, 'parent_name': parent_name}
  response = execute_rest_api_call(post_request, get_api_config(dbricks_instance, "groups", "remove-member"), databricks_pat, jsondata)
  return response  


# group_name = "ANALYST_USA"
# parent_name = "cody_dataanalytics"
# response = remove_group_from_group(databricks_instance, databricks_pat, group_name, parent_name)
# print(f"group_name '{group_name}' removed from group '{parent_name}': {response}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - List All the Groups a User is in
def list_groups_for_user(dbricks_instance = None, dbricks_pat = None, user_name = None):
  """list all groups a user is in"""
  try:
    jsondata = {'user_name': user_name}
    response = execute_rest_api_call(get_request, get_api_config(dbricks_instance, "groups", "list-parents"), databricks_pat, jsondata)
    usergroups = []
    for usergroup in json.loads(response.text)["group_names"]:
      usergroups.append(usergroup)
    return usergroups
  except: return None

# user_name = "robert.altmiller@databricks.com"
# usergroups = list_groups_for_user(databricks_instance, databricks_pat, user_name)
# print(f"{usergroups}")

# COMMAND ----------

# DBTITLE 1,Databricks Rest API 2.0 - Delete a Group
def delete_group(dbricks_instance = None, dbricks_pat = None, group_name = None):
  """delete a group from organization"""
  jsondata = {"group_name": group_name}
  response = execute_rest_api_call(post_request, get_api_config(dbricks_instance, "groups", "delete"), databricks_pat, jsondata)
  return response

# group_name = "dbricks-readers"
# response = delete_group(databricks_instance, databricks_pat, jsondata)
# print(f"response: {response}; response_text: {response.text}")

# COMMAND ----------

# DBTITLE 1,Create Workspace Groups Report - Applies to a Single Group or to All Groups
def get_groups_report(dbricks_instance = None, dbricks_pat = None, group_name = None):
  """
  get a report of all the groups or individual group in a databricks workspacwe
  we get groups, users in groups, and groups assigned to all users
  """
  
  SS_REPORT_ITEMS = {}
  SS_REPORT_FINAL_GROUPS = []
  SS_REPORT_FINAL_USER_GROUPS = []
  worspace_allusers = []

  # iterate over single group or all workspace groups
  if group_name == None:
    workspacegroups = list_all_groups(dbricks_instance, dbricks_pat)
  else: workspacegroups = [group_name]
  
  # workspace name
  workspace_name = str(' '.join([x for x in get_api_config(dbricks_instance)["databricks_host"]]))

  counter = 1
  for group in workspacegroups:

    # databricks instance / workspace name
    SS_REPORT_ITEMS["workspace"] = workspace_name

    # group name
    SS_REPORT_ITEMS["group_name"] = group

    # get a list of all group members
    group_members = list_group_members(dbricks_instance, dbricks_pat, group)
    if group_members != None: 
      SS_REPORT_ITEMS["group_members_count"] = len(group_members)  
      # get a running list of workspace members
      worspace_allusers += group_members
    else: SS_REPORT_ITEMS["group_members_count"] = 0
    SS_REPORT_ITEMS["group_members"] = group_members

    # append group results
    SS_REPORT_FINAL_GROUPS.append(SS_REPORT_ITEMS)
    SS_REPORT_ITEMS = {}

    # print groups processing status
    print(f'{counter}. group "{group}" processed.....')
    counter += 1
  
  # get all the groups each user is assigned to in databricks workspace
  allusergroupslist = []
  allusergroupsdict = {}

  # remove duplicates from workspace_allusers
  worspace_allusers = [i for n, i in enumerate(worspace_allusers) if i not in worspace_allusers[:n]] 
  # exclude groups and only include users
  worspace_allusers = [user for user in worspace_allusers if "'user_name'" in str(user)]
  print(f"total workspace users to process for user groups: {len(worspace_allusers)}")

  # get all groups single users are a part of
  # counter = 1
  # for user_name in worspace_allusers:
  #   print(user_name)
  #   user = user_name["user_name"]
  #   user_groups = list_groups_for_user(dbricks_instance, dbricks_pat, user)
  #   allusergroupsdict[user] = user_groups
  #   allusergroupslist.append(allusergroupsdict)
  #   allusergroupsdict = {}

  #   # print user groups processing status
  #   print(f'{counter}. user "{user}" groups processed.....')
  #   counter += 1

  # # append user group results 
  # SS_REPORT_FINAL_USER_GROUPS.append(
  #   {
  #     "workspace": workspace_name,
  #     "workspace_user_groups": allusergroupslist
  #   }
  # )

  return json.dumps(SS_REPORT_FINAL_GROUPS)

# COMMAND ----------

# DBTITLE 1,Execute Workspace Groups Report For Recreation of a Single Group or All Workspace Groups
def recreate_all_groups(dbricks_instance = None, dbricks_pat = None, instructions = None,  new_group_name = None):
  """
  recreates all groups in a databricks workspace with correct members (e.g. users and groups) all added
  new_group_name can be 'None' or the name of a new group.  If 'None' overwrite the same group, and
  if new_group_name != None then create a new group based on the settings in instructions
  """
  
  json_groups_obj = json.loads(instructions)

  for group in json_groups_obj:
    
    # workspace name
    workspace_name = group['workspace'].replace(' ', '') #redacted
    
    if new_group_name == None: group_name = group['group_name'] # overwrite same group
    else: group_name = new_group_name # make a new group
    group_members = group["group_members"]

    # delete group
    print(f'delete group "{group_name}": \
      {delete_group(dbricks_instance, dbricks_pat, group_name)}')
    
    # create group
    print(f'create group "{group_name}": \
      {create_group(dbricks_instance, dbricks_pat, group_name)}')

    # add members (e.g. users and groups) to created group
    for member in group_members:
      try: # add a user to a group
        member_name = member["user_name"]
        print(f'add member "{member_name}" to group "{group_name}": \
          {add_user_to_group(dbricks_instance, dbricks_pat, member_name, group_name)}')
      except: # add a group to a group 
        member_name = member["group_name"]
        print(f'add group "{member_name}" to group "{group_name}": \
          {add_group_to_group(dbricks_instance, dbricks_pat, member_name, group_name)}')

    # break after one loop because we created a new group based on the settings in 'instructions'
    if new_group_name != None: break
    print("\n")
