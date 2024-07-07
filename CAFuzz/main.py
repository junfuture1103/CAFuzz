from MiniCmdUtil import MiniCmdUtil
import csv
from tabulate import tabulate
import pickle
import re
import sys
from pathlib import Path

class OffsetInit():
    HDR_VER_1_OFFSET = 0
    HDR_VER_2_OFFSET = 4

    #
    # Init the class
    #
    def __init__(self):
        super().__init__()


        self.setTlmOffset()
        self.setCmdOffsets()
        self.saveOffsets()

        self.sbTlmOffset = None
        self.sbCmdOffsetPri = None
        self.sbCmdOffsetSec = None

    def setTlmOffset(self):
        # print("start setTlmOffset()")
        selectedVer = "1"

        if selectedVer == "1":
            self.sbTlmOffset = self.HDR_VER_1_OFFSET
        elif selectedVer == "2":
            self.sbTlmOffset = self.HDR_VER_2_OFFSET
            
    def setCmdOffsets(self):
        # print("start setCmdOffsets()")
        selectedVer = "1"
        
        if selectedVer == "1":
            self.sbCmdOffsetPri = self.HDR_VER_1_OFFSET
        elif selectedVer == "2":
            self.sbCmdOffsetPri = self.HDR_VER_2_OFFSET

        self.sbCmdOffsetSec = self.HDR_VER_1_OFFSET

    def saveOffsets(self):
        # print("start saveOffsets()")
        offsets = bytes((self.sbTlmOffset, self.sbCmdOffsetPri, self.sbCmdOffsetSec))
        with open("/tmp/OffsetData", "wb") as f:
            f.write(offsets)



ROOTDIR = Path(sys.argv[0]).resolve().parent

def start_send(host="127.0.0.1",
               port="1234",
               endian="LE",
               pktID="0x1880",
               cmdCode='struct_c_f_e___e_s___start_app_cmd__t.html',
               params = None):
    
    offsetinit = OffsetInit()

    # param_file from
    param_file = 'struct_c_f_e___e_s___start_app_cmd__t.html'
    param_file = 'TO_OUTPUT_ENABLE_CC'

    cmdCode=cmdCode[0]
    parameters=None

    args = False

    if(args == True):
        mcu = MiniCmdUtil(host, port, endian, pktID, cmdCode)
    else : 
        # 
        pageDefFile = "CFE_ES_CMD"

        pickle_file = f'{ROOTDIR}/CommandFiles/{pageDefFile}'
        with open(pickle_file, 'rb') as pickle_obj:
            cmdDesc, cmdCodes, param_files = pickle.load(pickle_obj)

        headers = ["cmdDesc", "cmdCodes", "param_files"]
        rows = zip(cmdDesc, cmdCodes, param_files)
        print(tabulate(rows, headers, tablefmt="grid"))

        pickle_file = f'{ROOTDIR}/ParameterFiles/' + re.split(r'\.', param_file)[0]

        # print("pickle_file : ", pickle_file)
        with open(pickle_file, 'rb') as pickle_obj:
            _, paramNames, _, paramDesc, dataTypesNew, stringLen = pickle.load(
                pickle_obj) # paramDescription is only for GUI
            
        input_list = []
        for j in range(0,1,1):
            # item = tbl.item(j, 2)
            input_list.append("12")

        print("===================== [Parameter] =====================")
        print("ParameterFile Name : ", re.split(r'\.', param_file))
        print("paramNames, dataTypesNew, stringLen : ", paramNames, dataTypesNew, stringLen)
        print("generated input values : ", input_list)

        param_list = []

        # k, inpt mean just key:value
        for k, inpt in enumerate(input_list):
            dataType = dataTypesNew[k]
            if dataType == '--string':
                param_list.append(f'{dataType}=\"{stringLen[k]}:{inpt}\"')
            else:
                param_list.append(f'{dataType}={inpt}')  # --byte=4

        print("param & input list : ", param_list)

        param_string = ' '.join(param_list)

        mcu = MiniCmdUtil(host, port, endian, pktID, cmdCode, param_string.strip())

    sendSuccess = mcu.sendPacket()
    print("Command sent successfully:", sendSuccess)

if __name__ == "__main__":
    # Init main window
    
    cmdDefFile = "command-pages.txt"
    cmdPageIsValid, cmdPageDesc, cmdPageDefFile, cmdPageAppid, \
        cmdPageEndian, cmdClass, cmdPageAddress, cmdPagePort = ([] for _ in range(8))

    i = 0

    with open(f"{ROOTDIR}/{cmdDefFile}") as cmdfile:
        reader = csv.reader(cmdfile, skipinitialspace=True)
        for cmdRow in reader:
            try:
                if not cmdRow[0].startswith('#'):
                    cmdPageIsValid.append(True)
                    cmdPageDesc.append(cmdRow[0])
                    cmdPageDefFile.append(cmdRow[1])
                    cmdPageAppid.append(int(cmdRow[2], 16))
                    cmdPageEndian.append(cmdRow[3])
                    cmdClass.append(cmdRow[4])
                    cmdPageAddress.append(cmdRow[5])
                    cmdPagePort.append(int(cmdRow[6]))
                    i += 1
            except IndexError as e:
                fullErr = repr(e)
                errName = fullErr[:fullErr.index('(')]
                print(f"{errName}:", e)
                print(("This could be due to improper formatting in "
                       "command-pages.txt.\nThis is a common error "
                       "caused by blank lines in command-pages.txt"))
    #
    # Mark the remaining values as invalid
    #
    for _ in range(i, 22):
        cmdPageAppid.append(0)
        cmdPageIsValid.append(False)

    # Print the values in a tabular format
    headers = ["IsValid", "Description", "DefFile", "AppID", "Endian", "Class", "Address", "Port"]
    rows = zip(cmdPageIsValid, cmdPageDesc, cmdPageDefFile, cmdPageAppid, cmdPageEndian, cmdClass, cmdPageAddress, cmdPagePort)

    print(tabulate(rows, headers, tablefmt="grid"))

    quickDefFile = 'quick-buttons.txt'
    subsys, subsysFile, quickCmd, quickCode, quickPktId,\
        quickEndian, quickAddress, quickPort, quickParam, \
            quickIndices = ([] for _ in range(10))

    with open(f'{ROOTDIR}/{quickDefFile}') as subFile:
        reader = csv.reader(subFile)
        for fileRow in reader:
            if not fileRow[0].startswith('#'):
                subsys.append(fileRow[0])
                subsysFile.append(fileRow[1])
                quickCmd.append(fileRow[2].strip())
                quickCode.append(fileRow[3].strip())
                quickPktId.append(fileRow[4].strip())
                quickEndian.append(fileRow[5].strip())
                quickAddress.append(fileRow[6].strip())
                quickPort.append(fileRow[7].strip())
                quickParam.append(fileRow[8].strip())

    # Print the quick command values in a tabular format
    quick_headers = ["Subsystem", "SubsysFile", "QuickCmd", "QuickCode", "QuickPktId", "QuickEndian", "QuickAddress", "QuickPort", "QuickParam"]
    quick_rows = zip(subsys, subsysFile, quickCmd, quickCode, quickPktId, quickEndian, quickAddress, quickPort, quickParam)
    print(tabulate(quick_rows, quick_headers, tablefmt="grid"))

    send_index = 0  # send_index 변수 선언

    print(  subsys[send_index], 
            subsysFile[send_index], 
            quickCmd[send_index],
            quickAddress[send_index],   
            quickPort[send_index],     
            quickEndian[send_index],   
            quickPktId[send_index],    
            quickCode[send_index])

    start_send(
            quickAddress[send_index],   
            quickPort[send_index],     
            quickEndian[send_index],   
            quickPktId[send_index],    
            quickCode[send_index])     
    

    

    