"""
Library for TDM Connections (CONN) - Topology 1NE2 PONT(STM64 CONSTRAIN)

"""

from katelibs.testcase          import TestCase
from katelibs.eqpt1850tss320    import Eqpt1850TSS320
from katelibs.instrumentONT     import InstrumentONT
from katelibs.swp1850tss320     import SWP1850TSS
from katelibs.facility_tl1      import *

import sys
import time

from audioop import ratecv
from asyncio.tasks import sleep
from xdist.slavemanage import HostRSync
from inspect import currentframe
from sunau import Au_read


def Debug_Line_Function(zq_gap = 0, info = "None"):
    cf = currentframe()
    zq_line = cf.f_back.f_lineno + zq_gap
    zq_code = str(cf.f_back.f_code)
    zq_temp = zq_code.split(",")
    zq_function = zq_temp[0].split(" ")
    zq_res = "***** FAILED at Line [{}] in Function [{}] - [{}]".format(zq_line, zq_function[2], info)
    return zq_res


def setup_ONT_Conn(ONT1, ONT2, ONT1_P1, ONT2_P1, rate):
        
    callResult = ONT1.init_instrument(ONT1_P1)
    print("ONT5xx.init_intrument ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)
        
    callResult = ONT2.init_instrument(ONT2_P1)
    print("ONT5xx.init_intrument ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_tx_bit_rate(ONT1_P1, rate)
    print("ONT5xx.get_set_tx_bit_rate ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_tx_bit_rate(ONT2_P1, "STM64")
    print("ONT5xx.get_set_tx_bit_rate ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_rx_bit_rate(ONT1_P1, rate)
    print("ONT5xx.get_set_rx_bit_rate ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_rx_bit_rate(ONT2_P1, "STM64")
    print("ONT5xx.get_set_rx_bit_rate ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_rx_channel_mapping_size(ONT1_P1, "VC4")
    print("ONT5xx.get_set_rx_channel_mapping_size ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_rx_channel_mapping_size(ONT2_P1, "VC4")
    print("ONT5xx.get_set_rx_channel_mapping_size ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_tx_channel_mapping_size(ONT1_P1, "VC4")
    print("ONT5xx.get_set_tx_channel_mapping_size ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_tx_channel_mapping_size(ONT2_P1, "VC4")
    print("ONT5xx.get_set_tx_channel_mapping_size ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_laser_status(ONT1_P1, "ON")
    print("ONT5xx.get_set_laser_status ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_laser_status(ONT2_P1, "ON")
    print("ONT5xx.get_set_laser_status ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_clock_reference_source(ONT1_P1, "RX")
    print("ONT5xx.get_set_clock_reference_source ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_clock_reference_source(ONT2_P1, "RX")
    print("ONT5xx.get_set_clock_reference_source ONT2 result: [{}]".format(callResult)) 
         
    return(callResult)
            
        
def formatDate():
    # format date and time
    today = time.localtime(time.time())
    theDate = time.strftime("%A %B %d", today)
    now = time.ctime()
    parsed = time.strptime(now)
    #formatDate = time.strftime("%a_%b_%d_%Y_%H_%M_%S ", parsed)
    formatDate = time.strftime("%b_%d_%Y_%H_%M_%S", parsed)
    #print (formatDate)
    return(formatDate)
    

def select_from(rate, au_type, ne_s1):
    conn_from = rate + au_type + "-" + ne_s1 + "-1"
    return(conn_from)


def select_to(rate, au_type, ne_s2, n_conn, conc_factor):
    conn_to = []
    for i in range(1, (n_conn + 1)):
        conn_to = conn_to + [rate + au_type + "-" + ne_s2 + "-" + str(i + conc_factor)]
        
    return(conn_to)


def ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, sec):
    ONT1.start_measurement(ONT1_P1)
    ONT2.start_measurement(ONT2_P1)
    time.sleep(sec)
    ONT1.halt_measurement(ONT1_P1)
    ONT2.halt_measurement(ONT2_P1)
    return


def enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, enable, mode):
    """
    Input value:
    enable = Y or N
    mode = 1W or 2W
    """
    res_from = True
    res_to = True
    
    for i in range(len(conn_to)):
        tl1_cmd = "ED-" + au_type + "::" + conn_to[i] + "::::POM=" + enable + ",EGPOM=" + enable + ",CMDMDE=FRCD;"
        res_tl1_cmd = NE1.tl1.do(tl1_cmd)
        if(res_tl1_cmd == True):
            tl1_string_out = NE1.tl1.get_last_outcome()
            print(tl1_string_out)
            res_to = True
        else:
            res_to = False
            break

    if(mode == "2W"):
        tl1_cmd = "ED-" + au_type + "::" + conn_from + "::::POM=" + enable + ",EGPOM=" + enable + ",CMDMDE=FRCD;"
        res_tl1_cmd = NE1.tl1.do(tl1_cmd)
        if(res_tl1_cmd == True):
            tl1_string_out = NE1.tl1.get_last_outcome()
            print(tl1_string_out)
            res_from = True
        else:
            res_from = False

    return((res_to and res_from))
    

def check_UNEQ_alarm(NE1):
    """
    Return Value: UNEQ-P or NO_UNEQ-P string
    """
    
    check_res = "UNEQ-P"
    
    tl1_cmd = "RTRV-COND-ALL:::::UNEQ-P;"
    res_tl1_cmd = NE1.tl1.do(tl1_cmd)
    if(res_tl1_cmd == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out)
        tl1_msg_out = TL1message(tl1_string_out)
        tl1_len = tl1_msg_out.get_cmd_response_size()
        if(tl1_len ==  0):
            check_res = "NO_UNEQ-P"
        else:
            check_res = "UNEQ-P"
    
    return(check_res)   
    
    
def test_conn_join(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, conn_from, conn_to):
    
    test_res = False
    
    # Join the connection
    tl1_command = "CNVT-CCJ-" + vc_type + "::" + conn_to[0] + ";"
    res_tl1_cmd = NE1.tl1.do(tl1_command)
    if(res_tl1_cmd == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out)
        time.sleep(5)
        # Start ONT measurement and check alarms
        ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
        alr_ho_ont1_res = ONT1.retrieve_ho_alarms(ONT1_P1)
        alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
        if(((alr_ho_ont1_res[0] == True) and (len(alr_ho_ont1_res[1]) == 0)) and
           ((alr_ho_ont2_res[0] == True) and (len(alr_ho_ont2_res[1]) == 0))):
            # check Cross Connection primary state PST
            tl1_command = "RTRV-CRS-" + vc_type + "::" + conn_from + ";"
            res_tl1_cmd = NE1.tl1.do(tl1_command)
            if(res_tl1_cmd == True):
                tl1_string_out = NE1.tl1.get_last_outcome()
                print(tl1_string_out)
                tl1_msg_out = TL1message(tl1_string_out)
                aid_list = tl1_msg_out.get_cmd_aid_list()
                pst1 = tl1_msg_out.get_cmd_pst(aid_list[0])
                if(pst1[0][0] == "IS-NR"):
                    # Check if UNEQ-P
                    res_check_UNEQ = check_UNEQ_alarm(NE1)
                    if(res_check_UNEQ == "NO_UNEQ-P"):
                        test_res = True
    
    return(test_res)


def test_conn_split(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, conn_from, conn_to):
    """
    Return Value:
    split_done = 0  CNVT-CCS Command Failed
    split_done = 1  RTRV-CRS Command Failed
    split_done = 2  ONT Alarms
    split_done = 3  Success
    split_done = 4  UNEQ-P Alarm
    """
    
    split_done = 0
    
    # Split the connection
    tl1_command = "CNVT-CCS-" + vc_type + "::" + conn_from + ";"
    res_tl1_cmd = NE1.tl1.do(tl1_command)
    if(res_tl1_cmd == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out)
        time.sleep(5)
        
        # Start ONT measurement and check alarms
        ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
        alr_ho_ont1_res = ONT1.retrieve_ho_alarms(ONT1_P1)
        alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
        if(((alr_ho_ont1_res[0] == True) and (len(alr_ho_ont1_res[1]) == 0)) and
           ((alr_ho_ont2_res[0] == True) and (len(alr_ho_ont2_res[1]) == 0))):
            
            # check Cross Connection primary state PST
            tl1_command = "RTRV-CRS-" + vc_type + "::" + conn_from + ";"
            res_tl1_cmd = NE1.tl1.do(tl1_command)
            if(res_tl1_cmd == True):
                tl1_string_out = NE1.tl1.get_last_outcome()
                print(tl1_string_out)
                tl1_msg_out = TL1message(tl1_string_out)
                aid_list = tl1_msg_out.get_cmd_aid_list()
                pst1 = tl1_msg_out.get_cmd_pst(aid_list[0])
                pst2 = tl1_msg_out.get_cmd_pst(aid_list[1])
                if((pst1[0][0] == "IS-NR") and (pst2[0][0] == "IS-NR")):
                    
                    # Check if UNEQ-P
                    res_check_UNEQ = check_UNEQ_alarm(NE1)
                    if(res_check_UNEQ == "NO_UNEQ-P"):
                        split_done = 3
                    else:
                        split_done = 4
            else:
                split_done = 1
        else:  
            split_done = 2
                    
    return(split_done)
    

def test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2):
    
    test_ok = False
    
    # Check alarms on ONT1 and ONT2
    ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
    alr_ho_ont1_res = ONT1.retrieve_ho_alarms(ONT1_P1)
    alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
    if((alr_ho_ont1_res[0] == True) and (alr_ho_ont2_res[0] == True)):
        alr_ho_ont1_list = alr_ho_ont1_res[1]
        alr_ho_ont2_list = alr_ho_ont2_res[1]
        if((alr_ho_ont1_list[0] == "HP-UNEQ") and (alr_ho_ont2_list[0] == "HP-UNEQ")):
            
            # Enable POM and check UNEQ-P alarms on NE by RTRV-COND-ALL command
            conn_from = select_from(rate, au_type, ne_s1)
            conn_to = select_to("STM64", au_type, ne_s2, 1, 0)
            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "Y", "2W")
            time.sleep(5)
            res_check_UNEQ = check_UNEQ_alarm(NE1)
            if(res_check_UNEQ == "UNEQ-P"):
                
                # Do Cross Connection and check
                tl1_command = "ENT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                res_tl1_cmd = NE1.tl1.do(tl1_command)
                if(res_tl1_cmd == True):
                    tl1_string_out = NE1.tl1.get_last_outcome()
                    print(tl1_string_out)
                    time.sleep(5)
                    
                    # Check alarms on ONT
                    ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
                    alr_ho_ont1_res = ONT1.retrieve_ho_alarms(ONT1_P1)
                    alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
                    if(((alr_ho_ont1_res[0] == True) and (len(alr_ho_ont1_res[1]) == 0)) and
                       ((alr_ho_ont2_res[0] == True) and (len(alr_ho_ont2_res[1]) == 0))):
                        
                        # check Cross Connection primary state PST
                        tl1_command = "RTRV-CRS-" + vc_type + "::" + conn_from + ";"
                        res_tl1_cmd = NE1.tl1.do(tl1_command)
                        if(res_tl1_cmd == True):
                            tl1_string_out = NE1.tl1.get_last_outcome()
                            print(tl1_string_out)
                            tl1_msg_out = TL1message(tl1_string_out)
                            aid_list = tl1_msg_out.get_cmd_aid_list()
                            pst = tl1_msg_out.get_cmd_pst(aid_list[0])
                            if(pst[0][0] == "IS-NR"):
                                
                                # Check if UNEQ-P
                                res_check_UNEQ = check_UNEQ_alarm(NE1)
                                if(res_check_UNEQ == "NO_UNEQ-P"):
                                    self.add_success(NE1, "Conn 2W", "0", "- SUCCESS: Conn 2W - [{}] - [{}] - [{}]".format(rate, au_type, vc_type))
                                    time.sleep(5)
                                    
                                    # Test SPLIT CONN
                                    split_res = test_conn_split(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, conn_from, conn_to)
                                    if(split_res == 3):
                                        self.add_success(NE1, "SPLIT", "0", "- SUCCESS: SPLIT - [{}] - [{}] - [{}]".format(rate, au_type, vc_type))
                                        time.sleep(5)
                                        
                                        # Test JOIN CONN
                                        join_res = test_conn_join(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, conn_from, conn_to)
                                        if(join_res == True):
                                            self.add_success(NE1, "JOIN", "0", "- SUCCESS: JOIN - [{}] - [{}] - [{}]".format(rate, au_type, vc_type))
                                            time.sleep(5)
                                            
                                            # Delete Cross Connection
                                            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")    
                                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                                            if(res_tl1_cmd == True):
                                                tl1_string_out = NE1.tl1.get_last_outcome()
                                                print(tl1_string_out)
                                                test_ok = True
                                            else:
                                                local_deb = Debug_Line_Function()
                                                self.add_failure(NE1, "DLT-CRS ", "0", "DLT-CRS Failed", local_deb)
                                                print(local_deb)
                                                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                                                tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                                                res_tl1_cmd = NE1.tl1.do(tl1_command)
                                                if(res_tl1_cmd == True):
                                                    tl1_string_out = NE1.tl1.get_last_outcome()
                                                    print(tl1_string_out)
                                        else:
                                            local_deb = Debug_Line_Function()
                                            self.add_failure(NE1, "JOIN ", "0", "JOIN Failed", local_deb)
                                            print(local_deb)
                                            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                                            if(res_tl1_cmd == True):
                                                tl1_string_out = NE1.tl1.get_last_outcome()
                                                print(tl1_string_out)  
                                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_to[0] + "," + conn_from + ":::" + "1WAY;"
                                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                                            if(res_tl1_cmd == True):
                                                tl1_string_out = NE1.tl1.get_last_outcome()
                                                print(tl1_string_out)  
                                    else:
                                        local_deb = Debug_Line_Function()
                                        self.add_failure(NE1, "SPLIT ", "0", "SPLIT Failed", local_deb)
                                        print(local_deb)
                                        enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                                        if(split_res == 0):
                                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                                            if(res_tl1_cmd == True):
                                                tl1_string_out = NE1.tl1.get_last_outcome()
                                                print(tl1_string_out)
                                        else:
                                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                                            if(res_tl1_cmd == True):
                                                tl1_string_out = NE1.tl1.get_last_outcome()
                                                print(tl1_string_out)  
                                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_to[0] + "," + conn_from + ":::" + "1WAY;"
                                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                                            if(res_tl1_cmd == True):
                                                tl1_string_out = NE1.tl1.get_last_outcome()
                                                print(tl1_string_out)  
                                else:
                                    local_deb = Debug_Line_Function()
                                    self.add_failure(NE1, "Check UNEQ-P ", "0", "Check UNEQ-P Failed", local_deb)
                                    print(local_deb)
                                    enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                                    tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                                    res_tl1_cmd = NE1.tl1.do(tl1_command)
                                    if(res_tl1_cmd == True):
                                        tl1_string_out = NE1.tl1.get_last_outcome()
                                        print(tl1_string_out)
                            else:
                                local_deb = Debug_Line_Function()
                                self.add_failure(NE1, "Check IS-NR ", "0", "Check IS-NR Failed", local_deb)
                                print(local_deb)
                                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                                tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                                res_tl1_cmd = NE1.tl1.do(tl1_command)
                                if(res_tl1_cmd == True):
                                    tl1_string_out = NE1.tl1.get_last_outcome()
                                    print(tl1_string_out)
                        else:
                            local_deb = Debug_Line_Function()
                            self.add_failure(NE1, "RTRV-CRS ", "0", "RTRV-CRS Failed", local_deb)
                            print(local_deb)
                            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                            if(res_tl1_cmd == True):
                                tl1_string_out = NE1.tl1.get_last_outcome()
                                print(tl1_string_out)
                    else:
                        local_deb = Debug_Line_Function()
                        self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
                        print(local_deb)
                        enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
                        tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "2WAY;"
                        res_tl1_cmd = NE1.tl1.do(tl1_command)
                        if(res_tl1_cmd == True):
                            tl1_string_out = NE1.tl1.get_last_outcome()
                            print(tl1_string_out)
                else:
                    local_deb = Debug_Line_Function()
                    self.add_failure(NE1, "ENT-CRS ", "0", "ENT-CRS Failed", local_deb)
                    print(local_deb)
                    enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
            else:
                local_deb = Debug_Line_Function()
                self.add_failure(NE1, "Enable POM and Check UNEP-P ", "0", "Enable POM and Check UNEQ-P Failed", local_deb)
                print(local_deb)
                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "2W")
        else:
            local_deb = Debug_Line_Function()
            self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
            print(local_deb)
    else:
        local_deb = Debug_Line_Function()
        self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
        print(local_deb)
        
    return(test_ok)


def test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2):
    
    test_ok = False
    
    # Check alarms on ONT1 and ONT2
    ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
    alr_ho_ont1_res = ONT1.retrieve_ho_alarms(ONT1_P1)
    alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
    if((alr_ho_ont1_res[0] == True) and (alr_ho_ont2_res[0] == True)):
        alr_ho_ont1_list = alr_ho_ont1_res[1]
        alr_ho_ont2_list = alr_ho_ont2_res[1]
        if((alr_ho_ont1_list[0] == "HP-UNEQ") and (alr_ho_ont2_list[0] == "HP-UNEQ")):
            
            # Enable POM and check UNEQ-P alarms on NE by RTRV-COND-ALL command
            conn_from = select_from(rate, au_type, ne_s1)
            conn_to = select_to("STM64", au_type, ne_s2, 1, 0)
            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "Y", "1W")
            time.sleep(5)
            res_check_UNEQ = check_UNEQ_alarm(NE1)
            if(res_check_UNEQ == "UNEQ-P"):
                
                # Do Cross Connection and check
                tl1_command = "ENT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                res_tl1_cmd = NE1.tl1.do(tl1_command)
                if(res_tl1_cmd == True):
                    tl1_string_out = NE1.tl1.get_last_outcome()
                    print(tl1_string_out)
                    time.sleep(5)
                    ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
                    alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
                    if((alr_ho_ont2_res[0] == True) and (len(alr_ho_ont2_res[1]) == 0)):
                        
                        # check Cross Connection primary state PST
                        tl1_command = "RTRV-CRS-" + vc_type + "::" + conn_from + ";"
                        res_tl1_cmd = NE1.tl1.do(tl1_command)
                        if(res_tl1_cmd == True):
                            tl1_string_out = NE1.tl1.get_last_outcome()
                            print(tl1_string_out)
                            tl1_msg_out = TL1message(tl1_string_out)
                            aid_list = tl1_msg_out.get_cmd_aid_list()
                            pst = tl1_msg_out.get_cmd_pst(aid_list[0])
                            if(pst[0][0] == "IS-NR"):
                                
                                # Check if UNEQ-P
                                res_check_UNEQ = check_UNEQ_alarm(NE1)
                                if(res_check_UNEQ == "NO_UNEQ-P"):

                                    # Delete Cross Connection
                                    enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")    
                                    tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                                    res_tl1_cmd = NE1.tl1.do(tl1_command)
                                    if(res_tl1_cmd == True):
                                        tl1_string_out = NE1.tl1.get_last_outcome()
                                        print(tl1_string_out)
                                        test_ok = True
                                    else:
                                        local_deb = Debug_Line_Function()
                                        self.add_failure(NE1, "DLT-CRS ", "0", "DLT-CRS Failed", local_deb)
                                        print(local_deb)
                                        enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
                                        tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                                        res_tl1_cmd = NE1.tl1.do(tl1_command)
                                        if(res_tl1_cmd == True):
                                            tl1_string_out = NE1.tl1.get_last_outcome()
                                            print(tl1_string_out)
                                else:
                                    local_deb = Debug_Line_Function()
                                    self.add_failure(NE1, "Check UNEQ-P ", "0", "Check UNEQ-P Failed", local_deb)
                                    print(local_deb)
                                    enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
                                    tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                                    res_tl1_cmd = NE1.tl1.do(tl1_command)
                                    if(res_tl1_cmd == True):
                                        tl1_string_out = NE1.tl1.get_last_outcome()
                                        print(tl1_string_out)
                            else:
                                local_deb = Debug_Line_Function()
                                self.add_failure(NE1, "Check IS-NR ", "0", "Check IS-NR Failed", local_deb)
                                print(local_deb)
                                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
                                tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                                res_tl1_cmd = NE1.tl1.do(tl1_command)
                                if(res_tl1_cmd == True):
                                    tl1_string_out = NE1.tl1.get_last_outcome()
                                    print(tl1_string_out)
                        else:
                            local_deb = Debug_Line_Function()
                            self.add_failure(NE1, "RTRV-CRS ", "0", "RTRV-CRS Failed", local_deb)
                            print(local_deb)
                            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
                            tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                            res_tl1_cmd = NE1.tl1.do(tl1_command)
                            if(res_tl1_cmd == True):
                                tl1_string_out = NE1.tl1.get_last_outcome()
                                print(tl1_string_out)
                    else:
                        local_deb = Debug_Line_Function()
                        self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms", local_deb)
                        print(local_deb)
                        enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
                        tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[0] + ":::" + "1WAY;"
                        res_tl1_cmd = NE1.tl1.do(tl1_command)
                        if(res_tl1_cmd == True):
                            tl1_string_out = NE1.tl1.get_last_outcome()
                            print(tl1_string_out)
                else:
                    local_deb = Debug_Line_Function()
                    self.add_failure(NE1, "ENT-CRS ", "0", "ENT-CRS Failed", local_deb)
                    print(local_deb)
                    enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
            else:
                local_deb = Debug_Line_Function()
                self.add_failure(NE1, "Enable POM and Check UNEQ-P ", "0", "Enable POM and Check UNEQ-P Failed", local_deb)
                print(local_deb)
                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
        else:
            local_deb = Debug_Line_Function()
            self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
            print(local_deb)
    else:
        local_deb = Debug_Line_Function()
        self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
        print(local_deb)
        
    return(test_ok)


def test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, n_conn, conc_factor):
    
    pass_1 = False; pass_2 = False; pass_3 = False; pass_4 = False; pass_5 = False;
    pass_6 = False; pass_7 = False; pass_8 = False; pass_9 = False;
    
    # Check alarms on ONT1 and ONT2
    ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
    alr_ho_ont1_res = ONT1.retrieve_ho_alarms(ONT1_P1)
    alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
    if((alr_ho_ont1_res[0] == True) and (alr_ho_ont2_res[0] == True)):
        pass_1 = True
        alr_ho_ont1_list = alr_ho_ont1_res[1]
        alr_ho_ont2_list = alr_ho_ont2_res[1]
        if((alr_ho_ont1_list[0] == "HP-UNEQ") and (alr_ho_ont2_list[0] == "HP-UNEQ")):
            pass_2 = True
            # Enable POM and check UNEQ-P alarms on NE by RTRV-COND-ALL command
            conn_from = select_from(rate, au_type, ne_s1)
            conn_to = select_to("STM64", au_type, ne_s2, n_conn, conc_factor)
            enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "Y", "1W")
            time.sleep(5)
            res_check_UNEQ = check_UNEQ_alarm(NE1)
            if(res_check_UNEQ == "UNEQ-P"):
                pass_3 = True
                # Do Cross Connection and check ONT alarms
                for i in range(len(conn_to)):                   
                    tl1_command = "ENT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[i] + ":::" + "1WAY;"
                    res_tl1_cmd = NE1.tl1.do(tl1_command)
                    if(res_tl1_cmd == True):
                        pass_4 = True
                        tl1_string_out = NE1.tl1.get_last_outcome()
                        print(tl1_string_out)
                        time.sleep(2)
                        ONT2.get_set_rx_measure_channel(ONT2_P1, str(i+1))
                        ont_measurement(ONT1, ONT2, ONT1_P1, ONT2_P1, 2)
                        alr_ho_ont2_res = ONT2.retrieve_ho_alarms(ONT2_P1)
                        if((alr_ho_ont2_res[0] == True) and (len(alr_ho_ont2_res[1]) == 0)):
                            pass_5 = True
                        else:
                            pass_5 = False
                            local_deb = Debug_Line_Function()
                            self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
                            print(local_deb)
                            break                           
                    else:
                        pass_4 = False
                        local_deb = Debug_Line_Function()
                        self.add_failure(NE1, "ENT-CRS ", "0", "ENT-CRS Command Failed", local_deb)
                        print(local_deb)
                        break                                            

                # check Cross Connection primary state
                tl1_command = "RTRV-CRS-" + vc_type + "::" + conn_from + ";"
                res_tl1_cmd = NE1.tl1.do(tl1_command)
                if(res_tl1_cmd == True):
                    pass_6 = True
                    tl1_string_out = NE1.tl1.get_last_outcome()
                    print(tl1_string_out)
                    tl1_msg_out = TL1message(tl1_string_out)
                    aid_list = tl1_msg_out.get_cmd_aid_list()
                    pst = tl1_msg_out.get_cmd_pst(aid_list[0])
                    if(pst[0][0] == "IS-NR"):
                        pass_7 = True        
                        # Check if UNEQ-P
                        res_check_UNEQ = check_UNEQ_alarm(NE1)
                        if(res_check_UNEQ == "NO_UNEQ-P"):
                            pass_8 = True
                        else:
                            local_deb = Debug_Line_Function()
                            self.add_failure(NE1, "Check UNEQ-P ", "0", "Check UNEQ-P Failed", local_deb)
                            print(local_deb)
                    else:
                        local_deb = Debug_Line_Function()
                        self.add_failure(NE1, "Check IS-NR ", "0", "Check IS-NR Failed", local_deb)
                        print(local_deb)
                else:
                    local_deb = Debug_Line_Function()
                    self.add_failure(NE1, "RTRV-CRS ", "0", "RTRV-CRS Command Failed", local_deb)
                    print(local_deb)
                                
                # Disable POM and Delete Cross Connection
                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
                for i in range(len(conn_to)):    
                    tl1_command = "DLT-CRS-" + vc_type + "::" + conn_from + "," + conn_to[i] + ":::" + "1WAY;"
                    res_tl1_cmd = NE1.tl1.do(tl1_command)
                    if(res_tl1_cmd == True):
                        pass_9 = True
                        tl1_string_out = NE1.tl1.get_last_outcome()
                        print(tl1_string_out)
                        time.sleep(2)
                    else:
                        pass_9 = False
                        local_deb = Debug_Line_Function()
                        self.add_failure(NE1, "DLT-CRS ", "0", "DLT-CRS Command Failed", local_deb)
                        print(local_deb)
                        break     
            else:
                local_deb = Debug_Line_Function()
                self.add_failure(NE1, "Enable POM and Check UNEQ-P ", "0", "Enable POM and Check UNEQ-P Failed", local_deb)
                print(local_deb)
                enable_dis_POM(NE1, rate, vc_type, au_type, conn_from, conn_to, "N", "1W")
        else:
            local_deb = Debug_Line_Function()
            self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
            print(local_deb)
    else:
        local_deb = Debug_Line_Function()
        self.add_failure(NE1, "Check ONT Alarms ", "0", "Check ONT Alarms Failed", local_deb)
        print(local_deb)
        
    return(pass_1 and pass_2 and pass_3 and pass_4 and pass_5 and pass_6 and pass_7 and pass_8 and pass_9)


def setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, n_conn):
    
    callResult = True
    conc_factor = 0
    chan_map = vc_type[0:3] + "_" + vc_type[3:]
    
    callResult = ONT1.get_set_rx_channel_mapping_size(ONT1_P1, chan_map)
    print("ONT5xx.get_set_rx_channel_mapping_size ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_rx_channel_mapping_size(ONT2_P1, chan_map)
    print("ONT5xx.get_set_rx_channel_mapping_size ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_tx_channel_mapping_size(ONT1_P1, chan_map)
    print("ONT5xx.get_set_tx_channel_mapping_size ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_tx_channel_mapping_size(ONT2_P1, chan_map)
    print("ONT5xx.get_set_tx_channel_mapping_size ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)
    
    if((rate == "STM4") and (vc_type == "VC44C")):
        hostruct_s1 = "1xAU44C;"
        hostruct_s2 = "1xAU44C-60xAU4;"
        conc_factor = 4
    elif((rate == "STM16") and (vc_type == "VC44C")):
        hostruct_s1 = "1xAU44C-12xAU4;"
        hostruct_s2 = "1xAU44C-60xAU4;"
        conc_factor = 4
    elif((rate == "STM16") and (vc_type == "VC416C")):
        hostruct_s1 = "1xAU416C;"
        hostruct_s2 = "1xAU416C-48xAU4;"
        conc_factor = 16
    elif((rate == "STM64") and (vc_type == "VC44C")):
        hostruct_s1 = "1xAU44C-60xAU4;"
        hostruct_s2 = "1xAU44C-60xAU4;"
        conc_factor = 4
    elif((rate == "STM64") and (vc_type == "VC416C")):
        hostruct_s1 = "1xAU416C-48xAU4;"
        hostruct_s2 = "1xAU416C-48xAU4;"
        conc_factor = 16
    else:
        hostruct_s1= "1xAU464C;"
        hostruct_s1= "1xAU464C;"
        conc_factor = 64
    
    tl1_command= "ED-" + rate + "::" + rate + "-" + ne_s1 + "::::" + "CMDMDE=FRCD,HOSTRUCT=" + hostruct_s1
    callResult = NE1.tl1.do(tl1_command)
    if(callResult == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out)
        
    tl1_command= "ED-STM64::STM64-" + ne_s2 + "::::" + "CMDMDE=FRCD,HOSTRUCT=" + hostruct_s2
    callResult = NE1.tl1.do(tl1_command)
    if(callResult == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out)        
    
    return(conc_factor)
       
    
def default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2):
    
    callResult = True
    
    callResult = ONT1.get_set_rx_channel_mapping_size(ONT1_P1, "VC4")
    print("ONT5xx.get_set_rx_channel_mapping_size ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_rx_channel_mapping_size(ONT2_P1, "VC4")
    print("ONT5xx.get_set_rx_channel_mapping_size ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT1.get_set_tx_channel_mapping_size(ONT1_P1, "VC4")
    print("ONT5xx.get_set_tx_channel_mapping_size ONT1 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)

    callResult = ONT2.get_set_tx_channel_mapping_size(ONT2_P1, "VC4")
    print("ONT5xx.get_set_tx_channel_mapping_size ONT2 result: [{}]".format(callResult))
    if(callResult == False):
        return(callResult)
    
    if(rate == "STM4"):
        hostruct = "4xAU4;"
    elif(rate == "STM16"):
        hostruct = "16xAU4;"
    else:
        hostruct = "64xAU4;"

    tl1_command= "ED-" + rate + "::" + rate + "-" + ne_s1 + "::::" + "CMDMDE=FRCD,HOSTRUCT=" + hostruct
    callResult = NE1.tl1.do(tl1_command)
    if(callResult == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out)
    else:
        return(callResult)
    
    tl1_command= "ED-STM64::STM64-" + ne_s2 + "::::" + "CMDMDE=FRCD,HOSTRUCT=64xAU4"
    callResult = NE1.tl1.do(tl1_command)
    if(callResult == True):
        tl1_string_out = NE1.tl1.get_last_outcome()
        print(tl1_string_out) 
    else:
        return(callResult)       

    return(callResult)
        

def verify_conn_2w_split_join(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2):
    '''
    Verify the cross-connection 2 Way, Split and Join commands, for any rate, VC type and AU type, as 
    described in cap. 5.3.3.x, 5.3.26.x, 5.3.28.x of Cross Connection (CONN) TPS
    '''
 
    test_result = False
    
    if(rate == "STM1"):
        test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        
    elif(rate == "STM4"):
        if(vc_type == "VC44C"):
            setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        
    elif(rate == "STM16"):
        if((vc_type == "VC44C") or (vc_type == "VC416C")):
            setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        
    elif(rate == "STM64"):
        if((vc_type == "VC44C") or (vc_type == "VC416C") or (vc_type == "VC464C")):
            setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_2w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)     
    else:
        print("*****  Wrong Rate value!!!")
        
    return(test_result)


def verify_conn_1w_tps534x(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2):
    '''
    Verify the cross-connection 1 Way, for any rate, VC type and AU type,
    as described in cap. 5.3.4.x of Cross Connection (CONN) TPS
    '''
 
    test_result = False
    
    if(rate == "STM1"):
        test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        
    elif(rate == "STM4"):
        if(vc_type == "VC44C"):
            setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        
    elif(rate == "STM16"):
        if((vc_type == "VC44C") or (vc_type == "VC416C")):
            setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        
    elif(rate == "STM64"):
        if((vc_type == "VC44C") or (vc_type == "VC416C") or (vc_type == "VC464C")):
            setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_1w(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)     
    else:
        print("*****  Wrong Rate value!!!")
        
    return(test_result)


def verify_conn_br_tps536x(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2):
    '''
    Verify the cross-connection broadcast for any rate, VC type and AU type, as described 
    in cap. 5.3.6.x of Cross Connection (CONN) TPS
    '''

    test_result = True
    
    if(rate == "STM1"):
        test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 64, 0)
        
    elif(rate == "STM4"):
        if(vc_type == "VC44C"):
            conc_factor = setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 16)
            test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 16, conc_factor)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 64, 0)
        
    elif(rate == "STM16"):
        if((vc_type == "VC44C") or (vc_type == "VC416C")):
            conc_factor = setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 4)
            test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 4, conc_factor)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 64, 0)
        
    elif(rate == "STM64"):
        if((vc_type == "VC44C") or (vc_type == "VC416C") or (vc_type == "VC464C")):
            conc_factor = setup_vc_conc(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1)
            test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 1, conc_factor)
            default_vc_type(NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2)
        else:
            test_result = test_conn_br(self, NE1, ONT1, ONT2, ONT1_P1, ONT2_P1, rate, vc_type, au_type, ne_s1, ne_s2, 64, 0)     
    else:
        print("*****  Wrong Rate value!!!")
    
    return(test_result)
