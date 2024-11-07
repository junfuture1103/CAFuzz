from MiniCmdUtil import MiniCmdUtil
import csv
from tabulate import tabulate
import pickle
import re
import sys
from pathlib import Path
import random
import struct
from datetime import datetime
import os

# mutation!!
cmd_ind = 5

commands_list = []
    
def generate_random_bytes(dataType, length=None):
    if dataType == '--word':
        # 32-bit signed word, Little Endian
        return struct.unpack('<i', struct.pack('<I', random.getrandbits(32)))[0]
    elif dataType == '--half':
        # 16-bit signed half-word, Little Endian
        return struct.unpack('<h', struct.pack('<H', random.getrandbits(16)))[0]
    elif dataType == '--byte':
        # 8-bit signed byte, Little Endian
        return struct.unpack('<b', struct.pack('<B', random.getrandbits(8)))[0]
    elif dataType == 'int': # what the?
        # 32-bit signed word, Little Endian
        return struct.unpack('<i', struct.pack('<I', random.getrandbits(32)))[0]
    elif dataType == '--double':
        # 64-bit double, Little Endian
        return random.uniform(-1.7e+308, 1.7e+308)
    elif dataType == '--string':
        if length is not None:
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
        else:
            raise ValueError("Length required for string type")
    else:
        raise ValueError(f"Unknown data type: {dataType}")
    
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

def checkParams(pickle_file):
    try:
        with open(pickle_file, 'rb') as pickle_obj:
            _, paramNames, _, paramDesc, dataTypesNew, stringLen = pickle.load(
                pickle_obj) # paramDescription is only for GUI
        return len(paramNames) > 0  # if has parameters
    except IOError:
        return False


# 각 요소를 개별 파일에 저장하는 함수
def save_elements_to_separate_files(data_list):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = f"generate_commands/mutation_{timestamp}"

    # 출력 디렉토리가 없으면 생성
    # if not os.path.exists(directory):
    os.makedirs(directory)

    # 각 요소를 개별 파일에 저장
    for i, item in enumerate(data_list):
        filename = os.path.join(directory, f"element_{i+1}.bin")
        with open(filename, "wb") as f:
            f.write(item)

def start_send(host="127.0.0.1",
               port="1234",
               endian="LE",
               pktID="0x1880",
               cmdfilename = "CFE_ES_CMD"):
    
    offsetinit = OffsetInit()

    print("\n===================== [Parameter Def] =====================")
    # pageDefFile = "CFE_ES_CMD"
    pageDefFile = cmdfilename
    # pageDefFile = "CFE_TBL_CMD"
    # pageDefFile = "CFE_TIME_CMD"
    # pageDefFile = "CFE_EVS_CMD"
    # pageDefFile = "CI_LAB_CMD"
    # pageDefFile = "TO_LAB_CMD"
    # pageDefFile = "SAMPLE_APP_CMD"
    
    print("Parameter DefFile : ", pageDefFile)

    pickle_file = f'{ROOTDIR}/CommandFiles/{pageDefFile}'
    with open(pickle_file, 'rb') as pickle_obj:
        cmdDesc, cmdCodes, param_files = pickle.load(pickle_obj)

    headers = ["cmdDesc", "cmdCodes", "param_files"]
    rows = zip(cmdDesc, cmdCodes, param_files)
    print(tabulate(rows, headers, tablefmt="grid"))

    print("cmdCodes len :",len(cmdCodes))
    cmd_ind = random.randint(0, len(cmdCodes)-1)

    command_file_name = param_files[cmd_ind]
    pickle_file = f'{ROOTDIR}/ParameterFiles/' + command_file_name

    print("\n===================== [Parameter] =====================")

    print("pickle_file : ", pickle_file)
    print(f"Command Parameter File Name(index:{cmd_ind}) : ", command_file_name)

    if(checkParams(pickle_file) == False):
        mcu = MiniCmdUtil(host, port, endian, pktID, cmdCodes[cmd_ind])
    else : 
        with open(pickle_file, 'rb') as pickle_obj:
            _, paramNames, _, paramDesc, dataTypesNew, stringLen = pickle.load(
                pickle_obj) # paramDescription is only for GUI

        # using these Lists for extract information dataTypesNew, stringLen

        input_list = [] # input_list means user generate input
        string_index = 0

        print("dataTypesNew :", dataTypesNew)

        for dataType in dataTypesNew:
            if dataType == '--string':
                length = int(stringLen[string_index])
                input_list.append(generate_random_bytes(dataType, length))
            else:
                input_list.append(generate_random_bytes(dataType))
            string_index += 1

        param_list = []
        # k, inpt mean just key:value
        for k, inpt in enumerate(input_list):
            dataType = dataTypesNew[k]
            if dataType == '--string':
                param_list.append(f'{dataType}=\"{stringLen[k]}:{inpt}\"')
            else:
                param_list.append(f'{dataType}={inpt}')  # --byte=4

        param_string = ' '.join(param_list)
        mcu = MiniCmdUtil(host, port, endian, pktID, cmdCodes[cmd_ind], param_string.strip())

        print(f"ParameterFile Name(index:{cmd_ind}) : ", command_file_name)
        print(f"paramNames(len:{len(paramNames)}): ", paramNames)
        print("dataTypesNew : ",dataTypesNew)
        print("stringLen : ",stringLen)
        print("generated input values : ", input_list)
        print("param & input list : ", param_list)

    sendSuccess, sent_packet = mcu.sendPacket()
    print("Command sent successfully:", sendSuccess)
    print("log by mcu generation")

    global commands_list
    commands_list.append(sent_packet)

    # 현재 시간을 타임스탬프로 변환
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # filename = f"test_{timestamp}.bin"

    # # 파일에 저장
    # with open(filename, "wb") as f:
    #     f.write(bytes(sent_packet))
    # f.close()


    for i, v in enumerate(sent_packet):
        print(f"0x{format(v, '02X')}", end=" ")
        if (i + 1) % 8 == 0:
            print()


if __name__ == "__main__":
    # Init main window
    cmdDefFile = "command-pages.txt"
    cmdPageIsValid, cmdPageDesc, cmdPageDefFile, cmdPageAppid, \
        cmdPageEndian, cmdClass, cmdPageAddress, cmdPagePort = ([] for _ in range(8))

    i = 0

    print("\n===================== [cmdDefFile] =====================")

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
    # print(tabulate(quick_rows, quick_headers, tablefmt="grid"))

    send_index = 0  # send_index 변수 선언

    # print(subsys[send_index],
    #       subsysFile[send_index], 
    #       quickCmd[send_index],
    #       cmdPageAddress[send_index],   
    #       cmdPagePort[send_index],     
    #       cmdPageEndian[send_index],   
    #       cmdPageAppid[send_index],    
    #       quickCode[send_index])

    #cmdPageAddress[0] -> There is only a one case! "127.0.0.1 1234 LE"

    # pageDefFile = "CFE_ES_CMD"
    cmdfilenames = ["CFE_ES_CMD", "CFE_SB_CMD", "CFE_TBL_CMD", "CFE_TIME_CMD", "CFE_EVS_CMD", "CI_LAB_CMD", "TO_LAB_CMD", "SAMPLE_APP_CMD"]
    cmdfilename = random.choice(cmdfilenames)

    commands_flow_count = random.randint(1,101)

    for i in range(0, commands_flow_count, 1):
        start_send(
            cmdPageAddress[send_index],
            cmdPagePort[send_index],     
            cmdPageEndian[send_index],   
            hex(cmdPageAppid[send_index]),
            cmdfilename)     
        
        rows = zip(cmdPageIsValid, cmdPageDesc, cmdPageDefFile,)


    save_elements_to_separate_files(commands_list)
