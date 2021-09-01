class Scheduler:
    def __init__(self, _id):
        self._id = _id

    def checkForUserConfig(self, cid):
        # use constants
        if cid == 'ess':
            return {
                "default": 3,
                "packetCapture": -1
            }
        return {
            "default": -1,
            "packetCapture": 10
        }

    def filter_allowed_custom_job_ids_to_run(self, cid: str, job_list: list) -> list:
        # 1. ensure the parallel count limit
        # 2. allow one cnReach job at a time
        userConfig = self.checkForUserConfig(cid)
        allowedCnt = {
            "defaultCount": 0
        }
        cnReachLimit = 1
        valid_jobs_list = []
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
            if job['jobType'] in userConfig and job['jobType'] not in allowedCnt:
                allowedCnt[job['jobType']] = 0

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
                if allowedCnt[job['jobType']] < userConfig[job['jobType']] or userConfig[job['jobType']] == -1:
                    valid_jobs_list.append(job['jobId'])
                    allowedCnt[job['jobType']] += 1
        print(allowedCnt)
        return valid_jobs_list
