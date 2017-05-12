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

global E_TTE_MSG     #TOTAL TEST TIME ELAPSED
global E_PTE_MSG     #PARTIAL TEST TIME ELAPSED
global E_LO_MTX 
global E_MAX_MVC4 
global E_TIMEOUT 

global E_RFI_NUM_TU12
global E_RFI_NUM_TU3 
global E_BLOCK_SIZE         
global E_WAIT 

global E_HO_TI
global E_LO_TI
global E_BAD_TI
global E_DEF_TI 

global E_VC4_1_1 
global E_VC4_1_2 
global E_VC4_2_1 
global E_VC4_2_2 
global E_VC4_3_1 
global E_VC4_3_2 

global E_TUG3
global E_TUG2
global E_TU12

global E_BBE_HOVC_15_ON 
global E_ES_HOVC_15_ON 
global E_SES_HOVC_15_ON 

global E_BBE_HOVC_24_ON 
global E_ES_HOVC_24_ON 
global E_SES_HOVC_24_ON 

# TCA THREHOLD VALUES FOR ALARM CLEAR
global E_BBE_HOVC_15_OFF 
global E_ES_HOVC_15_OFF 
global E_SES_HOVC_15_OFF 

global E_BBE_HOVC_24_OFF 
global E_ES_HOVC_24_OFF 
global E_SES_HOVC_24_OFF 

global E_SLOT
global E_10XANY10G
global E_10XANY10G_MOD

global E_24XANYMR
global E_24XANYMR_STMx_MOD

global E_10XANY
global E_10XANY_STM1_4_MOD
global E_10XANY_STM16_MOD
global E_10XANY_STM1_4_MOD_NUM
global E_10XANY_STM16_MOD_NUM 
global E_24XANYMR_STMx_MOD_NUM 
global E_10XANY10G_MOD_NUM

global E_AU44C_STM16_IDX
global E_AU44C_STM64_IDX
global E_AU416C_STM64_IDX


E_TTE_MSG  = "TEST DURATION [TOTAL]"
E_PTE_MSG  = "TEST DURATION [PARTIAL]"
E_MAX_MVC4 = 384
E_LO_MTX = "MXH60GLO"
E_TIMEOUT = 20

E_RFI_NUM_TU12 = 1
E_RFI_NUM_TU3 = 2
E_BLOCK_SIZE = 64        
E_WAIT = 10

#TO BE USED WITH ONT
E_ASCII_HO_TI  = 'ONT HO-TRACE   '
E_ASCII_LO_TI  = 'ONT LO-TRACE   '
E_ASCII_BAD_TI = 'ABCDEFGHIJKL   '
E_ASCII_DEF_TI = '' 

#TO BE USED FOR AU4 
E_HO_TI  = 'X4F4E5420484F2D5452414345202020' #'ONT HO-TRACE   '
E_LO_TI  = 'X4F4E54204C4F2D5452414345202020' #'ONT LO-TRACE   '
E_BAD_TI = 'X4142434445464748494A4B4C202020' #'ABCDEFGHIJKL   '
E_DEF_TI = 'X000000000000000000000000000000' 

E_SLOT = ['2','3','4','5','6','7','8','12','13','14','15','16','17','18','19']

E_VC4_1_1 = 34      # <64
E_VC4_1_2 = 92      # 65<x<129
E_VC4_2_1 = 189     # 128<x<193
E_VC4_2_2 = 227     # 192<x<257
E_VC4_3_1 = 289     # 256<x<321
E_VC4_3_2 = 356     # 320<x<385

#CHANGE THIS LISTS TO RANGE IN MORE LOVC12, ACCORDING TO SDH SPECIFICATION
#TUG3 range from 1..3
#TUG2 range from 1..7
#TU12 range from 1..3
E_TUG3 = [1,2,3]
E_TUG2 = [4]
E_TU12 = [1,3]

#
#   PM CONSTANTS DEFINITION
'''
    MonitorType    Location    Direction    Threshold Level Clear    15-Minute Threshold    1-Day Threshold
    ES-HOVC         NEND        TRMT            20                      180                      1500
                                RCV             20                      180                      1500
                    FEND        TRMT            20                      180                      1500
                                RCV             20                      180                      1500
    SES-HOVC        NEND        TRMT             0                       15                        20
                                RCV              0                       15                        20
                    FEND        TRMT             0                       15                        20
                                RCV              0                       15                        20
    BBE-HOVC        NEND        TRMT           200                    36000                     48000
                                RCV            200                    36000                     48000
                    FEND        TRMT           200                    36000                     48000
                                RCV            200                    36000                     48000
'''

# TCA THREHOLD VALUES FOR ALARM ARISE
E_BBE_HOVC_15_ON = 12000 
E_ES_HOVC_15_ON  = 50 
E_SES_HOVC_15_ON = 5 

E_BBE_HOVC_24_ON = 12000 
E_ES_HOVC_24_ON  = 50 
E_SES_HOVC_24_ON = 5 

# TCA THREHOLD VALUES FOR ALARM CLEAR
E_BBE_HOVC_15_OFF = 200 
E_ES_HOVC_15_OFF  = 20 
E_SES_HOVC_15_OFF = 0 

E_BBE_HOVC_24_OFF = 200 
E_ES_HOVC_24_OFF  = 20 
E_SES_HOVC_24_OFF = 0 


E_10GSO = "1P10GSO"
E_10GSOE = "1P10GSOE"
E_10GSO_MOD = [1]
E_10GSO_MOD_NUM = 1


E_10XANY10G = "10XANY10G"
E_10XANY10G_MOD = [1,2,3,4,5,6,7,8,9,10]
E_10XANY10G_MOD_NUM = 10

E_MRSOE = "MRSOE"
E_MRSOE_STMx_MOD = [1,2,3,4,5,6,7,8]
E_MRSOE_STMx_MOD_NUM = 8

E_10XANY = "10XANY"
E_10XANY_STMx_MOD = [1,2,3,4,5,6,7,8,9,10]
E_10XANY_STMx_MOD_NUM = 10

E_24XANYMR = "24XANYMR"
E_24XANYMR_STMx_MOD = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
E_24XANYMR_STMx_MOD_NUM = 24

E_AU44C_STM16_IDX = [1,5,9,13]
E_AU44C_STM64_IDX = [1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61]
E_AU416C_STM64_IDX = [1,17,33,49]


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


def QS_035_Create_LO_XC_Block(zq_run, NE1, zq_vc4_1, zq_vc4_2, zq_xc_list):
    
    zq_tu12_list=zq_xc_list[zq_vc4_1].split(',')
    zq_tu12_tmp1=zq_tu12_list[1].replace('MVC4','MVC4TU12')

    zq_tu12_list=zq_xc_list[zq_vc4_2].split(',')
    zq_tu12_tmp2=zq_tu12_list[1].replace('MVC4','MVC4TU12')

    for zq_j in range (1,4):
        for zq_k in range(1,8):                                        #zq_k=TU12 index
            for zq_m in range(1,4):
                zq_tu12_idx1=zq_tu12_tmp1+'-'+str(zq_j)+'-'+str(zq_k)+'-'+str(zq_m)
                zq_tu12_idx2=zq_tu12_tmp2+'-'+str(zq_j)+'-'+str(zq_k)+'-'+str(zq_m)
                zq_tl1_res=NE1.tl1.do("ENT-CRS-LOVC12::{},{}:::2WAY;".format(zq_tu12_idx1,zq_tu12_idx2))
                zq_msg=TL1message(NE1.tl1.get_last_outcome())
                dprint(NE1.tl1.get_last_outcome(),1)
                zq_cmd=zq_msg.get_cmd_status()
                if zq_cmd == (True,'COMPLD'):
                    dprint("\nOK\tCross-connection successfully created from {} to {}".format(zq_tu12_idx1,zq_tu12_idx2),2)
                    zq_run.add_success(NE1, "Cross-connection creation successful {} to {}".format(zq_tu12_idx1,zq_tu12_idx2),"0.0", "Cross-connection creation successful")
    
                else:
                    dprint("\nKO\tCross-connection creation failed from {} to {}".format(zq_tu12_idx1,zq_tu12_idx2),2)
                    zq_run.add_failure(NE1, "TL1 COMMAND","0.0","TL1 COMMAND FAIL",
                                            "Cross-connection creation failed from {} to {} {}".format(zq_tu12_idx1,zq_tu12_idx2,QS_000_Print_Line_Function()))


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


def QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_vc3, zq_trace):

    zq_tl1_res=NE1.tl1.do("ED-TU3::{}::::TRCEXPECTED={}, EGTRCEXPECTED={};".format(zq_vc3, zq_trace, zq_trace))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tLO Trace Identifier changed to {} for {}".format(zq_trace, zq_vc3),2)
        zq_run.add_success(NE1, "LO Trace Identifier changed to {} for {}".format(zq_trace, zq_vc3),"0.0", "LO Trace Identifier changed")

    else:
        dprint("\nKO\tLO Trace Identifier change failure for {}".format(zq_vc3),2)
        zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "LO Trace Identifier change failure for {}".format(zq_vc3),
                                "LO Trace Identifier change failure for {} {}".format(zq_vc3,QS_000_Print_Line_Function()))
    
    return


def QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_vc12, zq_trace):

    zq_tl1_res=NE1.tl1.do("ED-TU12::{}::::TRCEXPECTED={}, EGTRCEXPECTED={};".format(zq_vc12, zq_trace, zq_trace))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tLO Trace Identifier changed to {} for {}".format(zq_trace, zq_vc12),2)
        zq_run.add_success(NE1, "LO Trace Identifier changed to {} for {}".format(zq_trace, zq_vc12),"0.0", "LO Trace Identifier changed")

    else:
        dprint("\nKO\tLO Trace Identifier change failure for {}".format(zq_vc12),2)
        zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMAND FAIL",
                                "LO Trace Identifier change failure for {} {}".format(zq_vc12,QS_000_Print_Line_Function()))
    
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

def QS_065_Delete_LO_XC_Block(zq_run, NE1, zq_vc4_1, zq_vc4_2, zq_xc_list):

    zq_tu12_list=zq_xc_list[zq_vc4_1].split(',')
    zq_tu12_tmp1=zq_tu12_list[1].replace('MVC4','MVC4TU12')

    zq_tu12_list=zq_xc_list[zq_vc4_2].split(',')
    zq_tu12_tmp2=zq_tu12_list[1].replace('MVC4','MVC4TU12')

    for zq_j in range (1,4):
        for zq_k in range(1,8):                                        #zq_k=TU12 index
            for zq_m in range(1,4):
                zq_tu12_idx1=zq_tu12_tmp1+'-'+str(zq_j)+'-'+str(zq_k)+'-'+str(zq_m)
                zq_tu12_idx2=zq_tu12_tmp2+'-'+str(zq_j)+'-'+str(zq_k)+'-'+str(zq_m)
                zq_tl1_res=NE1.tl1.do("DLT-CRS-LOVC12::{},{};".format(zq_tu12_idx1,zq_tu12_idx2))
                zq_msg=TL1message(NE1.tl1.get_last_outcome())
                dprint(NE1.tl1.get_last_outcome(),1)
                zq_cmd=zq_msg.get_cmd_status()
                if zq_cmd == (True,'COMPLD'):
                    dprint("\nOK\tCross-connection successfully deleted from {} to {}".format(zq_tu12_idx1,zq_tu12_idx2),2)
                    zq_run.add_success(NE1, "Cross-connection successfully deleted from {} to {}".format(zq_tu12_idx1,zq_tu12_idx2),"0.0", "Cross-connection successfully deleted")
    
                else:
                    dprint("\nKO\tCross-connection deletion failed from {} to {}".format(zq_tu12_idx1,zq_tu12_idx2),2)
                    zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "Cross-connection deletion failed from {} to {}".format(zq_tu12_idx1,zq_tu12_idx2), 
                                            "Cross-connection deletion failed from {} to {} {}".format(zq_tu12_idx1,zq_tu12_idx2,QS_000_Print_Line_Function()))
    

    return


def QS_070_Check_No_Alarm(zq_run, NE1, ONT, zq_ONT_p1, zq_ONT_p2, zq_vc4_ch1, zq_vc4_ch2):

    
    ONT.get_set_rx_lo_measure_channel(zq_ONT_p1, zq_vc4_ch1)
    ONT.get_set_rx_lo_measure_channel(zq_ONT_p2, zq_vc4_ch2)

    ONT.get_set_tx_lo_measure_channel(zq_ONT_p1, zq_vc4_ch1)
    ONT.get_set_tx_lo_measure_channel(zq_ONT_p2, zq_vc4_ch2)
    
    ONT.start_measurement(zq_ONT_p1)
    ONT.start_measurement(zq_ONT_p2)
    
    time.sleep(1)

    ONT.halt_measurement(zq_ONT_p1)
    ONT.halt_measurement(zq_ONT_p2)

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


def QS_070_Enable_Disable_POM(zq_run, NE1, zq_mtx_slot, zq_vc4, zq_enadis):

    zq_tu12_idx="MVC4TU12-{}-{}".format(zq_mtx_slot,str(zq_vc4))
    for zq_j in range (1,4):
        for zq_m in range (1,8):
            for zq_l in range (1,4):
                zq_tl1_res=NE1.tl1.do("ED-TU12::{}-{}-{}-{}::::POM={},EGPOM={};".format(zq_tu12_idx, str(zq_j), str(zq_m), str(zq_l), zq_enadis, zq_enadis))
                zq_msg=TL1message(NE1.tl1.get_last_outcome())
                dprint(NE1.tl1.get_last_outcome(),1)
                zq_cmd=zq_msg.get_cmd_status()
            
                if zq_cmd == (True,'COMPLD'):
                    dprint("\nOK\tPom and EGPOM setting to [{}] for {}-{}-{}-{} successful".format(zq_enadis, zq_tu12_idx, str(zq_j), str(zq_m), str(zq_l)),2)
                    zq_run.add_success(NE1, "Pom and EGPOM setting to [{}] for {}-{}-{} successful".format(zq_enadis, zq_tu12_idx, str(zq_j), str(zq_m), str(zq_l)),"0.0", "Pom and EGPOM setting")
            
                else:
                    dprint("\nKO\tPom and EGPOM setting to [{}] for {}-{}-{}-{} failed".format(zq_enadis, zq_tu12_idx, str(zq_j), str(zq_m), str(zq_l)),2)
                    zq_run.add_failure(NE1,  "TL1 COMMAND","0.0", "Pom and EGPOM setting to [{}] for {}-{}-{}-{} failed".format(zq_enadis, zq_tu12_idx, str(zq_j), str(zq_m), str(zq_l)), 
                                             "Pom and EGPOM setting to [{}] for {}-{}-{}-{} failed {}".format(zq_enadis, zq_tu12_idx, str(zq_j), str(zq_m), str(zq_l),QS_000_Print_Line_Function()))
                
        
    return


def QS_072_Enable_Disable_POM(zq_run, NE1, zq_mtx_slot, zq_vc4, zq_enadis):

    for zq_j in range (1,4):
        zq_tl1_res=NE1.tl1.do("ED-TU3::MVC4TU3-{}-{}-{}::::POM={},EGPOM={};".format(zq_mtx_slot, zq_vc4, zq_j, zq_enadis, zq_enadis))
        zq_msg=TL1message(NE1.tl1.get_last_outcome())
        dprint(NE1.tl1.get_last_outcome(),1)
        zq_cmd=zq_msg.get_cmd_status()
    
        if zq_cmd == (True,'COMPLD'):
            dprint("\nOK\tPOM and EGPOM setting to [{}] for MVC4TU3-{}-{}-{} successful".format(zq_enadis,zq_mtx_slot, zq_vc4, zq_j),2)
            zq_run.add_success(NE1, "POM and EGPOM setting to [{}] for MVC4TU3-{}-{}-{} successful".format(zq_enadis,zq_mtx_slot, zq_vc4, zq_j),"0.0", "POM and EGPOM setting")
    
        else:
            dprint("\nKO\tPOM and EGPOM setting to [{}] for MVC4TU3-{}-{}-{} failed".format(zq_enadis,zq_mtx_slot, zq_vc4, zq_j),2)
            zq_run.add_failure(NE1,  "TL1 COMMAND","0.0", "POM and EGPOM setting to [{}] for MVC4TU3-{}-{}-{} failed".format(zq_enadis,zq_mtx_slot, zq_vc4, zq_j),
                                     "POM and EGPOM setting to [{}] for MVC4TU3-{}-{}-{} failed {}".format(zq_enadis,zq_mtx_slot, zq_vc4, zq_j,QS_000_Print_Line_Function()))
        
    return



def QS_075_Enable_Disable_TRCMON(zq_run, NE1, zq_vc4, zq_enadis):

    zq_tl1_res=NE1.tl1.do("ED-TU3::{}::::TRCMON={},EGTRCMON={};".format(zq_vc4, zq_enadis, zq_enadis))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    zq_cmd=zq_msg.get_cmd_status()

    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tTRCMON and EGTRCMON setting to [{}] for {} successful".format(zq_enadis, zq_vc4),2)
        zq_run.add_success(NE1, "TRCMON and EGTRCMON setting to [{}] for {} successful".format(zq_enadis, zq_vc4),"0.0", "TRCMON and EGTRCMON setting")

    else:
        dprint("\nKO\tTRCMON and EGTRCMON setting to [{}] for {} failed".format(zq_enadis, zq_vc4),2)
        zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TRCMON and EGTRCMON setting to [{}] for {} failed".format(zq_enadis, zq_vc4),
                                "TRCMON and EGTRCMON setting to [{}] for {} failed {}".format(zq_enadis, zq_vc4,QS_000_Print_Line_Function()))
    
    return


def QS_077_Enable_Disable_TRCMON(zq_run, NE1, zq_vc12, zq_enadis):

    zq_tl1_res=NE1.tl1.do("ED-TU12::{}::::TRCMON={},EGTRCMON={};".format(zq_vc12, zq_enadis, zq_enadis))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    zq_cmd=zq_msg.get_cmd_status()

    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tTRCMON and EGTRCMON setting to [{}] for {} successful".format(zq_enadis, zq_vc12),2)
        zq_run.add_success(NE1, "TRCMON and EGTRCMON setting to [{}] for {} successful".format(zq_enadis, zq_vc12),"0.0", "TRCMON and EGTRCMON setting")

    else:
        dprint("\nKO\tTRCMON and EGTRCMON setting to [{}] for {} failed".format(zq_enadis, zq_vc12),2)
        zq_run.add_failure(NE1,  "TL1 COMMAND","0.0", "TRCMON and EGTRCMON setting to [{}] for {} failed".format(zq_enadis, zq_vc12),
                                 "TRCMON and EGTRCMON setting to [{}] for {} failed {}".format(zq_enadis, zq_vc12,QS_000_Print_Line_Function()))
    
    return


def QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx, zq_counter_type, zq_locn, zq_period, zq_dir="RCV"):

    zq_counter = -1
    zq_tl1_res=NE1.tl1.do("RTRV-PM-VC4::{}:::{},0-UP,{},{},{};".format(zq_vc4_idx, zq_counter_type, zq_locn,zq_dir,zq_period))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        if zq_msg.get_cmd_response_size() != 0:
            zq_counter=zq_msg.get_cmd_attr_value("{},VC4".format(zq_vc4_idx), "2")

    return int(zq_counter[0])


def QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ont_port, zq_alm_exp):

    ONT.start_measurement(zq_ont_port)
    time.sleep(E_WAIT)
    ONT.halt_measurement(zq_ont_port)
    zq_alm = ONT.retrieve_ho_lo_alarms(zq_ont_port)
    if zq_alm[0] == True:           #COMMAND IS OK
        if len(zq_alm[1]) == 0:     #NO ALARM FOUND
            if zq_alm_exp == "":    #NO ALARM EXPECTED AND NO ALARM FOUND
                dprint("OK\tNO Alarm found on ONT port {}".format(zq_ont_port),2)
                zq_run.add_success(NE1, "NO Alarm found on ONT port {}".format(zq_ont_port),"0.0", "ONT Alarm check")
                
            else:                   #NO ALARM EXPECTED BUT ALARM FOUND  
                dprint("KO\tAlarm found on ONT port {}:".format(zq_ont_port),2)
                dprint("\t\tAlarm: Exp [{}]  - Rcv [{}]".format("no alarm",zq_alm[1][0]),2)
                zq_run.add_failure(NE1,  "ONT Alarm check","0.0", "ONT Alarms check", 
                                         "Alarm found on ONT port {}: Exp [{}]  - Rcv [{}] {}".format(zq_ont_port, "no alarm", zq_alm[1][0],QS_000_Print_Line_Function()))
                
        else:                       #ALARM FOUND
            if zq_alm[1][0] == zq_alm_exp:      #ALARM FOUND AND ALARM WAS EXPECTED
                dprint("OK\t{} Alarm found on ONT port {}".format(zq_alm_exp,zq_ont_port),2)
                zq_run.add_success(NE1, "{} Alarm found on ONT port {}".format(zq_alm_exp,zq_ont_port),"0.0", "ONT Alarm check")
            else:                               #ALARM FOUND BUT ALARM WAS NOT EXPECTED
                dprint("KO\tAlarm mismatch on ONT port {}:".format(zq_ont_port),2)
                dprint("\t\tAlarm: Exp [{}]  - Rcv [{}]".format(zq_alm_exp,zq_alm[1][0]),2)
                zq_run.add_failure(NE1,  "ONT Alarm check","0.0", "ONT Alarms check", 
                                         "Alarm mismatch on ONT port {}: Exp [{}]  - Rcv [{}] {}".format(zq_ont_port, zq_alm_exp, zq_alm[1][0],QS_000_Print_Line_Function()))

    return


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


def QS_92_Check_MVC4_Alarm(zq_run, NE1,zq_vc4,zq_man_exp,zq_type_exp,zq_dir_exp):

    zq_tl1_res=NE1.tl1.do("RTRV-COND-VC4::{}:::{};".format(str(zq_vc4),zq_man_exp))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("KO\t{} Condition verification failure for {} facility : Exp [{}] - Rcv [0]".format(zq_man_exp, zq_vc4, E_RFI_NUM_TU3),2)
        zq_run.add_failure(NE1,"{} CONDITION CHECK".format(zq_man_exp),"0.0","{} Condition verification failure for {} facility : Exp [{}] - Rcv [0]".format(zq_man_exp, zq_vc4, E_RFI_NUM_TU3), 
                               "{} Condition verification failure: Exp [{}] - Rcv [0] {}".format(zq_man_exp, E_RFI_NUM_TU3,QS_000_Print_Line_Function()))
    else:
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            zq_man = zq_msg.get_cmd_attr_value("{},VC4".format(zq_vc4), 2)
            zq_type = zq_msg.get_cmd_attr_value("{},VC4".format(zq_vc4), 6)
            zq_dir = zq_msg.get_cmd_attr_value("{},VC4".format(zq_vc4), 7)
            
            zq_man = zq_man[0]
            zq_type = zq_type[0]
            zq_dir = zq_dir[0]

            if (zq_man == zq_man_exp) and (zq_type == zq_type_exp) and (zq_dir == zq_dir_exp):
                dprint("OK\t{} Condition verification successful for {} facility.".format(zq_man_exp, str(zq_vc4)),2)
                zq_run.add_success(NE1, "{} Condition verification successful for {} facility.".format(zq_man_exp, str(zq_vc4)),"0.0", "{} CONDITION CHECK".format(zq_man_exp))
            else:
                dprint("KO\t{} Condition verification failure for {} facility.".format(zq_man_exp, str(zq_vc4)),2)
                dprint("\t\tCOND: Exp [{}]  - Rcv [{}]".format(zq_man_exp,zq_man),2)
                dprint("\t\tTYPE: Exp [{}] - Rcv [{}]".format(zq_type_exp,zq_type),2)
                dprint("\t\tDIR : Exp [{}]  - Rcv [{}]".format(zq_dir_exp,zq_dir),2)
                zq_run.add_failure(NE1,"{} CONDITION CHECK".format(zq_man_exp),"0.0","{} Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}]".format(zq_man_exp, str(zq_vc4),zq_man_exp,zq_type_exp,zq_dir_exp,zq_man,zq_type,zq_dir),
                                       "{} Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}] {}".format(zq_man_exp,zq_type_exp,zq_dir_exp,zq_man,zq_type,zq_dir,QS_000_Print_Line_Function()))
        
    return


def QS_95_Check_MVC4TU3_Alarm(zq_run, NE1, zq_vc3, zq_man_exp, zq_type_exp, zq_dir_exp):

    zq_tl1_res=NE1.tl1.do("RTRV-COND-LOVC3::{}:::{},{},{};".format(str(zq_vc3),zq_man_exp,zq_type_exp,zq_dir_exp))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("KO\t{} Condition verification failure for {} facility : Exp [{}] - Rcv [0]".format(zq_man_exp, zq_vc3, E_RFI_NUM_TU3),2)
        zq_run.add_failure(NE1,"SSF CONDITION CHECK","0.0","{} Condition verification failure for {} facility : Exp [{}] - Rcv [0]".format(zq_man_exp, zq_vc3, E_RFI_NUM_TU3),
                               "SSF Condition verification failure: Exp [{}] - Rcv [0] {}".format(E_RFI_NUM_TU3,QS_000_Print_Line_Function()))
    else:
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            zq_man = zq_msg.get_cmd_attr_value("{},LOVC3".format(zq_vc3), 2)
            zq_type = zq_msg.get_cmd_attr_value("{},LOVC3".format(zq_vc3), 6)
            zq_dir = zq_msg.get_cmd_attr_value("{},LOVC3".format(zq_vc3), 7)

            zq_man = zq_man[0]
            zq_type = zq_type[0]
            zq_dir = zq_dir[0]
            
            if (zq_man == zq_man_exp) and (zq_type == zq_type_exp) and (zq_dir == zq_dir_exp):
                dprint("OK\t{} Condition verification successful for {} facility [{}][{}][{}].".format(zq_man_exp,str(zq_vc3),zq_man,zq_type,zq_dir),2)
                zq_run.add_success(NE1, "{} Condition verification successful for {} facility [{}][{}][{}].".format(zq_man_exp,str(zq_vc3),zq_man,zq_type,zq_dir),"0.0", "{} CONDITION CHECK".format(zq_man_exp))
            else:
                dprint("KO\t{} Condition verification failure for {} facility.".format(zq_man_exp, str(zq_vc3)),2)
                dprint("\t\tCOND: Exp [{}]  - Rcv [{}]".format(zq_man_exp,zq_man),2)
                dprint("\t\tTYPE: Exp [{}] - Rcv [{}]".format(zq_type_exp,zq_type),2)
                dprint("\t\tDIR : Exp [{}]  - Rcv [{}]".format(zq_dir_exp,zq_dir),2)
                zq_run.add_failure(NE1, "{} CONDITION CHECK".format(zq_man_exp),"0.0","{} Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}]".format(zq_man_exp, str(zq_vc3),zq_man_exp,zq_type_exp,zq_dir_exp,zq_man,zq_type,zq_dir),
                                        "{} Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}] {}".format(zq_man_exp, str(zq_vc3),zq_man_exp,zq_type_exp,zq_dir_exp,zq_man,zq_type,zq_dir,QS_000_Print_Line_Function()))
        
    return


def QS_97_Check_MVC4TU12_Alarm(zq_run, NE1, zq_vc12, zq_man_exp, zq_type_exp, zq_dir_exp):

    zq_tl1_res=NE1.tl1.do("RTRV-COND-LOVC12::{}:::{},{},{};".format(str(zq_vc12),zq_man_exp,zq_type_exp,zq_dir_exp))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("KO\t{} Condition verification failure for {} facility : Exp [{}] - Rcv [0]".format(zq_man_exp, zq_vc12, E_RFI_NUM_TU12),2)
        zq_run.add_failure(NE1,"SSF CONDITION CHECK","0.0","{} Condition verification failure for {} facility : Exp [{}] - Rcv [0]".format(zq_man_exp, zq_vc12, E_RFI_NUM_TU12),
                               "SSF Condition verification failure: Exp [{}] - Rcv [0]".format(E_RFI_NUM_TU12,QS_000_Print_Line_Function()))
    else:
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            zq_man = zq_msg.get_cmd_attr_value("{},LOVC12".format(zq_vc12), 2)
            zq_type = zq_msg.get_cmd_attr_value("{},LOVC12".format(zq_vc12), 6)
            zq_dir = zq_msg.get_cmd_attr_value("{},LOVC12".format(zq_vc12), 7)

            zq_man = zq_man[0] 
            zq_type = zq_type[0]
            zq_dir = zq_dir[0]
            
            if (zq_man == zq_man_exp) and (zq_type == zq_type_exp) and (zq_dir == zq_dir_exp):
                dprint("OK\t{} Condition verification successful for {} facility [{}][{}][{}].".format(zq_man_exp,str(zq_vc12),zq_man,zq_type,zq_dir),2)
                zq_run.add_success(NE1, "{} Condition verification successful for {} facility [{}][{}][{}].".format(zq_man_exp,str(zq_vc12),zq_man,zq_type,zq_dir),"0.0", "{} CONDITION CHECK".format(zq_man_exp))
            else:
                dprint("KO\t{} Condition verification failure for {} facility.".format(zq_man_exp, str(zq_vc12)),2)
                dprint("\t\tCOND: Exp [{}]  - Rcv [{}]".format(zq_man_exp,zq_man),2)
                dprint("\t\tTYPE: Exp [{}] - Rcv [{}]".format(zq_type_exp,zq_type),2)
                dprint("\t\tDIR : Exp [{}]  - Rcv [{}]".format(zq_dir_exp,zq_dir),2)
                zq_run.add_failure(NE1,"{} CONDITION CHECK".format(zq_man_exp),"0.0","{} Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}]".format(zq_man_exp, str(zq_vc12),zq_man_exp,zq_type_exp,zq_dir_exp,zq_man,zq_type,zq_dir),
                                       "{} Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}] {}".format(zq_man_exp, str(zq_vc12),zq_man_exp,zq_type_exp,zq_dir_exp,zq_man,zq_type,zq_dir,QS_000_Print_Line_Function()))
        
    return


def QS_100_Check_Alarm(zq_run, NE1, ONT, zq_ONT_p1, zq_ONT_p2, zq_mtx_slot, zq_vc4_1, zq_vc4_2, zq_alm_type):
    
    zq_vc4_ch1="{}.1.1.1".format(str(zq_vc4_1 % E_BLOCK_SIZE))
    zq_vc4_ch2="{}.1.1.1".format(str(zq_vc4_2 % E_BLOCK_SIZE))
     
    #"MVC4-1-1-7-92,VC4:NR,SSF-P,SA,07-29,13-12-21,NEND,RCV"

    zq_vc4_idx1 = "MVC4-{}-{}".format(zq_mtx_slot,str(zq_vc4_1))
    zq_vc4_idx2 = "MVC4-{}-{}".format(zq_mtx_slot,str(zq_vc4_2)) 

    ONT.get_set_rx_lo_measure_channel(zq_ONT_p1, zq_vc4_ch1)
    ONT.get_set_rx_lo_measure_channel(zq_ONT_p2, zq_vc4_ch2)

    ONT.get_set_tx_lo_measure_channel(zq_ONT_p1, zq_vc4_ch1)
    ONT.get_set_tx_lo_measure_channel(zq_ONT_p2, zq_vc4_ch2)
    
    ONT.get_set_alarm_insertion_mode(zq_ONT_p1, "HI", "CONT")
    ONT.get_set_alarm_insertion_mode(zq_ONT_p2, "HI", "CONT")

    ONT.get_set_alarm_insertion_type(zq_ONT_p1, zq_alm_type)
    ONT.get_set_alarm_insertion_type(zq_ONT_p2, zq_alm_type)

    ONT.get_set_alarm_insertion_activation(zq_ONT_p1,"HI","ON")

    time.sleep(1)

    if zq_alm_type == 'HPPLM':
        QS_92_Check_MVC4_Alarm(zq_run, NE1,zq_vc4_idx1,"PLM-P","NEND","RCV")
    else:
        QS_92_Check_MVC4_Alarm(zq_run, NE1,zq_vc4_idx1,"SSF-P","NEND","RCV")

    ONT.get_set_alarm_insertion_activation(zq_ONT_p1,"HI","OFF")
    ONT.get_set_alarm_insertion_activation(zq_ONT_p2,"HI","ON")
        
    time.sleep(1)
        
    if zq_alm_type == 'HPPLM':
        QS_92_Check_MVC4_Alarm(zq_run, NE1,zq_vc4_idx2,"PLM-P","NEND","RCV")
    else:
        QS_92_Check_MVC4_Alarm(zq_run, NE1,zq_vc4_idx2,"SSF-P","NEND","RCV")
            
    ONT.get_set_alarm_insertion_activation(zq_ONT_p2,"HI","OFF")

    time.sleep(5)
    
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


def QS_100_Check_BBE_ES_SES_UAS_TCA(zq_run,
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
    time.sleep(20)
    zq_tca_bbe = False
    zq_tca_es  = False
    zq_tca_ses = False
    for zq_i in range(1,80):
        time.sleep(20)
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
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "PM counter [{}]-[15-MIN] for {} are still 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
    
            dprint("\tPM counter BBE: {}".format(zq_bbe),2)
            dprint("\tPM counter  ES: {}".format(zq_es),2)
            dprint("\tPM counter SES: {}".format(zq_ses),2)
            
            if (int(zq_bbe) >= E_BBE_HOVC_15_ON) and (not zq_tca_bbe):
                zq_tca_bbe = True
                dprint("BBE threshold 15-MIN reached...check TCA Alarm presence",2)
                QS_150_Check_TCA(zq_run, NE1,zq_vc4_idx1,"WR","T-BBE-HOVC-15-MIN","NSA",zq_locn,zq_dir)

            if (int(zq_es) >= E_ES_HOVC_15_ON) and (not zq_tca_es):
                zq_tca_es = True
                dprint("ES  threshold 15-MIN reached...check TCA Alarm presence",2)
                QS_150_Check_TCA(zq_run, NE1,zq_vc4_idx1,"WR","T-ES-HOVC-15-MIN","NSA",zq_locn,zq_dir)
                
            if (int(zq_ses) >= E_SES_HOVC_15_ON) and (not zq_tca_ses):
                zq_tca_ses = True
                dprint("SES  threshold 15-MIN reached...check TCA Alarm presence",2)
                QS_150_Check_TCA(zq_run, NE1,zq_vc4_idx1,"WR","T-SES-HOVC-15-MIN","NSA",zq_locn,zq_dir)
                
    
        if zq_period == "BOTH" or zq_period == "1-DAY":  
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

            if (int(zq_bbe) >= E_BBE_HOVC_24_ON) and (not zq_tca_bbe):
                zq_tca_bbe = True
                dprint("BBE threshold 1-DAY reached...check TCA Alarm presence",2)
                QS_150_Check_TCA(zq_run, NE1,zq_vc4_idx1,"WR","T-BBE-HOVC-1-DAY","NSA",zq_locn,zq_dir)

            if (int(zq_es) >= E_ES_HOVC_24_ON) and (not zq_tca_es):
                zq_tca_es = True
                dprint("ES  threshold 1-DAY reached...check TCA Alarm presence",2)
                QS_150_Check_TCA(zq_run, NE1,zq_vc4_idx1,"WR","T-ES-HOVC-1-DAY","NSA",zq_locn,zq_dir)
                
            if (int(zq_ses) >= E_SES_HOVC_24_ON) and (not zq_tca_ses):
                zq_tca_ses = True
                dprint("SES  threshold 1-DAY reached...check TCA Alarm presence",2)
                QS_150_Check_TCA(zq_run, NE1,zq_vc4_idx1,"WR","T-SES-HOVC-1-DAY","NSA",zq_locn,zq_dir)

        if zq_tca_bbe and zq_tca_es and zq_tca_ses:
            dprint("All TCA alarms set after {} min".format(zq_i*20//60),2)
            break  
        
            
    ONT.get_set_error_activation(zq_ONT_p1, "HO", "OFF")
    

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

def QS_107_Check_TIM(zq_run, NE1, ONT, zq_ONT_p1, zq_ONT_p2, zq_mtx_slot, zq_vc4_1, zq_vc4_2):
    
    for zq_j in range(1,4):
        zq_tu3_ch1="{}.{}.1.1".format(str(zq_vc4_1 % E_BLOCK_SIZE),str(zq_j))
        zq_tu3_ch2="{}.{}.1.1".format(str(zq_vc4_2 % E_BLOCK_SIZE),str(zq_j))
         
        zq_tu3_idx1="MVC4TU3-{}-{}-{}".format(zq_mtx_slot,str(zq_vc4_1),str(zq_j))
        zq_tu3_idx2="MVC4TU3-{}-{}-{}".format(zq_mtx_slot,str(zq_vc4_2),str(zq_j))
    
        ONT.get_set_rx_lo_measure_channel(zq_ONT_p1, zq_tu3_ch1)
        ONT.get_set_rx_lo_measure_channel(zq_ONT_p2, zq_tu3_ch2)
    
        ONT.get_set_tx_lo_measure_channel(zq_ONT_p1, zq_tu3_ch1)
        ONT.get_set_tx_lo_measure_channel(zq_ONT_p2, zq_tu3_ch2)

        QS_075_Enable_Disable_TRCMON(zq_run, NE1, zq_tu3_idx1, "Y")
        QS_075_Enable_Disable_TRCMON(zq_run, NE1, zq_tu3_idx2, "Y")
        
        QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_tu3_idx1, E_LO_TI)
        QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_tu3_idx2, E_LO_TI)
        time.sleep(E_WAIT)
        time.sleep(E_WAIT)
        time.sleep(E_WAIT)

        #VERIFY INITIAL NOT ALARM CONDITION ON LOVC3
        #MVC4TU3-1-1-7-<MVC4>-1&&-3
        QS_150_Check_No_Alarm(zq_run, NE1, "MVC4TU3-{}-{}-1&&-3".format(zq_mtx_slot,str(zq_vc4_1)))
        QS_150_Check_No_Alarm(zq_run, NE1, "MVC4TU3-{}-{}-1&&-3".format(zq_mtx_slot,str(zq_vc4_2)))
        
        #Change expected string on TU3 so that TIM-V condition is raised on LOVC3
        QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_tu3_idx1, E_BAD_TI)
        QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_tu3_idx2, E_BAD_TI)
        time.sleep(E_WAIT)
        time.sleep(E_WAIT)
        time.sleep(E_WAIT)

        QS_95_Check_MVC4TU3_Alarm(zq_run, NE1, zq_tu3_idx1,"TIM-V","NEND","RCV")
        QS_95_Check_MVC4TU3_Alarm(zq_run, NE1, zq_tu3_idx1,"TIM-V","NEND","TRMT")
        QS_95_Check_MVC4TU3_Alarm(zq_run, NE1, zq_tu3_idx2,"TIM-V","NEND","RCV")
        QS_95_Check_MVC4TU3_Alarm(zq_run, NE1, zq_tu3_idx2,"TIM-V","NEND","TRMT")

        #Change TIM sent from ONT into the expected on TU3 so that LP-TIM alarm is raised on ONT ports
        ONT.get_set_tu_path_trace_tx_TR16_string(zq_ONT_p1,"ABCDEFGHIJKL   ")
        ONT.get_set_tu_path_trace_tx_TR16_string(zq_ONT_p2,"ABCDEFGHIJKL   ")

        QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p1, "LP-TIM")
        QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p2, "LP-TIM")

        #Restore original TIM sent from ONT into the expected on TU3 so that LP-TIM alarm cleared on ONT ports
        ONT.get_set_tu_path_trace_tx_TR16_string(zq_ONT_p1,"ONT LO-TRACE   ")
        ONT.get_set_tu_path_trace_tx_TR16_string(zq_ONT_p2,"ONT LO-TRACE   ")

        QS_075_Enable_Disable_TRCMON(zq_run, NE1, zq_tu3_idx1, "N")
        QS_075_Enable_Disable_TRCMON(zq_run, NE1, zq_tu3_idx2, "N")

        QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_tu3_idx1, E_DEF_TI)
        QS_055_Modify_MVC4TU3_LO_Trace_Block(zq_run, NE1, zq_tu3_idx2, E_DEF_TI)

        time.sleep(E_WAIT)
        time.sleep(E_WAIT)
        time.sleep(E_WAIT)

        QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p1, "")
        QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p2, "")

        QS_150_Check_No_Alarm(zq_run, NE1, "MVC4TU3-{}-{}-1&&-3".format(zq_mtx_slot,str(zq_vc4_1)))
        QS_150_Check_No_Alarm(zq_run, NE1,"MVC4TU3-{}-{}-1&&-3".format(zq_mtx_slot,str(zq_vc4_2)))
    
    
    return


def QS_108_Check_TIM(zq_run, NE1, ONT, zq_ONT_p1, zq_ONT_p2, zq_mtx_slot, zq_vc4_1, zq_vc4_2):
    
    for zq_j in  E_TUG3:
        for zq_m in E_TUG2:
            for zq_l in E_TU12:
            
                zq_tu12_ch1="{}.{}.{}.{}".format(str(zq_vc4_1 % E_BLOCK_SIZE),str(zq_j),str(zq_m),str(zq_l))
                zq_tu12_ch2="{}.{}.{}.{}".format(str(zq_vc4_2 % E_BLOCK_SIZE),str(zq_j),str(zq_m),str(zq_l))

                zq_tu12_idx1="MVC4TU12-{}-{}-{}-{}-{}".format(zq_mtx_slot,str(zq_vc4_1),str(zq_j),str(zq_m),str(zq_l))
                zq_tu12_idx2="MVC4TU12-{}-{}-{}-{}-{}".format(zq_mtx_slot,str(zq_vc4_2),str(zq_j),str(zq_m),str(zq_l))
           
                ONT.get_set_rx_lo_measure_channel(zq_ONT_p1, zq_tu12_ch1)
                ONT.get_set_rx_lo_measure_channel(zq_ONT_p2, zq_tu12_ch2)
            
                ONT.get_set_tx_lo_measure_channel(zq_ONT_p1, zq_tu12_ch1)
                ONT.get_set_tx_lo_measure_channel(zq_ONT_p2, zq_tu12_ch2)
        
                QS_077_Enable_Disable_TRCMON(zq_run, NE1, zq_tu12_idx1, "Y")
                QS_077_Enable_Disable_TRCMON(zq_run, NE1, zq_tu12_idx2, "Y")
                
                QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_tu12_idx1, E_LO_TI)
                QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_tu12_idx2, E_LO_TI)
                time.sleep(E_WAIT)
                time.sleep(E_WAIT)
                time.sleep(E_WAIT)
        
                #VERIFY INITIAL NOT ALARM CONDITION ON LOVC12
                #MVC4TU3-1-1-7-<MVC4>-1&&-3
                QS_155_Check_No_Alarm(zq_run, NE1, "MVC4TU12-{}-{}-1&&-3-1&&-7-1&&-3".format(zq_mtx_slot,str(zq_vc4_1)))
                QS_155_Check_No_Alarm(zq_run, NE1, "MVC4TU12-{}-{}-1&&-3-1&&-7-1&&-3".format(zq_mtx_slot,str(zq_vc4_2)))
                
                #Change expected string on TU3 so that TIM-V condition is raised on LOVC12
                QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_tu12_idx1, E_BAD_TI)
                QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_tu12_idx2, E_BAD_TI)
                time.sleep(E_WAIT)
                time.sleep(E_WAIT)
                time.sleep(E_WAIT)
        
                QS_97_Check_MVC4TU12_Alarm(zq_run, NE1, zq_tu12_idx1,"TIM-V","NEND","RCV")
                QS_97_Check_MVC4TU12_Alarm(zq_run, NE1, zq_tu12_idx1,"TIM-V","NEND","TRMT")
                QS_97_Check_MVC4TU12_Alarm(zq_run, NE1, zq_tu12_idx2,"TIM-V","NEND","RCV")
                QS_97_Check_MVC4TU12_Alarm(zq_run, NE1, zq_tu12_idx2,"TIM-V","NEND","TRMT")
        
                #Change TIM sent from ONT into the expected on TU3 so that LP-TIM alarm is raised on ONT ports
                ONT.get_set_tu_path_trace_tx_J2_TR16_string(zq_ONT_p1,"ABCDEFGHIJKL   ")
                ONT.get_set_tu_path_trace_tx_J2_TR16_string(zq_ONT_p2,"ABCDEFGHIJKL   ")
        
                QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p1, "LP-TIM")
                QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p2, "LP-TIM")
        
                #Restore original TIM sent from ONT into the expected on TU3 so that LP-TIM alarm cleared on ONT ports
                ONT.get_set_tu_path_trace_tx_J2_TR16_string(zq_ONT_p1,"ONT LO-TRACE   ")
                ONT.get_set_tu_path_trace_tx_J2_TR16_string(zq_ONT_p2,"ONT LO-TRACE   ")
        
                QS_077_Enable_Disable_TRCMON(zq_run, NE1, zq_tu12_idx1, "N")
                QS_077_Enable_Disable_TRCMON(zq_run, NE1, zq_tu12_idx2, "N")
        
                QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_tu12_idx1, E_DEF_TI)
                QS_057_Modify_MVC4TU12_LO_Trace_Block(zq_run, NE1, zq_tu12_idx2, E_DEF_TI)
        
                time.sleep(E_WAIT)
                time.sleep(E_WAIT)
                time.sleep(E_WAIT)
        
                QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p1, "")
                QS_85_Check_ONT_Alarm(zq_run, NE1, ONT, zq_ONT_p2, "")
        
                QS_155_Check_No_Alarm(zq_run, NE1, "MVC4TU12-{}-{}-1&&-3-1&&-7-1&&-3".format(zq_mtx_slot,str(zq_vc4_1)))
                QS_155_Check_No_Alarm(zq_run, NE1, "MVC4TU12-{}-{}-1&&-3-1&&-7-1&&-3".format(zq_mtx_slot,str(zq_vc4_2)))
        
    
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


def QS_115_Check_UAT(zq_run,
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
                     zq_alm_type=""):

    ##################################################
    #Verify all counters are 0 when path is alarm free
    ##################################################
    if zq_period == "BOTH" or zq_period == "15-MIN":  
        zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
        if zq_uas == 0:
            dprint("OK\tUAS PM counter [{}]-[15-MIN] for {} is 0.".format(zq_locn, zq_vc4_idx1),2)
            zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[15-MIN] for {} is 0.".format(zq_locn, zq_vc4_idx1))
        else:
            zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                    "UAS PM counter [{}]-[15-MIN] for {} not 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
            dprint("KO\tUAS PM counter [{}]-[15-MIN] for {} not 0.".format(zq_locn, zq_vc4_idx1),2)
            dprint("\tPM counter UAS: {}".format(zq_uas),2)
    
    if zq_period == "BOTH" or zq_period == "1-DAY":
        if zq_locn == "BIDIR":
            zq_uas_bi = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
            if zq_uas_bi == 0:
                dprint("OK\tUAS PM counter [{}]-[1-DAY] for {} is 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[1-DAY] for {} is 0.".format(zq_locn, zq_vc4_idx1))
                dprint("\tPM counter UAS: {}".format(zq_uas_bi),2)
        
        else:  
            zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
            if zq_uas == 0:
                dprint("OK\tUAS PM counter [{}]-[1-DAY] for {} is 0.".format(zq_locn, zq_vc4_idx1),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[1-DAY] for {} is 0.".format(zq_locn, zq_vc4_idx1))
            else:
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "UAS PM counter [{}]-[1-DAY] for {} not 0. {}".format(zq_locn, zq_vc4_idx1,QS_000_Print_Line_Function()))
                dprint("KO\tUAS PM counter [{}]-[1-DAY] for {} not 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)


    ###################################################################
    # Insert AU-AIS and HP-RDI to detect UAT alarm
    ###################################################################
    ONT.get_set_alarm_insertion_mode(zq_ONT_p1, "HI", "CONT")
    ONT.get_set_alarm_insertion_type(zq_ONT_p1, zq_alm_type)
    ONT.get_set_alarm_insertion_activation(zq_ONT_p1, "HI","ON" )
    if zq_locn == "BIDIR":
        ONT.get_set_alarm_insertion_type(zq_ONT_p1, "HPRDI")

    NE1.tl1.event_collection_start()
    time.sleep(3)

    for zq_i in range(1,15):

        time.sleep(1)

        ###################################################################
        #Verify UAS counter is incremented 
        ###################################################################
        if zq_period == "BOTH" or zq_period == "15-MIN":  
            zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
            
            if zq_uas != 0:
                dprint("OK\tPM counter [{}]-[15-MIN] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[15-MIN] for {} is {}.".format(zq_locn, zq_vc4_idx1,zq_uas))
            else:
                dprint("KO\tPM counter [{}]-[15-MIN] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas),2)
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "UAS PM counter [{}]-[15-MIN] for {} is still {}. {}".format(zq_locn, zq_vc4_idx1,zq_uas,QS_000_Print_Line_Function()))
            
        if zq_period == "BOTH" or zq_period == "1-DAY":
            if zq_locn == "BIDIR":  
                zq_uas_bi = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
                if zq_uas_bi != 0:
                    dprint("OK\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi),2)
                    zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[1-DAY] for {} is {}.".format(zq_locn, zq_vc4_idx1,zq_uas_bi))
                else:
                    dprint("KO\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi),2)
                    zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                            "UAS PM counter [{}]-[1-DAY] for {} is still {}. {}".format(zq_locn, zq_vc4_idx1,zq_uas_bi,QS_000_Print_Line_Function()))
                
            else:
                zq_uas = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
                
                if zq_uas != 0:
                    dprint("OK\tPM counter [{}]-[1-DAY] for {} were incremented.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS: {}".format(zq_uas),2)
                    zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[1-DAY] for {} is {}.".format(zq_locn, zq_vc4_idx1,zq_uas))
                else:
                    dprint("KO\tPM counter [{}]-[1-DAY] for {} are still 0.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS: {}".format(zq_uas),2)
                    zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                            "UAS PM counter [{}]-[1-DAY] for {} is still {}. {}".format(zq_locn, zq_vc4_idx1,zq_uas,QS_000_Print_Line_Function()))
    
    NE1.tl1.event_collection_stop()
    zq_event_num=int(NE1.tl1.event_collection_size("**"))
    if zq_event_num > 0:
        for zq_elem in NE1.tl1.event_collection_get("**", aid="{}".format(zq_vc4_idx1)):
            if zq_elem.get_eve_type() == 'REPT ALM VC4':
                zq_alm = zq_elem.get_eve_body()
                zq_alm_ary = zq_alm.split(",")
                if (zq_alm_ary[1] == "UAT-HOVC") and (zq_alm_ary[5] == zq_locn) and (zq_alm_ary[0] == "MJ"): 
                    dprint("OK\tAlarm [{}] found for {} ".format(zq_alm,zq_vc4_idx1),2)
                    zq_run.add_success(NE1, "ALARM Reporting","0.0", "Alarm [{}] found for {}.".format(zq_alm, zq_vc4_idx1))
                else:
                    if (zq_locn == 'BIDIR') and (zq_alm_ary[5] == 'FEND'):
                        dprint("OK\tAlarm [{}] found for {} ".format(zq_alm,zq_vc4_idx1),2)
                        zq_run.add_success(NE1, "ALARM Reporting","0.0", "Alarm [{}] found for {}.".format(zq_alm, zq_vc4_idx1))
                    else:    
                        dprint("KO\tAlarm mismatch [{}] for {} ".format(zq_alm,zq_vc4_idx1),2)
                        zq_run.add_failure(NE1, "ALARM Reporting", "0.0", "ALARM Reporting", 
                                                "Alarm mismatch [{}] for {} {}".format(zq_alm,zq_vc4_idx1,QS_000_Print_Line_Function()))
            else:
                dprint("KO\tEVENT mismatch [{}] for {} ".format(zq_elem.get_eve_type(),zq_vc4_idx1),2)
                zq_run.add_failure(NE1, "EVENT Reporting", "0.0", "EVENT Reporting", 
                                        "EVENT mismatch [{}] for {} {}".format(zq_elem.get_eve_type(),zq_vc4_idx1,QS_000_Print_Line_Function()))
    else:
        dprint("KO\tEVENT not found for {} ".format(zq_vc4_idx1),2)
        zq_run.add_failure(NE1, "EVENT Reporting", "0.0", "EVENT Reporting", "EVENTnot found for {} {}".format(zq_vc4_idx1,QS_000_Print_Line_Function()))
                    

    ###################################################################
    # STOP Insertion AU-AIS and HP-RDI to detect UAT alarm
    ###################################################################
    ONT.get_set_alarm_insertion_activation(zq_ONT_p1, "HI","OFF" )
    NE1.tl1.event_collection_start()
    time.sleep(3)

    for zq_i in range(1,5):

        time.sleep(1)

        ###################################################################
        #Verify UAS counter is not incremented 
        ###################################################################
        if zq_period == "BOTH" or zq_period == "15-MIN":  
            zq_uas1 = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")
            time.sleep(1)
            zq_uas2 = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "15-MIN")

            if zq_uas1 == zq_uas2:
                dprint("OK\tPM counter [{}]-[15-MIN] for {} not incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas2),2)
                zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[15-MIN] for {} not incremented:[{}][{}].".format(zq_locn, zq_vc4_idx1,zq_uas1,zq_uas2))
            else:
                dprint("KO\tPM counter [{}]-[15-MIN] for {} incremented.".format(zq_locn, zq_vc4_idx1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas1),2)
                dprint("\tPM counter UAS: {}".format(zq_uas2),2)
                zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                        "UAS PM counter [{}]-[15-MIN] for {} incremented: [{}][{}]. {}".format(zq_locn, zq_vc4_idx1,zq_uas1,zq_uas2,QS_000_Print_Line_Function()))
            
        if zq_period == "BOTH" or zq_period == "1-DAY":
            if zq_locn == "BIDIR":  
                zq_uas_bi1 = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")
                time.sleep(1)
                zq_uas_bi2 = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC-BI", zq_locn, "1-DAY")

                if zq_uas_bi1 == zq_uas_bi2:
                    dprint("OK\tPM counter [{}]-[1-DAY] for {} not incremented.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi1),2)
                    dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi2),2)
                    zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[1-DAY] for {} not incremented:[{}][{}].".format(zq_locn, zq_vc4_idx1,zq_uas_bi1,zq_uas_bi2))
                else:
                    dprint("KO\tPM counter [{}]-[1-DAY] for {} incremented.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi1),2)
                    dprint("\tPM counter UAS-BI: {}".format(zq_uas_bi2),2)
                    zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                            "UAS PM counter [{}]-[1-DAY] for {} incremented: [{}][{}]. {}".format(zq_locn, zq_vc4_idx1,zq_uas_bi1,zq_uas_bi2,QS_000_Print_Line_Function()))
                
            else:
                zq_uas1 = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")
                time.sleep(1)
                zq_uas2 = QS_080_Get_PM_Counter(zq_run, NE1, zq_vc4_idx1,"UAS-HOVC", zq_locn, "1-DAY")

                if zq_uas1 == zq_uas2:
                    dprint("OK\tPM counter [{}]-[1-DAY] for {} not incremented.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS: {}".format(zq_uas1),2)
                    dprint("\tPM counter UAS: {}".format(zq_uas2),2)
                    zq_run.add_success(NE1, "PM Counter Reading","0.0", "UAS PM counter [{}]-[1-DAY] for {} not incremented:[{}][{}].".format(zq_locn, zq_vc4_idx1,zq_uas1,zq_uas2))
                else:
                    dprint("KO\tPM counter [{}]-[1-DAY] for {} incremented.".format(zq_locn, zq_vc4_idx1),2)
                    dprint("\tPM counter UAS: {}".format(zq_uas1),2)
                    dprint("\tPM counter UAS: {}".format(zq_uas2),2)
                    zq_run.add_failure(NE1, "PM Counter Reading", "0.0", "PM Counter Reading", 
                                            "UAS PM counter [{}]-[1-DAY] for {} incremented: [{}][{}]. {}".format(zq_locn, zq_vc4_idx1,zq_uas1,zq_uas2,QS_000_Print_Line_Function()))
    
    NE1.tl1.event_collection_stop()
    zq_event_num=int(NE1.tl1.event_collection_size("A"))
    if zq_event_num > 0:
        for zq_elem in NE1.tl1.event_collection_get("A", aid="{}".format(zq_vc4_idx1)):
            if zq_elem.get_eve_type() == 'REPT ALM VC4':
                zq_alm = zq_elem.get_eve_body()
                zq_alm_ary = zq_alm.split(",")
                if (zq_alm_ary[1] == "UAT-HOVC") and (zq_alm_ary[5] == zq_locn) and (zq_alm_ary[0] == "{}:CL".format(zq_vc4_idx1)): 
                    dprint("OK\tAlarm [{}] cleared for {} ".format(zq_alm,zq_vc4_idx1),2)
                    zq_run.add_success(NE1, "ALARM Reporting","0.0", "Alarm [{}] cleared for {}.".format(zq_alm, zq_vc4_idx1))
                else:
                    if (zq_locn == 'BIDIR') and (zq_alm_ary[5] == 'FEND'):
                        dprint("OK\tAlarm [{}] cleared for {} ".format(zq_alm,zq_vc4_idx1),2)
                        zq_run.add_success(NE1, "ALARM Reporting","0.0", "Alarm [{}] cleared for {}.".format(zq_alm, zq_vc4_idx1))
                    else:
                        dprint("KO\tAlarm clear mismatch [{}] for {} ".format(zq_alm,zq_vc4_idx1),2)
                        zq_run.add_failure(NE1, "ALARM Reporting", "0.0", "ALARM Reporting", 
                                                "Alarm clear mismatch [{}] for {} {}".format(zq_alm,zq_vc4_idx1,QS_000_Print_Line_Function()))
            else:
                dprint("KO\tEVENT mismatch [{}] for {} ".format(zq_elem.get_eve_type(),zq_vc4_idx1),2)
                zq_run.add_failure(NE1, "EVENT Reporting", "0.0", "EVENT Reporting", 
                                        "EVENT mismatch [{}] for {} {}".format(zq_elem.get_eve_type(),zq_vc4_idx1,QS_000_Print_Line_Function()))
    else:
        dprint("KO\tEVENT not found for {} ".format(zq_vc4_idx1),2)
        zq_run.add_failure(NE1, "EVENT Reporting", "0.0", "EVENT Reporting", "EVENTnot found for {} {}".format(zq_vc4_idx1,QS_000_Print_Line_Function()))
    
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


def QS_150_Check_No_Alarm(zq_run, NE1, zq_vc3_range):

    zq_tl1_res=NE1.tl1.do("RTRV-COND-LOVC3::{};".format(zq_vc3_range))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("OK\tPath is alarm free.",2)
        zq_run.add_success(NE1,"Path is alarm free.","0.0","CONDITION ALARMS CHECK")
    else:
        dprint("KO\tAlarms are present on path.",2)
        zq_run.add_failure(NE1,"CONDITION ALARMS CHECK","0.0","Alarms are present on path.","Alarms are present on path. "+QS_000_Print_Line_Function())

    return


def QS_150_Check_TCA(zq_run, 
                     NE1,
                     zq_vc4_idx,
                     zq_cond_code,
                     zq_cond_type,
                     zq_sev,
                     zq_locn,
                     zq_dir):

    # RTRV-ALM-VC4:[TID]:AID:[CTAG]::[NTFCNCDE],[CONDTYPE],[SRVEFF],[LOCN],[DIRN]
    zq_tl1_res=NE1.tl1.do("RTRV-ALM-VC4::{}:::{},{},{},{},{};".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        if zq_msg.get_cmd_response_size() == 1:
            dprint("OK\tPM Check TCA successful for {}: [{}]-[{}]-[{}]-[{}]-[{}]".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir),2)
            zq_run.add_success(NE1, "TL1 Command","0.0", "PM Check TCA successful for {}: [{}]-[{}]-[{}]-[{}-[{}]]".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir))
        else:
            zq_run.add_failure(NE1, "TL1 Command", "0.0", "TL1 Command", 
                                    "PM TCA Fail for {}: [{}]-[{}]-[{}]-[{}]-[{}] {}".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir,QS_000_Print_Line_Function()))
            dprint("KO\tPM Check TCA fail for {}: [{}]-[{}]-[{}]-[{}]-[{}]".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir),2)
    else:
        zq_run.add_failure(NE1, "TL1 Command", "0.0", "TL1 Command", 
                                "PM TCA Retrieve Command Fail for {}: [{}]-[{}]-[{}]-[{}]-[{}] {}".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir,QS_000_Print_Line_Function()))
        dprint("KO\tPM TCA Retrieve Command Fail for {}: [{}]-[{}]-[{}]-[{}]-[{}]".format(zq_vc4_idx, zq_cond_code, zq_cond_type, zq_sev, zq_locn, zq_dir),2)

    return


def QS_154_Check_No_Alarm(zq_run, NE1, zq_vc4_range):

    zq_tl1_res=NE1.tl1.do("RTRV-COND-VC4::{};".format(zq_vc4_range))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("OK\tPath is alarm free.",2)
        zq_run.add_success(NE1,"Path is alarm free.","0.0","CONDITION ALARMS CHECK")
    else:
        dprint("KO\tAlarms are present on path.",2)
        zq_run.add_failure(NE1,"CONDITION ALARMS CHECK","0.0", "Alarms are present on path.", "Alarms are present on path. "+QS_000_Print_Line_Function())

    return


def QS_155_Check_No_Alarm(zq_run, NE1, zq_vc12_range):

    zq_tl1_res=NE1.tl1.do("RTRV-COND-LOVC12::{};".format(zq_vc12_range))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("OK\tPath is alarm free.",2)
        zq_run.add_success(NE1,"Path is alarm free.","0.0","CONDITION ALARMS CHECK")
    else:
        dprint("KO\tAlarms are present on path.",2)
        zq_run.add_failure(NE1,"CONDITION ALARMS CHECK","0.0","Alarms are present on path.","Alarms are present on path. "+QS_000_Print_Line_Function())

    return


def QS_160_Verify_TCA_Alarm(zq_run, NE1, zq_temp_ary, zq_vc4_idx, zq_alm_exp):

    zq_str = ""
    zq_res = False
    for zq_i in range(1,len(zq_temp_ary)):
        if zq_temp_ary[zq_i].find("{}".format(zq_vc4_idx)) > 0:
            #zq_temp_ary[zq_i] = zq_temp_ary[zq_i].replace("\"","")
            #zq_temp_ary[zq_i] = zq_temp_ary[zq_i].replace(" ","")
            zq_alm_ary = zq_temp_ary[zq_i].split(",")
            zq_alm_ary[4] = "" 
            zq_alm_ary[5] = ""
            zq_sep = ","
            zq_TCA_alm = zq_sep.join(zq_alm_ary)
            zq_TCA_alm = zq_TCA_alm.replace("\"","")
            zq_TCA_alm = zq_TCA_alm.replace(" ","")
            if zq_TCA_alm == zq_alm_exp:
                zq_res = True
                break
            else:
                zq_res = False
    
    if not zq_res:
        zq_str = zq_str + zq_alm_exp        
            
    return (zq_res,zq_str)


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


def QS_1000_Check_AU4_SST(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_status, zq_flag=True, zq_conc=""):
    
    zq_tl1_res=NE1.tl1.do("RTRV-AU4{}::{}AU4{}-{}-{};".format(zq_conc, zq_rate, zq_conc, zq_slot, zq_au4_num))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        zq_sst=zq_msg.get_cmd_sst("{}AU4{}-{}-{}".format(zq_rate, zq_conc, zq_slot, zq_au4_num))
        if (not zq_flag):
            if (zq_status not in str(zq_sst)):
                dprint("OK\t Initial SST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst),2)
                zq_run.add_success(NE1, 
                                 "SST VERIFY",
                                 "0.0", 
                                 "Initial SST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst))
            else:
                dprint("KO\t Initial SST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst),2)
                zq_run.add_failure(NE1,
                                 "SST VERIFY",
                                 "0.0",
                                 "SST Verify Error",
                                 "Initial SST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst)+QS_000_Print_Line_Function())
        else:
            if (zq_status in str(zq_sst)):
                dprint("OK\t Initial SST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst),2)
                zq_run.add_success(NE1, 
                                 "SST VERIFY",
                                 "0.0", 
                                 "Initial SST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst))
            else:
                dprint("KO\t Initial SST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst),2)
                zq_run.add_failure(NE1,
                                 "SST VERIFY",
                                 "0.0",
                                 "SST Verify Error",
                                 "Initial SST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst)+QS_000_Print_Line_Function())
            
    else:
        dprint("KO\t [RTRV-AU4::{}AU4{}-{}-1]".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_sst),2)
        zq_run.add_failure(NE1,
                         "EQUIPMENT RETRIEVAL",
                         "0.0",
                         "Equipment Retrieval Error",
                         "[RTRV-AU4::{}AU4{}-{}-1]".format(zq_rate, zq_conc, zq_slot, zq_au4_num)+QS_000_Print_Line_Function())

    return
    
    
def QS_1050_Check_AU4_PST(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_status, zq_flag=True, zq_conc=""):
    
    zq_tl1_res=NE1.tl1.do("RTRV-AU4{}::{}AU4{}-{}-{};".format(zq_conc, zq_rate, zq_conc, zq_slot, zq_au4_num))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        zq_pst=zq_msg.get_cmd_pst("{}AU4{}-{}-{}".format(zq_rate, zq_conc, zq_slot, zq_au4_num))
        if (not zq_flag):
            if (zq_status not in str(zq_pst)):
                dprint("OK\t Initial PST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst),2)
                zq_run.add_success(NE1, 
                                 "PST VERIFY",
                                 "0.0", 
                                 "Initial PST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst))
            else:
                dprint("KO\t Initial PST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst),2)
                zq_run.add_failure(NE1,
                                 "PST VERIFY",
                                 "0.0",
                                 "PST Verify Error",
                                 "Initial PST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst)+QS_000_Print_Line_Function())
        else:
            if (zq_status in str(zq_pst)):
                dprint("OK\t Initial PST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst),2)
                zq_run.add_success(NE1, 
                                 "PST VERIFY",
                                 "0.0", 
                                 "Initial PST is correct [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst))
            else:
                dprint("KO\t Initial PST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst),2)
                zq_run.add_failure(NE1,
                                 "PST VERIFY",
                                 "0.0",
                                 "PST Verify Error",
                                 "Initial PST is wrong [{}AU4{}-{}-{}]: {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pst)+QS_000_Print_Line_Function())
            
    else:
        dprint("KO\t [RTRV-AU4::{}AU4{}-{}-{}]".format(zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_failure(NE1,
                         "EQUIPMENT RETRIEVAL",
                         "0.0",
                         "Equipment Retrieval Error",
                         "[RTRV-AU4::{}AU4{}-{}-{}]".format(zq_rate, zq_conc, zq_slot, zq_au4_num)+QS_000_Print_Line_Function())

    return
    
        
def QS_1100_Create_AU4_XC(zq_run, NE1, zq_rate_from, zq_slot1, zq_au4_1, zq_au4_2, zq_cct="2WAY", zq_conc="", zq_slot2="", zq_rate_to=""):

    zq_from = "{}AU4{}-{}-{}".format(zq_rate_from, zq_conc, zq_slot1, zq_au4_1)
    zq_to = "{}AU4{}-{}-{}".format(zq_rate_to, zq_conc, zq_slot1, zq_au4_2)
    if zq_slot2 != "":
        if zq_rate_to != "":
            zq_to = "{}AU4{}-{}-{}".format(zq_rate_to, zq_conc, zq_slot2, zq_au4_2)
        else:
            zq_to = "{}AU4{}-{}-{}".format(zq_rate_from, zq_conc, zq_slot2, zq_au4_2)
        
    zq_tl1_res=NE1.tl1.do("ENT-CRS-VC4{}::{},{}:::{};".format(zq_conc, zq_from, zq_to, zq_cct))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\t [{}] Cross-connection from {} to {} creation successful".format(zq_cct, zq_from, zq_to),2)
        zq_run.add_success(NE1, 
                         "CROSS-CONNECTION CREATION",
                         "0.0", 
                         "[{}] Cross-connection from {} to {} creation successful".format(zq_cct, zq_from, zq_to))
    else:
        dprint("KO\t {} Cross-connection from {} to {} creation failed".format(zq_cct, zq_from, zq_to),2)
        zq_run.add_failure(NE1,
                         "CROSS-CONNECTION CREATION",
                         "0.0",
                         "Cross-Connection Creation Error",
                         "[{}] Cross-connection from {} to {} creation failed".format(zq_cct, zq_from, zq_to)+QS_000_Print_Line_Function())

    
    return


def QS_1200_Delete_AU4_XC(zq_run, NE1, zq_rate_from, zq_slot1, zq_au4_1, zq_au4_2, zq_cct="2WAY", zq_conc="",zq_slot2="", zq_rate_to=""):

    zq_from = "{}AU4{}-{}-{}".format(zq_rate_from, zq_conc, zq_slot1, zq_au4_1)
    zq_to = "{}AU4{}-{}-{}".format(zq_rate_to, zq_conc, zq_slot1, zq_au4_2)
    if zq_slot2 != "":
        if zq_rate_to != "":
            zq_to = "{}AU4{}-{}-{}".format(zq_rate_to, zq_conc, zq_slot2, zq_au4_2)
        else:
            zq_to = "{}AU4{}-{}-{}".format(zq_rate_from, zq_conc, zq_slot2, zq_au4_2)
        
    zq_tl1_res=NE1.tl1.do("DLT-CRS-VC4{}::{},{}:::{};".format(zq_conc, zq_from, zq_to, zq_cct))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\t [{}] Cross-connection from {} to {} deletion successful".format(zq_cct, zq_from, zq_to),2)
        zq_run.add_success(NE1, 
                         "CROSS-CONNECTION DELETION",
                         "0.0", 
                         "[{}] Cross-connection from {} to {} deletion successful".format(zq_cct, zq_from, zq_to))
    else:
        dprint("KO\t [{}] Cross-connection from {} to {} deletion failed".format(zq_cct, zq_from, zq_to),2)
        zq_run.add_failure(NE1,
                         "CROSS-CONNECTION DELETION",
                         "0.0",
                         "Cross-Connection Deletion Error",
                         "[{}] Cross-connection from {} to {} deletion failed".format(zq_cct, zq_from, zq_to)+QS_000_Print_Line_Function())
    return

def QS_1300_Change_STMn_Structure(zq_run, NE1, zq_rate, zq_slot, zq_struct):
    
    zq_tl1_res=NE1.tl1.do("ED-{}::{}-{}::::HOSTRUCT={};".format(zq_rate, zq_rate, zq_slot, zq_struct))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\t {}-{} structure change to {} successful".format(zq_rate, zq_slot, zq_struct),2)
        zq_run.add_success(NE1, 
                         "HO STRUCTURE MODIFY",
                         "0.0", 
                         "{}-{} structured to {}".format(zq_rate, zq_slot, zq_struct))
    else:
        dprint("KO\t {}-{} structure change to {} failed".format(zq_rate, zq_slot, zq_struct),2)
        zq_run.add_failure(NE1,
                         "HO STRUCTURE MODIFY",
                         "0.0",
                         "HO Structure Modify Error",
                         "{}-{} structure change to {} failed".format(zq_rate, zq_slot, zq_struct)+QS_000_Print_Line_Function())
    
    return

def QS_1400_Change_STMn_PST(zq_run, NE1, zq_rate, zq_slot, zq_status):
    
    zq_tl1_res=NE1.tl1.do("ED-{}::{}-{}:::::{};".format(zq_rate, zq_rate, zq_slot, zq_status))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("OK\t {}-{} status changed to {} successful".format(zq_rate, zq_slot, zq_status),2)
        zq_run.add_success(NE1, 
                         "{} STATUS CHANGE".format(zq_rate),
                         "0.0", 
                         "{}-{} status changed to {}".format(zq_rate, zq_slot, zq_status))
    else:
        dprint("KO\t {}-{} status change to {} failed".format(zq_rate, zq_slot, zq_status),2)
        zq_run.add_failure(NE1,
                         "{} STATUS CHANGE".format(zq_rate),
                         "0.0",
                         "{} Status Change Error".format(zq_rate),
                         "{}-{} status change to {} failed".format(zq_rate, zq_slot, zq_status)+QS_000_Print_Line_Function())
    
    return


def QS_1500_Ena_Dis_AU4_POM(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_pom_enadis, zq_egpom_enadis, zq_conc = ""):

    zq_tl1_res=NE1.tl1.do("ED-AU4{}::{}AU4{}-{}-{}::::POM={},EGPOM={};".format(zq_conc, zq_rate, zq_conc, zq_slot, zq_au4_num, zq_pom_enadis, zq_egpom_enadis))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),2)
    zq_cmd=zq_msg.get_cmd_status()

    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tSetting POM to [{}] and EGPOM to [{}] for {}AU4{}-{}-{} successful"
               .format(zq_pom_enadis, zq_egpom_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_success(NE1, "Setting POM to [{}] and EGPOM to [{}] for {}AU4{}-{}-{} successful".
                           format(zq_pom_enadis,zq_egpom_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),"0.0", "POM and EGPOM setting")

    else:
        dprint("\nKO\tSetting POM to [{}] and EGPOM to [{}] for {}AU4{}-{}-{} failed"
               .format(zq_pom_enadis, zq_egpom_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_failure(NE1,  "TL1 COMMAND","0.0", "Setting POM to [{}] and EGPOM to [{}] for {}AU4{}-{}-{} failed".
                           format(zq_pom_enadis,zq_egpom_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),
                           "Setting POM to [{}] and EGPOM to [{}] for {}AU4{}-{}-{} failed {}".format(zq_pom_enadis,zq_egpom_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num,QS_000_Print_Line_Function()))
        
    return


def QS_1550_Ena_Dis_AU4_TRCMON(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_trcmon_enadis, zq_egtrcmon_enadis, zq_conc = ""):

    zq_tl1_res=NE1.tl1.do("ED-AU4{}::{}AU4{}-{}-{}::::TRCMON={},EGTRCMON={};".format(zq_conc, zq_rate, zq_conc, zq_slot, zq_au4_num, zq_trcmon_enadis, zq_egtrcmon_enadis))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),2)
    zq_cmd=zq_msg.get_cmd_status()

    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tSetting TRCMON to [{}] and EGTRCMON to [{}] for {}AU4{}-{}-{} successful"
               .format(zq_trcmon_enadis, zq_egtrcmon_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_success(NE1, "Setting TRCMON to [{}] and EGTRCMON to [{}] for {}AU4{}-{}-{} successful".
                           format(zq_trcmon_enadis,zq_egtrcmon_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),"0.0", "POM and EGPOM setting")

    else:
        dprint("\nKO\tSetting TRCMON to [{}] and EGTRCMON to [{}] for {}AU4{}-{}-{} failed"
               .format(zq_trcmon_enadis, zq_egtrcmon_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_failure(NE1,  "TL1 COMMAND","0.0", "Setting TRCMON to [{}] and EGTRCMON to [{}] for {}AU4{}-{}-{} failed".
                           format(zq_trcmon_enadis,zq_egtrcmon_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num),
                           "Setting TRCMON to [{}] and EGTRCMON to [{}] for {}AU4{}-{}-{} failed {}".format(zq_trcmon_enadis,zq_egtrcmon_enadis, zq_rate, zq_conc, zq_slot, zq_au4_num,QS_000_Print_Line_Function()))
        
    return


def QS_1600_Modify_AU_Trace(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_trc_exp, zq_egtrc_exp, zq_conc = ""):

    zq_tl1_res=NE1.tl1.do("ED-AU4{}::{}AU4{}-{}-{}::::TRCEXPECTED={},EGTRCEXPECTED={};".format(zq_conc, zq_rate, zq_conc, zq_slot, zq_au4_num, zq_trc_exp, zq_egtrc_exp))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tHO Trace Identifier changed to [TRCEXPECTED={}] [EGTRCEXPECTED={}] for {}AU4{}-{}-{}".
               format(zq_trc_exp, zq_egtrc_exp, zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_success(NE1, "HOTrace Identifier changed to [TRCEXPECTED={}] [EGTRCEXPECTED={}] for {}AU4{}-{}-{}".
               format(zq_trc_exp, zq_egtrc_exp, zq_rate, zq_conc, zq_slot, zq_au4_num),"0.0", "HO Trace Identifier changed")

    else:
        dprint("\nKO\tHO Trace Identifier change failure for {}AU4{}-{}-{}".format(zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", 
        "HO Trace Identifier change failure for {}AU4{}-{}-{} {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, QS_000_Print_Line_Function()))

    return


def QS_1650_Modify_AU_Param(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_param_value, zq_conc = ""):

    zq_tl1_res=NE1.tl1.do("ED-AU4{}::{}AU4{}-{}-{}::::{};".
                          format(zq_conc, zq_rate, zq_conc, zq_slot, zq_au4_num, zq_param_value))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    zq_cmd=zq_msg.get_cmd_status()
    if zq_cmd == (True,'COMPLD'):
        dprint("\nOK\tParameter [{}] changed for {}AU4{}-{}-{}".
               format(zq_param_value, zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_success(NE1, "Parameter [{}] changed for {}AU4{}-{}-{}".
               format(zq_param_value, zq_rate, zq_conc, zq_slot, zq_au4_num),"0.0", "Parameter changed")

    else:
        dprint("\nKO\tParameter change failure for {}AU4{}-{}-{}".format(zq_rate, zq_conc, zq_slot, zq_au4_num),2)
        zq_run.add_failure(NE1, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL", 
        "Parameter change failure for {}AU4{}-{}-{} {}".format(zq_rate, zq_conc, zq_slot, zq_au4_num, QS_000_Print_Line_Function()))

    return



def QS_1700_Check_VC4_Condition(zq_run, NE1, zq_rate, zq_slot, zq_au4_num, zq_cond_exp, zq_locn_exp , zq_dir_exp, zq_conc):

    zq_facility = "{}AU4{}-{}-{}".format(zq_rate, zq_conc, zq_slot, zq_au4_num)
    zq_tl1_res=NE1.tl1.do("RTRV-COND-VC4{}::{}:::{},{},{};".format(zq_conc, zq_facility, zq_cond_exp, zq_locn_exp, zq_dir_exp))
    zq_msg=TL1message(NE1.tl1.get_last_outcome())
    dprint(NE1.tl1.get_last_outcome(),1)
    if (zq_msg.get_cmd_response_size() == 0):
        dprint("KO\tCondition verification [{}] for {} not found.".format(zq_cond_exp, zq_facility),2)
        zq_run.add_failure(NE1,"CONDITION CHECK","0.0","Condition verification [{}] for  not found.".format(zq_cond_exp, zq_facility),
                               "Condition verification [{}] for  not found. {}".format(zq_cond_exp, zq_facility, QS_000_Print_Line_Function()))
    else:
        zq_cmd=zq_msg.get_cmd_status()
        if zq_cmd == (True,'COMPLD'):
            zq_cond = zq_msg.get_cmd_attr_value("{},VC4".format(zq_facility), 2)
            zq_locn = zq_msg.get_cmd_attr_value("{},VC4".format(zq_facility), 6)
            zq_dir = zq_msg.get_cmd_attr_value("{},VC4".format(zq_facility), 7)

            zq_cond = zq_cond[0]
            zq_locn = zq_locn[0]
            zq_dir = zq_dir[0]
            
            if (zq_cond == zq_cond_exp) and (zq_locn == zq_locn_exp) and (zq_dir == zq_dir_exp):
                dprint("OK\tCondition verification successful for {} facility [{}][{}][{}].".format(zq_facility, zq_cond_exp, zq_locn, zq_dir),2)
                zq_run.add_success(NE1, "Condition verification successful for {} facility [{}][{}][{}].".format(zq_facility, zq_cond_exp, zq_locn, zq_dir),"0.0", "{} CONDITION CHECK".format(zq_cond_exp))
            else:
                dprint("KO\tCondition verification failure for {} facility.".format(zq_facility),2)
                dprint("\t\tCOND: Exp [{}]  - Rcv [{}]".format(zq_cond_exp,zq_cond),2)
                dprint("\t\tLOCN: Exp [{}] - Rcv [{}]".format(zq_locn_exp,zq_locn),2)
                dprint("\t\tDIR : Exp [{}]  - Rcv [{}]".format(zq_dir_exp,zq_dir),2)
                zq_run.add_failure(NE1, "CONDITION CHECK","0.0","Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}]".
                                   format(zq_facility, zq_cond_exp, zq_locn_exp, zq_dir_exp, zq_cond, zq_locn, zq_dir),
                                   "Condition verification failure for {} facility : Exp: [{}-{}-{}] - Rcv [{}-{}-{}] {}".
                                   format(zq_facility, zq_cond_exp, zq_locn_exp, zq_dir_exp, zq_cond, zq_locn, zq_dir,QS_000_Print_Line_Function()))

    return


def QS_2000_ONT_Check_No_Alarm(zq_run, NE1, ONT1, ONT1_P1, zq_vc4_ch1):
    
    ONT1.get_set_rx_lo_measure_channel(ONT1_P1, zq_vc4_ch1)
    ONT1.get_set_tx_lo_measure_channel(ONT1_P1, zq_vc4_ch1)

    ONT1.start_measurement(ONT1_P1)
    time.sleep(5)
    ONT1.halt_measurement(ONT1_P1)

    zq_res = False
    zq_alm=ONT1.retrieve_ho_alarms(ONT1_P1)
    if zq_alm[0]:
        if  len(zq_alm[1]) == 0:
            dprint("\nOK\tPath is alarm free.",2)
            zq_run.add_success(NE1, "CHECK PATH ALARMS","0.0", "Path is alarm free")
            zq_res = True
        else:
            dprint("\nKO\tAlarms found on path: {}".format(zq_alm[1]),2)
            zq_run.add_failure(NE1, "CHECK PATH ALARMS","0.0", "PATH ALARMS FOUND"
                                , "Path alarms found: {} {}".format(zq_alm[1],QS_000_Print_Line_Function()))
    else:
        dprint("\nKO\tONT command error: {}".format(zq_alm[1]),2)
        zq_run.add_failure(NE1, "ONT COMMAND","0.0", "ONT RETRIEVE ALARM"
                            , "ONT command error: {}".format(zq_alm[1],QS_000_Print_Line_Function()))
        
    return  zq_res

def QS_2100_Set_BER_mode(zq_run, ONT1, ONT1_P1, zq_order, zq_mode, zq_rate, zq_error, zq_num_err, zq_num_noerr):

    ONT1.get_set_error_insertion_mode(ONT1_P1, zq_order, zq_mode)
    ONT1.get_set_error_rate(ONT1_P1, zq_order, zq_rate)
    if zq_mode != 'RATE':
        ONT1.get_set_num_errored_burst_frames(ONT1_P1, zq_order, str(zq_frame_err))
        ONT1.get_set_num_not_errored_burst_frames(ONT1_P1, zq_order, str(zq_frame_noerr))
    ONT1.get_set_error_insertion_type(ONT1_P1, zq_error)
    print("***********************************************")
    print("*\tBER / EBER parameters:")
    print("*\t\tmode: {}".format(zq_mode))
    print("*\t\trate: {}".format(zq_rate))
    if zq_mode != 'RATE':
        print("*\t\terror frames: {}".format(zq_frame_err))
        print("*\t\tno error frames: {}".format(zq_frame_noerr))
    print("***********************************************")

    return

def QS_9999_Time_Measure(zq_action, zq_msg=""):

    global z_start_time
    global z_stop_time

    if zq_action == "START":    
        z_start_time = time.time()
    if zq_action == "STOP":
        z_stop_time = time.time()
        print("\n\t\t\t\t{}: {} [sec.]\n\n".format(zq_msg, str(z_stop_time-z_start_time)))
    
    return

