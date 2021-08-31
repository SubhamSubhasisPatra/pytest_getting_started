def checkForUserConfig(cid):
    if cid == 'ess':
        return {
            "default" : 1,
            "packetCapture" : 2
        }
    return {
        "default" : -1,
        "packetCapture" : 10
    }

def filter_allowed_custom_job_ids_to_run(cid, job_list):
    userConfig = checkForUserConfig(cid)
    allowedCnt = {
        "defaultCount" : 0
    }
    cnReachLimit = 1
    valid_jobs_list, processing_job_list , non_processing_job_list   = [], [], []
    cnReachAllowed = 0

    # Added all the processing jobs to the list
    for job in job_list:
        if job['status'] == "Processing":
            if job['jobType'] in ["upgrade", "Bulk_upgrade"] and 'eType' in job['payload'] and job['payload']['eType'] == "cnReach":
                cnReachAllowed += 1
            if job['jobType'] not in userConfig:
                allowedCnt["defaultCount"] += 1
            else:
                if job['jobType'] not in allowedCnt:
                    allowedCnt[job['jobType']] = 1
                else:
                    allowedCnt[job['jobType']] += 1
            valid_jobs_list.append(job['jobId'])

    for job in job_list:
        if job['status'] == "Processing":
            continue
        if job['jobType'] not in userConfig and job['jobType'] not in allowedCnt:
            allowedCnt[job['jobType']] = 0
        if job['jobType'] not in userConfig:
            if allowedCnt["defaultCount"] != 0 and allowedCnt[job['jobType']] >= userConfig["default"]:
                if userConfig["default"] != -1 :
                    break
        else:
            if allowedCnt["defaultCount"] != 0 and allowedCnt[job['jobType']] >= userConfig[job['jobType']]:
                if userConfig["default"] != -1:
                    break
        if job['jobType'] == "upgrade" or job['jobType'] == "Bulk_upgrade":
            if 'eType' in job['payload'] and job['payload']['eType'] == "cnReach":
                if cnReachAllowed >= cnReachLimit:
                    continue
                cnReachAllowed += 1
                allowedCnt["defaultCount"] += 1
                valid_jobs_list.append(job['jobType'])
        if job["jobType"] not in userConfig:
            if userConfig["default"] == -1:
                allowedCnt["defaultCount"] += 1
                valid_jobs_list.append(job['jobId'])
                continue
            if allowedCnt["defaultCount"] < userConfig["default"]:
                allowedCnt["defaultCount"] += 1
                valid_jobs_list.append(job['jobId'])
        else:
            if allowedCnt[job['jobType']] < userConfig[job['jobType']]:
                valid_jobs_list.append(job['jobId'])
                allowedCnt[job['jobType']] += 1

    print(allowedCnt)
    return valid_jobs_list

testCase1  =[
    {
      "jobId": "509edbbd-58c7-42b7-b2ec-1b75e98f8e2cp2-upgrade1",
      "jobType": "upgrade",
      "payload": {
        "user": "Administrator",
        "eType": ""
      },
      "status": "Processing"
    },
    {
      "jobId": "325212ef-d4ae-4524-a792-upgrade2",
      "jobType": "upgrade",
      "payload": {
        "eType": ""
      },
      "status": "Processing"
    },
    {
      "jobId": "325212ef-d4ae-4524-a792-packetCapture1",
      "jobType": "packetCapture",
      "payload": {
        "eType": ""
      },
      "status": "Created"
    },
    {
      "jobId": "325212ef-d4ae-4524-a792-packetCapture2",
      "jobType": "packetCapture",
      "payload": {
        "eType": ""
      },
      "status": "Created"
    },
    {
      "jobId": "325212ef-d4ae-4524-a792-packetCapture3",
      "jobType": "packetCapture",
      "payload": {
        "eType": ""
      },
      "status": "Created"
    },
    {
      "jobId": "d56fee98-9e06-44e1-a17d-packetCapture4",
      "jobType": "packetCapture",
      "payload": {
        "eType": ""
      },
      "status": "Processing"
    }
  ]

print(filter_allowed_custom_job_ids_to_run("ess", testCase1))