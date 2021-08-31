#############################################

# TEST THE CODE FOR THE SCHEDULER 

"""
2 types of jobs

- custom (upgrade, config, auto-upgrade, reboot, *packetCapture*)

ESS

- 1 custom job at a time
- 2 packet captures at a time

PRO;

- no limit of parallel custom jobs
- 1 cnreach job at a time
- 10 packet captures at a time

"""



# pkC = 2 
# upgrade=1
# default= 1

testCase1  = [

   {
      "jobId":"509edbbd-58c7-42b7-b2ec-1b75e98f8e2cp2-upgrade1",
      "jobType":"upgrade",
      "payload":{
         "user":"Administrator",
         "eType":"",
      },
      "status":"Processing"
   },
   {
      "jobId":"325212ef-d4ae-4524-a792-upgrade2",
      "jobType":"upgrade",
      "payload":{
         "eType":"",
      },
      "status":"processing"
   },
   {
      "jobId":"325212ef-d4ae-4524-a792-pktCapture1",
      "jobType":"pktCapture",
      "payload":{
         "eType":"",
      },
      "status":"Created"
   },
   {
      "jobId":"325212ef-d4ae-4524-a792-pktCapture2",
      "jobType":"pktCapture",
      "payload":{
         "eType":"",
      },
      "status":"Created"
   },
   {
      "jobId":"325212ef-d4ae-4524-a792-pktCapture3",
      "jobType":"pktCapture",
      "payload":{
         "eType":"",
      },
      "status":"Created"
   },
   {
      "jobId":"d56fee98-9e06-44e1-a17d-pktCapture4",
      "jobType":"pktCapture",
      "payload":{
         "eType":"",
      },
      "status":"Processing"
   }
]




CONST_PROCESSING = 'Processing'
CONST_UPGRADE = 'upgrade'
CONST_BULK_UPGRADE = 'bulkUpgrade'
CONST_PKT_CAPTURE = 'packetCapture'

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

# what if there are more than 10 packetCapt jobs in processing 
# when the user subscription change will reflect here in the function 
# If the user is in ESS then , he will be able to add a device and two packet capture 
# to the the job queue 


def filter_allowed_custom_job_ids_to_run(cid, job_list):
    # 1. ensure the parallel count limit
    # 2. allow one cnReach job at a time
    userConfig = checkForUserConfig(cid)
    allowedCnt = {
        "defaultCount" : 0 
    }
    cnReachLimit = 1
    valid_jobs_list = []
    cnReachAllowed = 0
    # include all running(processing) jobs to the allowed list first since they have to be considered for the allowed_count without fail
    for job in job_list:
        if job['status'] == "Processing":
            if job['jobType'] in ["upgrade", "Bulk_upgrade"] and 'eType' in job['payload'] and job['payload']['eType'] == "cnReach":
                cnReachAllowed += 1
            if job['jobType'] not in userConfig :
                allowedCnt["defaultCount"] += 1
            else:
                if job['jobType'] not in allowedCnt:
                    allowedCnt[job['jobType']] = 1
                else:
                    allowedCnt[job['jobType']] += 1
            valid_jobs_list.append(job['jobId'])
    print(allowedCnt,valid_jobs_list)

    for job in job_list:
        if job['status'] == "Processing":
            continue
        if job['jobType'] not in userConfig and job['jobType'] not in allowedCnt :
            allowedCnt[job['jobType']] = 0
        if (allowedCnt["defaultCount"] != 0 and allowedCnt[job['jobType']] >= userConfig["packetCapture"]):
            if userConfig["default"] != -1 :
                break


        # Packet Capture Case 
        if job['jobType'] == "pktCapture" and allowedCnt[job['jobType']] < userConfig["packetCapture"] :
            valid_jobs_list.append(job['jobId'])
            allowedCnt[job['jobType']] += 1
            continue 

        # CnReach Case 
        if job['jobType'] == "upgrade" or job['jobType'] == "Bulk_upgrade":
            if 'eType' in job['payload'] and job['payload']['eType'] == "cnReach":
                if cnReachAllowed >= cnReachLimit:
                    continue
                cnReachAllowed += 1
                allowedCnt["defaultCount"] += 1
                valid_jobs_list.append(job['jobId'])
            if userConfig["default"] == -1:
                allowedCnt["defaultCount"] += 1
                valid_jobs_list.append(job['jobId'])
                continue
            if allowedCnt["defaultCount"] < userConfig["default"]  :
                allowedCnt["defaultCount"] += 1
                valid_jobs_list.append(job['jobId'])

    return valid_jobs_list

cid = "ess"
testResult = filter_allowed_custom_job_ids_to_run(cid , testCase1)
for i in testResult:
    print(i,end=", \n")