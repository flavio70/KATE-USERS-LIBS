#!/usr/bin/env python
'''
.. module::FmLib
   :platform: Unix
   :synopsis:This module provides common functions for test cases implemtation.
   
.. moduleauthor:: Mario Pio Lindo Tosi <Mario.Tosi@sm-optics.com>
 
'''

from katelibs.testcase          import TestCase
from katelibs.eqpt1850tss320    import Eqpt1850TSS320
from katelibs.instrumentONT     import InstrumentONT
from katelibs.swp1850tss320     import SWP1850TSS
from katelibs.facility_tl1      import *
import time
from inspect import currentframe

global E_LO_MTX 
global E_MAX_MVC4 
global E_TIMEOUT 

global E_RFI_NUM 
global E_BLOCK_SIZE         
global E_WAIT 

E_MAX_MVC4 = 384
E_LO_MTX = "MXH60GLO"
E_TIMEOUT = 20

E_RFI_NUM = 2
E_BLOCK_SIZE = 64        
E_WAIT = 10

def dprint(zq_str,zq_level):
    '''
    # print debug level:  0=no print
    #                     1=TL1 message response
    #                     2=OK/KO info 
    #                     4=execution info
    # can be used in combination, i.e.
    #                     3=TL1 message response+OK/KO info
    # 
    '''
    E_DPRINT = 7    
    
    if (E_DPRINT & zq_level):
        print(zq_str)
    return

def QS_000_Print_Line_Function(zq_gap=0):
    """ Return a text string referencing the line number and the function in which it is called. Can be used to add
        trace informations when errors occurs.
        
    :param zq_gap: line reference offset.

     >>> Test1.add_failure(NE1,'MyTitle','0.0','some output text','some output text'+QS_000_Print_Line_Function()))


    """

    cf = currentframe()
    zq_line = cf.f_back.f_lineno + zq_gap
    zq_code = str(cf.f_back.f_code)
    zq_temp = zq_code.split(",")
    zq_function = zq_temp[0].split(" ")
    zq_res = "****** Line [{}] in function [{}]".format(zq_line,zq_function[2])
    
    return zq_res


def QS_010_Create_HO_XC_Block(zq_run, NE1, zq_slot, zq_start_block, zq_block_size, zq_xc_list):
    '''
    # Create zq_block_size HO cross-connection between STM1AU4x and LOPOOL
    # 
    # 
    '''
    zq_i = zq_start_block
    while zq_i < (zq_start_block+zq_block_size):
        zq_tl1_res=NE1.tl1.do("ENT-CRS-VC4::STM64AU4-{}-{},LOPOOL-1-1-1;".format(zq_slot,zq_i))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            zq_xc_list.append(''.join(zq_msg.get_cmd_aid_list()))
            zq_j = zq_xc_list.index(''.join(zq_msg.get_cmd_aid_list()))
            dprint("\nOK\tCross-connection creation successfull {}".format(zq_xc_list[zq_j]),2)
            zq_run.add_success(NE1, "Cross-connection creation successfull {}".format(zq_xc_list[zq_j]),"0.0", "Cross-connection creation successfull")
            
        else:
            if zq_cmd[1]== 'COMPLD':    
                dprint("\nKO\tCross-connection creation failed {}\n".format(zq_xc_list[zq_j]),2)
                zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", "Cross-connection creation failure " + QS_000_Print_Line_Function())
            else:
                dprint("\nKO\tTL1 Cross-connection command DENY\n",2)
                zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", "TL1 Cross-connection command DENY " + QS_000_Print_Line_Function())
        zq_i += 1
    return


def QS_020_Delete_HO_XC_Block(zq_run, NE1, zq_slot, zq_start_block, zq_block_size, zq_xc_list):

    zq_i = zq_start_block
    while zq_i < (zq_start_block+zq_block_size):
        zq_tl1_res=NE1.tl1.do("DLT-CRS-VC4::{};".format(zq_xc_list[zq_i]))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            dprint("\nOK\tCross-connection deletion successful {}".format(zq_xc_list[zq_i]),2)
            zq_run.add_success(NE1, "Cross-connection deletion successful {}".format(zq_xc_list[zq_i]),"0.0", "Cross-connection deletion successful")
        else:    
            dprint("\nKO\tCross-connection deletion failed {}".format(zq_xc_list[zq_i]),2)
            zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", "Cross-connection deletion failed {} {}".format(zq_xc_list[zq_i],QS_000_Print_Line_Function()))
    
        zq_i += 1

    return


def QS_030_Create_LO_XC_Block(zq_run, NE1, zq_vc4_1, zq_vc4_2, zq_xc_list):
    
    zq_tu3_list=zq_xc_list[zq_vc4_1].split(',')
    zq_tu3_idx1=zq_tu3_list[1].replace('MVC4','MVC4TU3')

    zq_tu3_list=zq_xc_list[zq_vc4_2].split(',')
    zq_tu3_idx2=zq_tu3_list[1].replace('MVC4','MVC4TU3')

    for zq_j in range (1,4):
        zq_tl1_res=NE1.tl1.do("ENT-CRS-LOVC3::{}-{},{}-{}:::2WAY;".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        dprint(NE1.tl1.get_last_outcome(),1)
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            dprint("\nOK\tCross-connection successfully created from {}-{} to {}-{}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j),2)
            zq_run.add_success(NE1, "Cross-connection creation successful {}-{} to {}-{}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j),"0.0", "Cross-connection creation successful")

        else:
            dprint("\nKO\tCross-connection creation failed from {}-{} to {}-{}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j),2)
            zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", "Cross-connection creation failed from {}-{} to {}-{} {}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j,QS_000_Print_Line_Function()))

    return

def QS_040_Modify_AU4_HO_Trace_Block(zq_run, NE1, zq_slot, zq_start_block, zq_block_size, zq_trace):
    '''
    # 
    # 
    '''
    zq_i = zq_start_block
    while zq_i < (zq_start_block+zq_block_size):
        zq_tl1_res=NE1.tl1.do("ED-AU4::STM64AU4-{}-{}::::TRCEXPECTED={},EGTRCEXPECTED={};".format(zq_slot,zq_i,zq_trace,zq_trace))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            dprint("\nOK\tHO Trace Identifier changed to {} for STM64AU4-{}-{}".format(zq_trace,zq_slot,zq_i),2)
            zq_run.add_success(NE1, "HO Trace Identifier changed to {} for STM64AU4-{}-{}".format(zq_trace,zq_slot,zq_i),"0.0", "HO Trace Identifier changed")

        else:
            dprint("\nKO\tHO Trace Identifier change failure for STM64AU4-{}-{}".format(zq_slot,zq_i),2)
            zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", 
                                    "HO Trace Identifier change failure for STM64AU4-{}-{} {}".format(zq_slot,zq_i,QS_000_Print_Line_Function()))

        zq_i += 1
    return


def QS_050_Modify_MVC4_HO_Trace_Block(zq_run, NE1, zq_slot, zq_start_block, zq_block_size, zq_trace):

    zq_i = zq_start_block
    while zq_i < (zq_start_block+zq_block_size):
        zq_tl1_res=NE1.tl1.do("ED-PTF::MVC4-{}-{}::::TRC={},TRCEXPECTED={};".format(zq_slot,zq_i,zq_trace,zq_trace))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            dprint("\nOK\tHO Trace Identifier changed to {} for MVC4-{}-{}".format(zq_trace,zq_slot,zq_i),2)
            zq_run.add_success(NE1, "HO Trace Identifier changed to {} for MVC4-{}-{}".format(zq_trace,zq_slot,zq_i),"0.0", "HO Trace Identifier changed")

        else:
            dprint("\nKO\tHO Trace Identifier change failure for MVC4-{}-{}".format(zq_slot,zq_i),2)
            zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", 
            "HO Trace Identifier change failure for MVC4-{}-{} {}".format(zq_slot,zq_i,QS_000_Print_Line_Function()))
        zq_i += 1
    return


def QS_060_Delete_LO_XC_Block(zq_run, NE1, zq_vc4_1, zq_vc4_2, zq_xc_list):

    zq_tu3_list=zq_xc_list[zq_vc4_1].split(',')
    zq_tu3_idx1=zq_tu3_list[1].replace('MVC4','MVC4TU3')

    zq_tu3_list=zq_xc_list[zq_vc4_2].split(',')
    zq_tu3_idx2=zq_tu3_list[1].replace('MVC4','MVC4TU3')

    for zq_j in range (1,4):
        zq_tl1_res=NE1.tl1.do("DLT-CRS-LOVC3::{}-{},{}-{};".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        dprint(NE1.tl1.get_last_outcome(),1)
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            dprint("\nOK\tCross-connection successfully deleted from {}-{} to {}-{}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j),2)
            zq_run.add_success(NE1, "Cross-connection successfully deleted from {}-{} to {}-{}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j),"0.0", "Cross-connection successfully deleted")

        else:
            dprint("\nKO\tCross-connection deletion failed from {}-{} to {}-{}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j),2)
            zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", 
                                    "Cross-connection deletion failed from {}-{} to {}-{} {}".format(zq_tu3_idx1,zq_j,zq_tu3_idx2,zq_j,QS_000_Print_Line_Function()))

    return

def QS_070_Check_No_Alarm(zq_run, NE1, ONT, zq_ONT_p1, zq_ONT_p2, zq_vc4_ch1, zq_vc4_ch2):

    
    ONT.get_set_rx_lo_measure_channel(zq_ONT_p1, zq_vc4_ch1)
    ONT.get_set_rx_lo_measure_channel(zq_ONT_p2, zq_vc4_ch2)

    ONT.get_set_tx_lo_measure_channel(zq_ONT_p1, zq_vc4_ch1)
    ONT.get_set_tx_lo_measure_channel(zq_ONT_p2, zq_vc4_ch2)
    
    time.sleep(1)

    zq_res = False
    zq_alm1=ONT.retrieve_ho_lo_alarms(zq_ONT_p1)
    zq_alm2=ONT.retrieve_ho_lo_alarms(zq_ONT_p2)

    if zq_alm1[0] and zq_alm2[0]:
        if  len(zq_alm1[1]) == 0 and \
            len(zq_alm2[1]) == 0:
            dprint("\nOK\tPath is alarm free.",2)
            zq_run.add_success(NE1, "CHECK PATH ALARMS","0.0", "Path is alarm free")
            zq_res = True
        else:
            dprint("\nKO\tAlarms found on path: {}".format(zq_alm1[1]),2)
            dprint("\n\tAlarms found on path: {}".format(zq_alm2[1]),2)
            zq_run.add_failure(NE1, "CHECK PATH ALARMS","0.0", "PATH ALARMS FOUND"
                                  , "Path alarms found: {}-{} {}".format(zq_alm1[1],zq_alm2[1],QS_000_Print_Line_Function()))


    return  zq_res


def QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx, zq_counter_type, zq_locn, zq_period, zq_dir="RCV"):

    zq_counter = -1
    zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},0-UP,{},{},{};".format(zq_vc4_idx, zq_counter_type, zq_locn,zq_dir,zq_period))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        if zq_msg.get_cmd_response_size() != 0:
            zq_counter=zq_msg.get_cmd_attr_value("{},VC4".format(zq_vc4_idx), "2")

    return int(zq_counter[0])


def QS_090_Set_PM_Mode(zq_run, NE1, zq_vc4_idx, zq_locn, zq_mode, zq_period, zq_dir="RCV"):
    #Enable PM ALL 15-MIN and 1-DAY
    zq_tl1_res=NE1.tl1.do("SET-PMMODE-VC4::{}:::{},ALL,{},{}:TMPER={};".format(zq_vc4_idx, zq_locn, zq_mode, zq_dir,zq_period))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\tPM set to {} for {}: [{}]-[{}]-[{}]".format(zq_mode, zq_vc4_idx,zq_locn,zq_dir,zq_period),2)
        zq_run.add_success(NE1, "TL1 Command","0.0", "PM set to {} for {}: [{}]-[{}]-[{}]".format(zq_mode, zq_vc4_idx,zq_locn,zq_dir,zq_period))
    else:
        dprint("KO\tPM NOT set to {} for {}: [{}]-[{}]-[{}]".format(zq_mode, zq_vc4_idx,zq_locn,zq_dir,zq_period),2)
        zq_run.add_failure(NE1, "TL1 Command","0.0", "TL1 Command not successful", 
                                "PM set to {} for {}: [{}]-[{}]-[{}] {}".format(zq_mode, zq_vc4_idx,zq_locn,zq_dir,zq_period,QS_000_Print_Line_Function()))

    return


def QS_100_Check_BBE_ES_SES_UAS(zq_run,
                                NE1, 
                                ONT,
                                zq_ONT_p1, 
                                zq_ONT_p2, 
                                zq_mtx_slot, 
                                zq_vc4_idx1, 
                                zq_vc4_idx2, 
                                zq_locn,
                                zq_period,
                                zq_dir,
                                zq_alm_type="",
                                zq_num_err="3000",
                                zq_num_err_free="64000"):

    ##################################################
    #Verify all counters are 0 when path is alarm free
    ##################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "15-MIN")
        zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "15-MIN")
        zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "15-MIN")
        zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
        if zq_bbe == 0 and zq_es == 0 and zq_ses == 0 and zq_uas == 0:
            dprint("OK\tAll PM counter [{}]-[15-MIN] for {} are 0.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "All PM counter [{}]-[15-MIN] for {} are 0.".format(zq_locn, zq_vc4_idx1))
        else:
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                    "Some PM counter [{}]-[15-MIN] for {} not 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
            dprint("KO\tSome PM counter [{}]-[15-MIN] for {} not 0.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter BBE: {}".format(zq_bbe),2)
            dprint("\tPM counter  ES: {}".format(zq_es),2)
            dprint("\tPM counter SES: {}".format(zq_ses),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
    
    if zq_period == "BOTH" or zq_period == "1-DAY":
        if zq_locn == "BIDIR":
            zq_bbe_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-NE", zq_locn, "1-DAY")
            zq_bbe_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-FE", zq_locn, "1-DAY")
            zq_es_ne  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-NE", zq_locn, "1-DAY")
            zq_es_fe  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-FE", zq_locn, "1-DAY")
            zq_ses_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-NE", zq_locn, "1-DAY")
            zq_ses_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-FE", zq_locn, "1-DAY")
            zq_uas_bi = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
            if  zq_bbe_ne == 0 and \
                zq_bbe_fe == 0 and \
                zq_es_ne == 0 and \
                zq_es_fe == 0 and \
                zq_ses_ne == 0 and \
                zq_ses_fe == 0 and \
                zq_uas_bi == 0:
                dprint("OK\tAll PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "All PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1))
                dprint("\tPM counter BBE: {}".format(zq_bbe_fe),2)
                dprint("\tPM counter  ES: {}".format(zq_es_ne),2)
                dprint("\tPM counter  ES: {}".format(zq_es_fe),2)
                dprint("\tPM counter SES: {}".format(zq_ses_ne),2)
                dprint("\tPM counter SES: {}".format(zq_ses_fe),2)
                dprint("\tPM counter UAS: {}".format(zq_uas_bi),2)
        
        else:  
            zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "1-DAY")
            zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "1-DAY")
            zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "1-DAY")
            zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
            if zq_bbe == 0 and zq_es == 0 and zq_ses == 0 and zq_uas == 0:
                dprint("OK\tAll PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "All PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "Some PM counter [{}]-[1-DAY] for {} not 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tSome PM counter [{}]-[1-DAY] for {} not 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter BBE: {}".format(zq_bbe),2)
                dprint("\tPM counter  ES: {}".format(zq_es),2)
                dprint("\tPM counter SES: {}".format(zq_ses),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
        
    
    ###################################################################
    # Insert B3 error continuous burst 
    ###################################################################
    ONT.get_set_error_insertion_mode(zq_ONT_p1, "HO", "BURST_CONT")
    ONT.get_set_num_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err)
    ONT.get_set_num_not_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err_free)
    ONT.get_set_error_insertion_type(zq_ONT_p1, zq_alm_type)
    ONT.get_set_error_activation(zq_ONT_p1, "HO", "ON")
    time.sleep(E_TIMEOUT)
    #time.sleep(E_TIMEOUT)
    if zq_locn == "BIDIR":
        ONT.get_set_error_insertion_type(zq_ONT_p1, "HPREI")
        time.sleep(E_TIMEOUT)
        #time.sleep(E_TIMEOUT)

    ONT.get_set_error_activation(zq_ONT_p1, "HO", "OFF")
    #time.sleep(E_TIMEOUT)
    
    ###################################################################
    #Verify BBE-ES-SES counters are incremented 
    ###################################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "15-MIN")
        zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "15-MIN")
        zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "15-MIN")
        if zq_bbe != 0 and zq_es != 0 and zq_ses != 0:
            dprint("OK\tPM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1))
        else:
            dprint("KO\tPM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", 
                                    "PM Counter Reading", "PM counter [{}]-[15-MIN] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))

        dprint("\tPM counter BBE: {}".format(zq_bbe),2)
        dprint("\tPM counter  ES: {}".format(zq_es),2)
        dprint("\tPM counter SES: {}".format(zq_ses),2)

    if zq_period == "BOTH" or zq_period == "1-DAY":  
        if zq_locn == "BIDIR":
            zq_bbe_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-NE", zq_locn, "1-DAY")
            zq_bbe_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-FE", zq_locn, "1-DAY")
            zq_es_ne  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-NE", zq_locn, "1-DAY")
            zq_es_fe  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-FE", zq_locn, "1-DAY")
            zq_ses_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-NE", zq_locn, "1-DAY")
            zq_ses_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-FE", zq_locn, "1-DAY")
            if  zq_bbe_ne != 0 and \
                zq_bbe_fe != 0 and \
                zq_es_ne != 0 and \
                zq_es_fe != 0 and \
                zq_ses_ne != 0 and \
                zq_ses_fe != 0: 
                dprint("OK\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1))
            else:
                dprint("KO\tSome PM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "Some PM counter [{}]-[1-DAY] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))

            dprint("\tPM counter BBE-NE: {}".format(zq_bbe_ne),2)
            dprint("\tPM counter BBE-FE: {}".format(zq_bbe_fe),2)
            dprint("\tPM counter  ES-NE: {}".format(zq_es_ne),2)
            dprint("\tPM counter  ES-FE: {}".format(zq_es_fe),2)
            dprint("\tPM counter SES-NE: {}".format(zq_ses_ne),2)
            dprint("\tPM counter SES-FE: {}".format(zq_ses_fe),2)
        
        else:  
            zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "1-DAY")
            zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "1-DAY")
            zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "1-DAY")
            if zq_bbe != 0 and zq_es != 0 and zq_ses != 0:
                dprint("OK\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1))
            else:
                dprint("KO\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[1-DAY] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))

            dprint("\tPM counter BBE: {}".format(zq_bbe),2)
            dprint("\tPM counter  ES: {}".format(zq_es),2)
            dprint("\tPM counter SES: {}".format(zq_ses),2)

    
    ###################################################################
    # Insert B3 error continuous burst 
    ###################################################################
    # Exchange error frame number with error free number to detect UAS         
    ###################################################################
    ONT.get_set_num_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err_free)
    ONT.get_set_num_not_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err)
    ONT.get_set_error_insertion_type(zq_ONT_p1, zq_alm_type)
    ONT.get_set_error_activation(zq_ONT_p1, "HO", "ON")
    time.sleep(E_TIMEOUT)
    #time.sleep(E_TIMEOUT)
    if zq_locn == "BIDIR":
        ONT.get_set_error_insertion_type(zq_ONT_p1, "HPREI")
        time.sleep(E_TIMEOUT)
        #time.sleep(E_TIMEOUT)

    ONT.get_set_error_activation(zq_ONT_p1, "HO", "OFF")
    time.sleep(E_TIMEOUT)
    
    ###################################################################
    #Verify UAS counter is incremented 
    ###################################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
        
        if zq_uas != 0:
            dprint("OK\tPM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1))
        else:
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                    "PM counter [{}]-[15-MIN] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
            dprint("KO\tPM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
        
    if zq_period == "BOTH" or zq_period == "1-DAY":
        if zq_locn == "BIDIR":  
            zq_uas_bi = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
            if zq_uas_bi != 0:
                dprint("OK\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[1-DAY] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi),2)
            
        else:
            zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
            
            if zq_uas != 0:
                dprint("OK\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[1-DAY] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
        
    return


def QS_105_Check_BBE_ES_SES_UAS_Zero(zq_run,
                                     NE1,
                                     ONT, 
                                     zq_ONT_p1, 
                                     zq_ONT_p2, 
                                     zq_mtx_slot, 
                                     zq_vc4_idx1, 
                                     zq_vc4_idx2, 
                                     zq_locn,
                                     zq_period,
                                     zq_dir,
                                     zq_alm_type="",
                                     zq_num_err="3000",
                                     zq_num_err_free="64000"):

    ##################################################
    #Verify all counters are 0 when path is alarm free
    ##################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "15-MIN")
        zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "15-MIN")
        zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "15-MIN")
        zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
        if zq_bbe == 0 and zq_es == 0 and zq_ses == 0 and zq_uas == 0:
            dprint("OK\tAll PM counter [{}]-[15-MIN] for {} are 0.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "All PM counter [{}]-[15-MIN] for {} are 0.".format(zq_locn, zq_vc4_idx1))
        else:
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                    "Some PM counter [{}]-[15-MIN] for {} not 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
            dprint("KO\tSome PM counter [{}]-[15-MIN] for {} not 0.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter BBE: {}".format(zq_bbe),2)
            dprint("\tPM counter  ES: {}".format(zq_es),2)
            dprint("\tPM counter SES: {}".format(zq_ses),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
    
    if zq_period == "BOTH" or zq_period == "1-DAY":
        if zq_locn == "BIDIR":
            zq_bbe_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-NE", zq_locn, "1-DAY")
            zq_bbe_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-FE", zq_locn, "1-DAY")
            zq_es_ne  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-NE", zq_locn, "1-DAY")
            zq_es_fe  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-FE", zq_locn, "1-DAY")
            zq_ses_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-NE", zq_locn, "1-DAY")
            zq_ses_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-FE", zq_locn, "1-DAY")
            zq_uas_bi = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
            if  zq_bbe_ne == 0 and \
                zq_bbe_fe == 0 and \
                zq_es_ne == 0 and \
                zq_es_fe == 0 and \
                zq_ses_ne == 0 and \
                zq_ses_fe == 0 and \
                zq_uas_bi == 0:
                dprint("OK\tAll PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "All PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1))
                dprint("\tPM counter BBE: {}".format(zq_bbe_fe),2)
                dprint("\tPM counter  ES: {}".format(zq_es_ne),2)
                dprint("\tPM counter  ES: {}".format(zq_es_fe),2)
                dprint("\tPM counter SES: {}".format(zq_ses_ne),2)
                dprint("\tPM counter SES: {}".format(zq_ses_fe),2)
                dprint("\tPM counter UAS: {}".format(zq_uas_bi),2)
        
        else:  
            zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "1-DAY")
            zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "1-DAY")
            zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "1-DAY")
            zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
            if zq_bbe == 0 and zq_es == 0 and zq_ses == 0 and zq_uas == 0:
                dprint("OK\tAll PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "All PM counter [{}]-[1-DAY] for {} are 0.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "Some PM counter [{}]-[1-DAY] for {} not 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tSome PM counter [{}]-[1-DAY] for {} not 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter BBE: {}".format(zq_bbe),2)
                dprint("\tPM counter  ES: {}".format(zq_es),2)
                dprint("\tPM counter SES: {}".format(zq_ses),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
        
    
    ###################################################################
    # Insert B3 error continuous burst 
    ###################################################################
    ONT.get_set_error_insertion_mode(zq_ONT_p1, "HO", "BURST_CONT")
    ONT.get_set_num_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err)
    ONT.get_set_num_not_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err_free)
    ONT.get_set_error_insertion_type(zq_ONT_p1, zq_alm_type)
    ONT.get_set_error_activation(zq_ONT_p1, "HO", "ON")
    time.sleep(E_TIMEOUT)
    #time.sleep(E_TIMEOUT)
    if zq_locn == "BIDIR":
        ONT.get_set_error_insertion_type(zq_ONT_p1, "HPREI")
        time.sleep(E_TIMEOUT)
        #time.sleep(E_TIMEOUT)

    ONT.get_set_error_activation(zq_ONT_p1, "HO", "OFF")
    #time.sleep(E_TIMEOUT)
    
    ###################################################################
    #Verify BBE-ES-SES counters are incremented 
    ###################################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "15-MIN")
        zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "15-MIN")
        zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "15-MIN")
        if zq_bbe == 0 and zq_es == 0 and zq_ses == 0:
            dprint("OK\tPM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1))
        else:
            dprint("KO\tPM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                    "PM counter [{}]-[15-MIN] for {} were incremented. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))

        dprint("\tPM counter BBE: {}".format(zq_bbe),2)
        dprint("\tPM counter  ES: {}".format(zq_es),2)
        dprint("\tPM counter SES: {}".format(zq_ses),2)

    if zq_period == "BOTH" or zq_period == "1-DAY":  
        if zq_locn == "BIDIR":
            zq_bbe_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-NE", zq_locn, "1-DAY")
            zq_bbe_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC-FE", zq_locn, "1-DAY")
            zq_es_ne  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-NE", zq_locn, "1-DAY")
            zq_es_fe  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC-FE", zq_locn, "1-DAY")
            zq_ses_ne = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-NE", zq_locn, "1-DAY")
            zq_ses_fe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC-FE", zq_locn, "1-DAY")
            if  zq_bbe_ne == 0 and \
                zq_bbe_fe == 0 and \
                zq_es_ne == 0 and \
                zq_es_fe == 0 and \
                zq_ses_ne == 0 and \
                zq_ses_fe == 0: 
                dprint("OK\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1))
            else:
                dprint("KO\tSome PM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "Some PM counter [{}]-[1-DAY] for {} were incremented. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))

            dprint("\tPM counter BBE-NE: {}".format(zq_bbe_ne),2)
            dprint("\tPM counter BBE-FE: {}".format(zq_bbe_fe),2)
            dprint("\tPM counter  ES-NE: {}".format(zq_es_ne),2)
            dprint("\tPM counter  ES-FE: {}".format(zq_es_fe),2)
            dprint("\tPM counter SES-NE: {}".format(zq_ses_ne),2)
            dprint("\tPM counter SES-FE: {}".format(zq_ses_fe),2)
        
        else:  
            zq_bbe = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"BBE-HOVC", zq_locn, "1-DAY")
            zq_es  = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"ES-HOVC", zq_locn, "1-DAY")
            zq_ses = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"SES-HOVC", zq_locn, "1-DAY")
            if zq_bbe == 0 and zq_es == 0 and zq_ses == 0:
                dprint("OK\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1))
            else:
                dprint("KO\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[1-DAY] for {} were incremented. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))

            dprint("\tPM counter BBE: {}".format(zq_bbe),2)
            dprint("\tPM counter  ES: {}".format(zq_es),2)
            dprint("\tPM counter SES: {}".format(zq_ses),2)

    
    ###################################################################
    # Insert B3 error continuous burst 
    ###################################################################
    # Exchange error frame number with error free number to detect UAS         
    ###################################################################
    ONT.get_set_num_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err_free)
    ONT.get_set_num_not_errored_burst_frames(zq_ONT_p1, "HO", zq_num_err)
    ONT.get_set_error_insertion_type(zq_ONT_p1, zq_alm_type)
    ONT.get_set_error_activation(zq_ONT_p1, "HO", "ON")
    time.sleep(E_TIMEOUT)
    #time.sleep(E_TIMEOUT)
    if zq_locn == "BIDIR":
        ONT.get_set_error_insertion_type(zq_ONT_p1, "HPREI")
        time.sleep(E_TIMEOUT)
        #time.sleep(E_TIMEOUT)

    ONT.get_set_error_activation(zq_ONT_p1, "HO", "OFF")
    time.sleep(E_TIMEOUT)
    
    ###################################################################
    #Verify UAS counter is incremented 
    ###################################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
        
        if zq_uas == 0:
            dprint("OK\tPM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1))
        else:
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
            "PM counter [{}]-[15-MIN] for {} were incremented. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
            dprint("KO\tPM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
        
    if zq_period == "BOTH" or zq_period == "1-DAY":
        if zq_locn == "BIDIR":  
            zq_uas_bi = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
            if zq_uas_bi == 0:
                dprint("OK\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[1-DAY] for {} were incremented. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi),2)
            
        else:
            zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
            
            if zq_uas == 0:
                dprint("OK\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "PM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[1-DAY] for {} were incremented. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
        
    return


def QS_110_Init_PM_Counter(zq_run, NE1, zq_vc4_idx, zq_locn, zq_period, zq_dir="RCV"):
    #INIT PM REGISTER/COUNTER
    #INIT-REG-VC4:[TID]:AID:[CTAG]::[MONTYPE],[MONVAL],[LOCN],[DIRN],[TMPER]*/
    
    zq_tl1_res=NE1.tl1.do("INIT-REG-VC4::{}:::ALL,0,{},{},{};".format(zq_vc4_idx, zq_locn, zq_dir, zq_period))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\tPM  Counter Reset Command successful for {}: [{}]-[{}]-[{}]".format(zq_vc4_idx,zq_locn,zq_dir,zq_period),2)
        zq_run.add_success(NE1, "TL1 Command","0.0", "PM  Counter Reset Command successful for {}: [{}]-[{}]-[{}]".format(zq_vc4_idx,zq_locn,zq_dir,zq_period))
    else:
        zq_run.add_failure(NE1, "TL1 Command", "0.0", "TL1 Command", 
                                "PM  Counter Reset Command successful for {}: [{}]-[{}]-[{}] {}".format(zq_vc4_idx,zq_locn,zq_dir,zq_period,QS_000_Print_Line_Function()))
        dprint("KO\tPM  Counter Reset Command NOT successful for {}: [{}]-[{}]-[{}]".format(zq_vc4_idx,zq_locn,zq_dir,zq_period),2)

    return


def QS_120_Verify_PM_Counter_Zero(zq_run, NE1, zq_vc4_idx):

    zq_counter = 0
    zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::ALL,0-UP,ALL,ALL,BOTH,,,1,1;".format(zq_vc4_idx))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        if zq_msg.get_cmd_response_size() != 0:
            zq_temp_ary = zq_msg._TL1message__m_plain.split("\r\n")
            for zq_i in range(1,len(zq_temp_ary)-2):
                if zq_temp_ary[zq_i].find("{},VC4:".format(zq_vc4_idx)) > 0:
                    zq_counter_ary = zq_temp_ary[zq_i].split(",")
                    zq_aid = zq_counter_ary[0].replace("\"","")
                    zq_cnt = zq_counter_ary[1]
                    zq_cnt_val = int(zq_counter_ary[2])
                    zq_counter = zq_counter + zq_cnt_val
                    if zq_cnt_val != 0:
                        zq_counter = zq_counter + 1
                    dprint("\tPM Counter [{}] for [{}] is {}".format(zq_cnt, zq_aid, zq_cnt_val),2)
                    
    return int(zq_counter)

def QS_200_Verify_Validity_Flag(zq_run, NE1, zq_vc4_idx, zq_locn, zq_period, zq_val_flag_exp, zq_cnt_entry, zq_dir="RCV", zq_counter_type=""):

    zq_str = ""
    zq_res = False
    if  (zq_val_flag_exp == 'COMPL'):
        zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},0-UP,{},{},{};".format(zq_vc4_idx, zq_counter_type, zq_locn, zq_dir, zq_period))
    else:
        if (zq_val_flag_exp == 'OFF'):
            if zq_period == '15-MIN':
                zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},0-UP,{},{},{},,00-00;".format(zq_vc4_idx, zq_counter_type, zq_locn, zq_dir, zq_period))
            else:
                zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},0-UP,{},{},{},05-02,00-00;".format(zq_vc4_idx, zq_counter_type, zq_locn, zq_dir, zq_period))

        if (zq_val_flag_exp == 'PRTL') or (zq_val_flag_exp == 'LONG'):
            if zq_period == '15-MIN':
                zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},1-UP,{},{},{},,,ALL;".format(zq_vc4_idx, zq_counter_type, zq_locn, zq_dir, zq_period))
            else:
                zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},1-UP,{},{},{},,,,ALL;".format(zq_vc4_idx, zq_counter_type, zq_locn, zq_dir, zq_period))
        
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        if zq_msg.get_cmd_response_size() != 0:
            zq_temp_ary = zq_msg._TL1message__m_plain.split("\r\n")
            for zq_i in range(1,len(zq_temp_ary)):
                if zq_temp_ary[zq_i].find("{},VC4".format(zq_vc4_idx)) > 0:
                    zq_cnt_ary = zq_temp_ary[zq_i].split(",")
                    zq_cnt_ary[2] = ""
                    zq_cnt_ary[7] = "" 
                    zq_cnt_ary[8] = ""
                    zq_cnt_ary[9] = ""
                    zq_val_flag = zq_cnt_ary[3] 
                    zq_sep = ","
                    zq_cnt_res = zq_sep.join(zq_cnt_ary)
                    zq_cnt_res = zq_cnt_res.replace("\"","")
                    zq_cnt_res = zq_cnt_res.replace(" ","")
                    if (zq_cnt_res == zq_cnt_entry): 
                        if (zq_val_flag == zq_val_flag_exp):
                            zq_res = True
                            dprint("OK\tValidity Flag [{}]".format(zq_cnt_entry),2)
                            zq_run.add_success(NE1, "PM Counter Validity Flag Check","0.0", "PM Counter Validity Flag Check successful [{}]".format(zq_cnt_entry))
                            break
                        else:
                            zq_res = False
                            dprint("KO\tValidity Flag [{}]".format(zq_cnt_entry),2)
                            zq_run.add_failure(NE1, "PM Counter Validity Flag Check", "0.0", "PM Counter Validity Flag Check", 
                                                    "PM Counter Validity Flag Check Fail [{}] {}".format(zq_cnt_entry,QS_000_Print_Line_Function()))
            
            if not zq_res:
                zq_str = zq_str + zq_cnt_entry        
                    
    return (zq_res,zq_str)


def QS_900_Set_Date(zq_run, NE1, zq_date,zq_time):

    zq_tl1_res=NE1.tl1.do("ED-DAT:::::{},{};".format(zq_date,zq_time))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\tNE date & time changed to {} & {}".format(zq_date,zq_time),2)
        zq_run.add_success(NE1, "NE date & time changed to {} & {}".format(zq_date,zq_time),"0.0", "NE date & time changed to {} & {}".format(zq_date,zq_time))
    else:
        dprint("KO\tNE date & time change failure",2)
        zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", "NE date & time change failure " + QS_000_Print_Line_Function())

    return



def QS_910_Wait_Quarter(NE1):
    
    zq_tl1_res=NE1.tl1.do("RTRV-HDR;")
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        zq_date_time=zq_msg.get_time_stamp()
        zq_time = zq_date_time[1]
        zq_min =  zq_date_time[1].split(":")
        #1 minuto e 1/2 in piu' rispetto allo scadere del quarto d'ora
        zq_wait = (15-(int(zq_min[1])%15)+1)*60 + 30  

    return(zq_wait)


def QS_920_Get_Date_Time(NE1):
    
    zq_tl1_res=NE1.tl1.do("RTRV-HDR;")
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        zq_date_time=zq_msg.get_time_stamp()

    return(zq_date_time)

