import json
from pkt_capture import Scheduler

testCaseJSON = open('testCase.json')
testCaseJSON = json.load(testCaseJSON)

non_exist_test = open("non_exist_testcases.json")
non_exist_test = json.load(non_exist_test)

'''
# TODO : check for the class obeject

def test_packet_capture_for_ess():
    pktCap = Scheduler(1)
    test_case_1 = pktCap.filter_allowed_custom_job_ids_to_run('ess', testCaseJSON["testCase1"])
    test_case_2 = pktCap.filter_allowed_custom_job_ids_to_run('ess', testCaseJSON["testCase2"])
    test_case_3 = pktCap.filter_allowed_custom_job_ids_to_run('ess', testCaseJSON["testCase3"])
    test_case_4 = pktCap.filter_allowed_custom_job_ids_to_run('ess', testCaseJSON["testCase4"])
    test_case_6 = pktCap.filter_allowed_custom_job_ids_to_run('ess', testCaseJSON["testCase6"])

    # Assertion
    assert test_case_1 == testCaseJSON["testCase1_output1"]
    assert test_case_2 == testCaseJSON["testCase2_output2"]
    assert test_case_3 == testCaseJSON["testCase3_output3"]
    assert test_case_4 == testCaseJSON["testCase4_output4"]
    assert test_case_6 == testCaseJSON["testCase6_output6"]


def test_packet_capture_for_pro():
    pktCap = Scheduler(1)
    test_case_5 = pktCap.filter_allowed_custom_job_ids_to_run('pro', testCaseJSON["testCase5"])

    # Assertion
    assert test_case_5 == testCaseJSON["testCase5_output5"]
'''


# TODO : Add the test cases for some non exsisting cases

def test_packet_capture_for_no_limit():
    pktCap = Scheduler(1)
    test_case_1 = pktCap.filter_allowed_custom_job_ids_to_run('ess', non_exist_test["testCase1"])
    test_case_2 = pktCap.filter_allowed_custom_job_ids_to_run('ess', non_exist_test["testCase2"])
    # Assertion
    assert test_case_1 == non_exist_test["testCase1_output1"]
    assert test_case_2 == non_exist_test["testCase2_output2"]