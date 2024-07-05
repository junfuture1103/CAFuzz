from MiniCmdUtil import MiniCmdUtil

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

    host="127.0.0.1"
    port="1234"
    endian="BE"
    pktID="0x1804"
    cmdCode="0"
    parameters=None

    mcu = MiniCmdUtil(host, port,
                            endian, pktID,
                            cmdCode)
    
    sendSuccess = mcu.sendPacket()
    print("Command sent successfully:", sendSuccess)