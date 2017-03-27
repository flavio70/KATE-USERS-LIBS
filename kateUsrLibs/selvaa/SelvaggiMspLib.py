#!/usr/bin/env python
'''
.. module::testcase
   :platform: Unix
   :synopsis:This module is used for TDM test case implementation.Provides common functions

.. moduleauthor:: Antonio Selvaggi <antonio.selvaggi.ext@nokia.com>
 
'''   

from katelibs.testcase          import TestCase
from katelibs.eqpt1850tss320    import Eqpt1850TSS320
from katelibs.instrumentONT     import InstrumentONT
from katelibs.swp1850tss320     import SWP1850TSS
from katelibs.facility_tl1      import *
import time
from inspect import currentframe

def PrintLineFunction(gap=0):

    """ Returns a line number in running file .
    :param gap: if equal to 0 identifies current line, else a prevoius or a following line  
     >>> PrintLine()

    """

    cf = currentframe()
    line = cf.f_back.f_lineno + gap
    code = str(cf.f_back.f_code)
    temp = code.split(",")
    function = temp[0].split(" ")
    res = "****** Line [{}] in function [{}]".format(line,function[2])
    
    return res




def dprint(str,level):
    
    """ Print on Eclipse output
    :param str: string printed on output
    :param level: debug level:  0=no print
                                1=TL1 message response
                                2=OK/KO info 
                                4=execution info
                                can be used in combination, i.e.
                                3=TL1 message response+OK/KO info
     
    >>> dprint("KO\t At least a matrix is not in service",2)
            
    """
    
    E_DPRINT = 7    
    
    if (E_DPRINT & level):
        print(str)
    return


def CheckPrimaryState(run, NE, msg, aid, state,line):

    """ Verifies if an entity's (card, module, facility) primary state is correct
    :param run: running instance of class Test
    :param NE:  an equipment variable
    :param msg: the response to the TL1 message retrieve 
    :param aid: the entity's AID
    :param state: the expected primary state
    :param line: the line of file corresponding to function call
     >>> CheckPrimaryState(self, NE1, msg, aidList[i], "IS-NR",PrintLineFunction())
            
    """

    found=False
    
    #time.sleep(2)
    #NE.tl1.do("RTRV-%s::%s;"%(type,aid))        
    
    #msg=TL1message(NE.tl1.get_last_outcome())
    
    cmd=msg.get_cmd_status()
    if cmd == (True,'COMPLD'):
           
        pstList=msg.get_cmd_pst(aid)
        
        if (pstList!=None):
           
            i=0
            
            while (i < len(pstList[0]) and not found)  :
                if (pstList[0][i]==state):
                   found=True
                else:
                   i=i+1
                       
    if(not found):
        dprint("KO\t Primary state of %s is wrong\n"%aid,2)
        run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","Primary state of %s is wrong  %s"%(aid,line))
        
    
        
    return found

def CheckSecondaryState(run, NE, msg, aid, state, line, positive=True, write=True):

    """ Verifies if a state is or is not present between the secondary states of entity's (card, module, facility)
    :param run: running instance of class Test
    :param NE:  an equipment variable
    :param msg: the response to the TL1 message retrieve
    :param aid: the entity's AID
    :param state: the expected secondary state
    :param line: the line of file corresponding to function call
    :param positive: if is equal to True the function is successful if expected state is found, 
                     if it is equal to False the function is successful if expected state is not found,  
    :param write: if is equal to True the function reports is successful if expected state is found, 
                     if it is equal to False the function is successful if expected state is not found,  
     >>> CheckPrimaryState(self, NE1, msg, aidList[i], "IS-NR",PrintLineFunction())
            
    """

    found=False
    
    #time.sleep(2)
    
    #NE.tl1.do("RTRV-%s::%s;"%(type,aid))        
    
    #msg=TL1message(NE.tl1.get_last_outcome())
    
    cmd=msg.get_cmd_status()
    
    if cmd == (True,'COMPLD'):
    
        sstList=msg.get_cmd_sst(aid)
        
        i=0
        
        if (sstList!=None):
        
            while (i < len(sstList[0]) and not found)  :
                if (sstList[0][i]==state):
                   found=True
                else:
                   i=i+1
    if write:                       
            
        if(positive and not found):
            
            dprint("KO\t %s is not a secondary state of %s \n"%(state,aid),2)
            run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","%s is not a secondary state of %s %s\n"%(state,aid,line))
        
        elif(not positive and found):
            
            dprint("KO\t %s is a secondary state of %s \n"%(state,aid),2)
            run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","%s is a secondary state of %s %s\n"%(state,aid,line))
        
        
        
    return found



def CheckIfIsInUasAndDsbldState(run, NE, msg, aid, line):

    isInState=False
    
    if CheckPrimaryState(run, NE, msg, aid, "OOS-AUMA", line) and CheckSecondaryState(run, NE, msg, aid, "UAS", line) and CheckSecondaryState(run, NE, msg, aid, "DSBLD", line):  
       isInState=True
    
    else:
                 
       dprint("KO\t %s is not in UAS&DSBLD state \n"%aid,2)
       run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL"," %s is not in UAS&DSBLD state  %s"%(aid,line))
                
    return isInState

def CheckIfIsNotConfigured(run, NE, msg, aid, line):

    isNotConfigured=False
    
    #time.sleep(2)
    
    #NE.tl1.do("RTRV-%s::%s;"%(type,aid))        
    
    #msg=TL1message(NE.tl1.get_last_outcome())
    
    cmd=msg.get_cmd_status()
    
    if cmd == (True,'COMPLD'):
    
        size=msg.get_cmd_response_size()
        
        if (size==0):
        
            isNotConfigured=True
                       
        if(not isNotConfigured):
                dprint("KO\t %s is unexpectedly configured\n"%aid,2)
                run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","%s is unexpectedly configured %s"%(aid,line))
    else:
                dprint("KO\t Retrieve on %s failed\n"%aid,2)
                run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","Retrieve on %s failed %s"%(aid,line))
        
        
    return isNotConfigured

def Au4InStmN(rate,au4):

    
    conversion = {('STM1','AU4'): 1, ('STM4','AU4'): 4, ('STM4','AU44C'): 1,('STM16','AU4'): 16, ('STM16','AU44C'): 4, ('STM4','AU416C'): 1,('STM64','AU4'): 64, ('STM64','AU44C'): 16, ('STM64','AU416C'): 4,('STM64','AU464C'): 4}
       
    number=conversion.get((rate,au4),0)
                 
    return number


def CheckParameterValue(run, NE, msg,aid,parameter,expValue,line):

    
    #msg=TL1message(NE.tl1.get_last_outcome())
    
    cmd=msg.get_cmd_status()
    if cmd == (True,'COMPLD'):
                     
        parameterList=msg.get_cmd_attr_value(aid, parameter)
        
        if parameterList==None:
                dprint("KO\t RTRV-%s failed \n"%aid,2)
                run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","RTRV-%s failed %s\n"%(aid,line))
                return
              
        if (expValue not in parameterList):
                dprint("KO\t Parameter %s of %s is wrong \n"%(parameter,aid),2)
                run.add_failure(NE, "TL1 COMMAND","0.0", "TL1 COMMAND FAIL","Parameter %s of %s is wrong  %s\n"%(parameter,aid,line))
      
            
    return

def CheckErrorCode(run, NE, msg, expected, line):

    (result,errorCode,errorMessageList)=msg.get_cmd_error_frame()
    
    if (errorCode!=expected):  
            dprint("KO\tNO Wrong error code: %s instead of  %s\n"%(errorCode,expected),2)
            run.add_failure(NE, "TL1 deny error code check","0.0","TL1 deny error code check","KO\tWrong error code: %s instead of  %s  %s\n"%(errorCode,expected, line))
            
    return
                

def CheckEvent (run, NE, marker, line, aid=None, cmd=None, positive=True):

    eSize=NE.tl1.event_collection_size(marker, aid, cmd)
    
    if(positive):
        if (eSize==0): #NO event FOUND
                if(aid==None):
                   aid=""
                if (cmd==None):
                   cmd="" 
                dprint("KO\tNO Event %s reported on aid %s %s\n"%(cmd,aid,line),2)
                run.add_failure(NE, "TL1 report check","0.0","KO TL1 event\n","KO\tNO Event %s reported on aid %s %s\n"%(cmd,aid,line))
    else:
        if (eSize!=0): #event FOUND
                if(aid==None):
                   aid=""
                if (cmd==None):
                   cmd="" 
                dprint("KO\tEvent %s reported on aid %s %s\n"%(cmd,aid, line),2)
                run.add_failure(NE, "TL1 report check","0.0","KO TL1 event\n","KO\t Event %s reported on aid %s %s\n"%(cmd,aid,line))    
    return

def CheckCondition (run, NE, msg, condition_exp, aid, line):

    '''
    Condition_exp same has to be equal [CONDTYPE] parameter of previous RTRV command
    
    If it is different from "" we expect a response having a body with 0 or 1 row
    
    If is void number of rows doesn't matter
     
    '''
    matched=False
    
    cmd=msg.get_cmd_status()
    
    if cmd == (True,'COMPLD'):
    
        responseSize=msg.get_cmd_response_size()
        
        if (responseSize==0): #NO ALARM FOUND
            if condition_exp == "":    #NO ALARM EXPECTED AND NO ALARM FOUND
                dprint("OK\tNO Condition/Alarm found on aid %s\n"%aid,2)
                run.add_success(NE, "TL1 Condition/Alarm check","0.0","NO Condition/Alarm found on aid %s %s\n"%(aid,line))
                
            else:                   #ALARM EXPECTED BUT NO ALARM FOUND  
                dprint("KO\t NO Condition/Alarm found on aid %s\n"%aid,2)
                run.add_failure(NE, "TL1 Condition/Alarm check","0.0","NO Condition/Alarm found on aid %s %s\n"%(aid,line),"No condition/alarm found")
                
        else:
            if condition_exp == "":    #NO ALARM EXPECTED BUT ALARM FOUND
                dprint("KO\t Condition/Alarm found on aid %s\n"%aid,2)
                run.add_failure(NE, "TL1 Condition/Alarm check","0.0","Condition/Alarm found on aid %s %s\n"%(aid,line),"Condition/Alarm wrongly found")
            else:                   #ALARM EXPECTED AND SAME ALARM FOUND  
                dprint("0K\t Condition/Alarm %s found on aid %s\n"%(condition_exp,aid),2)
                run.add_success(NE, "TL1 Condition/Alarm check","0.0","Condition/Alarm %s found on aid %s %s\n"%(condition_exp,aid,line))
                
    return

def CheckONTAlarm(run, NE, ont, ont_port, alm_exp, line, alone=False, measure=True):
    if measure:
        ont.start_measurement(ont_port)
        time.sleep(2)
        ont.halt_measurement(ont_port)

    alm = ont.retrieve_ho_lo_alarms(ont_port)
    if alm[0] == True:           #COMMAND IS OK
        if len(alm[1]) == 0:     #NO ALARM FOUND
            if alm_exp == "":    #NO ALARM EXPECTED AND NO ALARM FOUND
                dprint("OK\tNO Alarm found on ont %s port %s"%(ont,ont_port),2)
                run.add_success(NE, "NO Alarm found on ont %s port %s %s"%(ont,ont_port,line),"0.0", "ont Alarm check")
                
                
            else:                   #ALARM EXPECTED BUT NO ALARM FOUND  
                dprint("KO\t%s not found on ont %s port %s:"%(alm_exp,ont,ont_port),2)
                run.add_failure(NE,  "ont Alarm check","0.0", "ont Alarms check", 
                                     " %s not found on ont %s port %s: Exp [%s]  - Rcv [%s] %s"%(alm_exp,ont,ont_port,alm_exp,"no alarm",line))
                
        else:                       #AT LEAST ONE ALARM FOUND
            if alm_exp == "":    #NO ALARM EXPECTED BUT ALARM FOUND
                alarmString=""
                for alarmIndex in range (0, len (alm[1])):
                    if (alarmIndex==(len (alm[1])-1)):
                        alarmString="%s %s"%(alarmString,alm[1][alarmIndex])
                    else:
                        alarmString="%s %s,"%(alarmString,alm[1][alarmIndex])
                dprint("KO\t%s not expected but found on ont %s port %s"%(alarmString,ont,ont_port),2)
                run.add_failure(NE,  "ont Alarm check","0.0", "ont Alarms check", 
                                     "%s not expected but found on ont %s port %s %s"%(alarmString,ont,ont_port,line))
            else:              
                alarmString=""
                found=False
                for alarmIndex in range (0, len (alm[1])):
                    if alm[1][alarmIndex] == alm_exp:      
                        found= True   
                    else:
                        if (alarmIndex==(len (alm[1])-1)):
                            alarmString="%s %s"%(alarmString,alm[1][alarmIndex])
                        else:
                            alarmString="%s %s,"%(alarmString,alm[1][alarmIndex])
                if found: #Alarm found:
                    if(alone and len(alm[1])>1):
                        dprint("KO\tExpected %s found but is not alone also %s found on ont %s port %s "%(alm_exp,alarmString,ont,ont_port),2)
                        run.add_failure(NE,  "ont Alarm check","0.0", "ont Alarms check", 
                                         "Expected %s found but is not alone also %s found on ont %s port %s  %s"%(alm_exp,alarmString,ont,ont_port,line))
                    else:
                        dprint("OK\t%s found on ont %s port %s"%(alm_exp,ont,ont_port),2)
                        run.add_success(NE, "%s found on ont %s port %s %s"%(alm_exp,ont,ont_port,line),"0.0", "ont Alarm check")
                else: #Expected alarm is not between alarms found 
                    dprint("KO\t%s found but expected %s not found on ont %s port %s "%(alarmString,alm_exp,ont,ont_port),2)
                    run.add_failure(NE,  "ont check","0.0", "ont Alarms check", 
                                         "%s found but expected %s not found on ont %s port %s  %s"%(alarmString,alm_exp,ont,ont_port,line))

    return

def ExtractRate(rateCard):
    
    rate="STM1"
    
    if(rateCard.find("STM4")>=0):
        rate="STM4"
    elif (rateCard.find("STM16")>=0):
        rate="STM16"
    elif (rateCard.find("STM64")>=0):
        rate="STM64"
         
       
    return rate
