from MiniCmdUtil import MiniCmdUtil
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
        self.setTlmOffset
        self.setCmdOffsets
        self.saveOffsets

    def setTlmOffset(self):
        selectedVer = self.cbTlmHeaderVer.currentText().strip()
        if selectedVer == "Custom":
            self.sbTlmOffset.setEnabled(True)
        else:
            self.sbTlmOffset.setEnabled(False)
            if selectedVer == "1":
                self.sbTlmOffset.setValue(self.HDR_VER_1_OFFSET)
            elif selectedVer == "2":
                self.sbTlmOffset.setValue(self.HDR_VER_2_OFFSET)

    def setCmdOffsets(self):
        selectedVer = self.cbCmdHeaderVer.currentText().strip()
        if selectedVer == "Custom":
            self.sbCmdOffsetPri.setEnabled(True)
            self.sbCmdOffsetSec.setEnabled(True)
        else:
            self.sbCmdOffsetPri.setEnabled(False)
            self.sbCmdOffsetSec.setEnabled(False)
            if selectedVer == "1":
                self.sbCmdOffsetPri.setValue(self.HDR_VER_1_OFFSET)
            elif selectedVer == "2":
                self.sbCmdOffsetPri.setValue(self.HDR_VER_2_OFFSET)
            self.sbCmdOffsetSec.setValue(self.HDR_VER_1_OFFSET)

    def saveOffsets(self):
        offsets = bytes((self.sbTlmOffset.value(), self.sbCmdOffsetPri.value(),
                         self.sbCmdOffsetSec.value()))
        with open("/tmp/OffsetData", "wb") as f:
            f.write(offsets)
            

if __name__ == "__main__":
    # Init main window
    offsetinit = OffsetInit()

    ROOTDIR = Path(sys.argv[0]).resolve().parent
    print(ROOTDIR)

    param_file = 'struct_c_f_e___e_s___start_app_cmd__t.html'

    host="127.0.0.1"
    port="1234"
    endian="BE"
    pktID="0x1804"
    cmdCode="0"
    parameters=None

    args = False
    if(args == True):
        mcu = MiniCmdUtil(host, port, endian, pktID, cmdCode)
    else : 
        pickle_file = f'{ROOTDIR}/ParameterFiles/' + re.split(r'\.', param_file)[0]
        with open(pickle_file, 'rb') as pickle_obj:
            _, paramNames, _, paramDesc, dataTypesNew, stringLen = pickle.load(
                pickle_obj)
            
        input_list = []
        for j in range(0,2,1):
            # item = tbl.item(j, 2)
            input_list.append("123")

        print("input_list : ", input_list)

        param_list = []
        for k, inpt in enumerate(input_list):
            dataType = dataTypesNew[k]
            if dataType == '--string':
                param_list.append(f'{dataType}=\"{stringLen[k]}:{inpt}\"')
            else:
                param_list.append(f'{dataType}={inpt}')  # --byte=4

        print("k, inpt, param_list : ", k, inpt, param_list)
        param_string = ' '.join(param_list)

        mcu = MiniCmdUtil(host, port, endian, pktID, cmdCode, param_string.strip())
    sendSuccess = mcu.sendPacket()
    print("Command sent successfully:", sendSuccess)