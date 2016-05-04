# Install

Install redis. On windows, you can install it from https://github.com/MSOpenTech/redis/releases

Then to install the python deps, in a virtualenv do 

```pip install -r requirements.txt```

# Run

You need to have redis, celery, and the webserver all running for stuff to work.

Start redis (on windows you can run C:\Program Files\Redis\redis-server.exe - I found it 
didn't work properly unless I ran it as administrator, ymmv)

Start the webserver

``` python web.py```

Start the celery - for me this looks like 

```venv/Scripts/celery -A tasks worker --loglevel=info ```

# Tests

The tests use environment variables, you need to run something like this:

```WEB_URL=http://localhost:5000 XPLAN_USERNAME=a XPLAN_PASSWORD=a XPLAN_URL=http://localhost:1983/autotestuk/ /cygdrive/c/python27/scripts/nosetests```

# REST API

These URLs are so ugly, sorry.

## CSV Uploads

These are all multipart POST handlers taking the following multipart/form-data parts:

```xplan_url```: the BASEURL of your XPLAN site

```xplan_username``` the XPLAN username to use to perform the upload. Must have the right capabilities i.e. ```create_user``` for user upload, ```edit_level``` for access level upload.

```xplan_password``` your XPLAN password (maybe one day we can support OAuth2 so nobody has to do this)

```file``` the CSV file being uploaded

When successful, each of the handlers returns 200 and a task UUID in the body which can be passed to ```/task/<task_id>``` to get the result.

###```POST /upload_csv/access_levels```

Upload a CSV of access levels in the format returned by ```GET /access_levels```, see [access_levels.csv](access_levels.csv) 

###```POST /upload_csv/users```

Upload a CSV of users in the format shown in [users.csv](users.csv)

###```GET /access_levels```

Dumps a csv of the site's access levels that can be used as a template. This also requires ```xplan_url```, ```xplan_username``` and ```xplan_password```, but they should be passed as GET parameters.

###```GET /task/<task_id>```

Get the results of the CSV upload. 

When the task has not yet completed, returns HTTP 102 with a description of the job status in JSON format (we could use celery custom states to doing load progress quite easily, but I haven't done this).

When the task has completed, returns HTTP 200 with a description of the job's result in JSON format. For now this is just the concatenated output of the batch requests used to perform the job, which is pretty raw but probably quite helpful in producing a report of what happened.

## cURL examples

Get the access levels template and write it to a csv

```curl "http://localhost:5000/access_levels?xplan_username=a&xplan_password=a&xplan_url=http%3A%2F%2Flocalhost%3A1983%2Fautotestuk%2F" > test.csv```

Stick some Xs in it and push it back up

```curl -v "http://localhost:5000/upload_csv/access_levels" -F "xplan_url=http://localhost:1983/autotestuk/" -F "xplan_username=a" -F "xplan_password=a" -F "file=@test.csv"```

> ```1ebae51e-efdd-4e34-b111-033ef0306bc3```

Ask for the result of the upload

```curl -v "http://localhost:5000/task/1ebae51e-efdd-4e34-b111-033ef0306bc3"```

> ```[{"msg": "OK", "body": "{\"caps\":[\"edit_entity_note\",\"list_group\",\"login\"],\"name\":\"Test Access Level 1462384104.84\",\"id\":\"10\"}", "code": 200, "name": "0", "headers": {"Content-Type": "application/json"}}, {"msg": "OK", "body": "{\"caps\":[\"view_user_time_taken_data_for_visible_users\",\"mailchimp_integration\",\"edit_entity_note\",\"campaign\",\"manage_template\",\"upload_template_merge_on_the_fly\",\"list_client\",\"list_group\",\"remove_existing_invoice\",\"allow_task_thread_tpl_access\",\"edit_existing_invoice\",\"login_with_sso\",\"change_password\",\"user_time_taken\",\"edit_client\",\"login_with_password\",\"create_tasks_from_template_only\",\"create_client\",\"client_focus\",\"list_user\",\"login\",\"allow_diary_tpl_access\",\"use_invoice\",\"link_client_partner\",\"edit_tasks\",\"allow_diary\",\"allow_edai\",\"create_tasks_from_non_template\",\"override_target_asset_allocation\",\"docnote_delete_docpart\",\"allow_tasks\",\"remove_groupitem\",\"xmerge_from_client_list_or_search_results\",\"allow_email\",\"allow_email_tpl_access\"],\"name\":\"Adviser\",\"id\":\"1\"}", .... etc ```

Create 20 or so users

```curl -v "http://localhost:5000/upload_csv/users" -F "xplan_url=http://localhost:1983/autotestuk/" -F "xplan_username=a" -F "xplan_password=a" -F "file=@users.csv"```

> ```8d47832b-1c8b-4c3f-a811-f03f1eb448e2```

Get the result (after a few 102s)

```curl -v "http://localhost:5000/task/8d47832b-1c8b-4c3f-a811-f03f1eb448e2"```

> HTTP/1.0 102 PROCESSING

> HTTP/1.0 102 PROCESSING

> HTTP/1.0 200 OK


```[{"msg": "Created", "body": "{\"id\":330}", "code": 201, "name": "0", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":331}", "code": 201, "name": "1", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":332}", "code": 201, "name": "2", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":333}", "code": 201, "name": "3", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":334}", "code": 201, "name": "4", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":335}", "code": 201, "name": "5", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":336}", "code": 201, "name": "6", "headers": {"Content-Type": "application/json"}}, {"msg": "Created", "body": "{\"id\":337}", .... ```









