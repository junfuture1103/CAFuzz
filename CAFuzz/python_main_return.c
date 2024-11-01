#include <stdio.h>
#include <stdlib.h>

int main() {
    // start generate comand using python
    int ret = system("python3 main.py");
    if (ret != 0) {
        fprintf(stderr, "Error executing Python script\n");
        return 1;
    }

    FILE *file = fopen("/tmp/sent_packet.bin", "rb");
    if (!file) {
        fprintf(stderr, "Error opening file\n");
        return 1;
    }

    // sent_packet 데이터를 저장할 배열 할당 (필요한 크기에 따라 조절)
    unsigned char sent_packet[1024];
    size_t bytesRead = fread(sent_packet, sizeof(unsigned char), sizeof(sent_packet), file);
    fclose(file);

    printf("\n ====== python_main_return ====== \n");
    printf("Read %zu bytes from sent_packet.bin:\n", bytesRead);
    for (size_t i = 0; i < bytesRead; i++) {
        printf("0x%02X ", sent_packet[i]);
        if ((i + 1) % 8 == 0) printf("\n");
    }
    return 0;
}
