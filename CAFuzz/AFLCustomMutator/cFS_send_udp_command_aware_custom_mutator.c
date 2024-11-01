#include <time.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <sys/select.h>

#include "afl-fuzz.h"

static int my_debug = 0;
static int my_read = 0;

#define DEBUG(...) if (my_debug) printf(__VA_ARGS__)

#define DATA_SIZE (10000)

typedef struct udp_send_mutator {
    afl_state_t* afl;
    u8 *mutated_out;
    struct sockaddr_in server_addr;
} udp_send_mutator_t;

void send_file_data(const char *buffer, size_t buf_size, const char *dest_ip, int dest_port) {

    printf("==== send data! in custom mutator : ====\n\n");
    printf("%s\n\n", buffer);
    printf("========================================\n\n");

    int sockfd;
    struct sockaddr_in destaddr;

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&destaddr, 0, sizeof(destaddr));
    destaddr.sin_family = AF_INET;
    destaddr.sin_port = htons(dest_port);

    if (inet_pton(AF_INET, dest_ip, &destaddr.sin_addr) <= 0) {
        perror("invalid address");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    sendto(sockfd, buffer, buf_size, 0, (const struct sockaddr *)&destaddr, sizeof(destaddr));
    close(sockfd);
}

void *afl_custom_init(afl_state_t* afl, uint32_t seed) {
    const char* ip = getenv("CUSTOM_SEND_IP");
    const char* port = getenv("CUSTOM_SEND_PORT");

    if (getenv("AFL_DEBUG")) my_debug = 1;
    if (getenv("CUSTOM_SEND_READ")) my_read = 1;

    if (!ip || !port) {
       fprintf(stderr, "You forgot to set CUSTOM_SEND_IP and/or CUSTOM_SEND_PORT\n");
       exit(1); 
    }

    udp_send_mutator_t* mutator = calloc(1, sizeof(udp_send_mutator_t));
    if (!mutator) {
       fprintf(stderr, "Failed to allocate mutator struct\n");
       exit(1); 
    }

    mutator->afl = afl;

    bzero(&mutator->server_addr, sizeof(mutator->server_addr));
    mutator->server_addr.sin_family = AF_INET;
    if (inet_pton(AF_INET, ip, &mutator->server_addr.sin_addr) <= 0) {
        fprintf(stderr, "Could not convert target ip address!\n");
        exit(1);
    }
    mutator->server_addr.sin_port = htons(atoi(port));
    
    printf("[+] Custom udp send mutator setup ready to go!\n");

    return mutator;
}

/**
 * Perform custom mutations on a given input
 *
 * (Optional for now. Required in the future)
 *
 * @param[in] data pointer returned in afl_custom_init for this fuzz case
 * @param[in] buf Pointer to input data to be mutated
 * @param[in] buf_size Size of input data
 * @param[out] out_buf the buffer we will work on. we can reuse *buf. NULL on
 * error.
 * @param[in] add_buf Buffer containing the additional test case
 * @param[in] add_buf_size Size of the additional test case
 * @param[in] max_size Maximum size of the mutated output. The mutation must not
 *     produce data larger than max_size.
 * @return Size of the mutated output.
 */
// size_t afl_custom_fuzz(udp_send_mutator_t *data, uint8_t *buf, size_t buf_size,
//                        u8 **out_buf, uint8_t *add_buf,
//                        size_t add_buf_size,  // add_buf can be NULL
//                        size_t max_size) {

//     // Make sure that the packet size does not exceed the maximum size expected by
//     // the fuzzer
//     size_t mutated_size = DATA_SIZE <= max_size ? DATA_SIZE : max_size;


//     // start generate comand using python
//     int ret = system("python3 /home/jun20/jun/kaist_research/CAFuzz/CAFuzz/main.py");
//     if (ret != 0) {
//         fprintf(stderr, "Error executing Python script\n");
//         return 1;
//     }

//     FILE *file = fopen("/tmp/sent_packet.bin", "rb");
//     if (!file) {
//         fprintf(stderr, "Error opening file\n");
//         return 1;
//     }

//     // sent_packet 데이터를 저장할 배열 할당 (필요한 크기에 따라 조절)
//     unsigned char sent_packet[1024];
//     size_t bytesRead = fread(sent_packet, sizeof(unsigned char), sizeof(sent_packet), file);
//     fclose(file);


//     // memcpy(data->mutated_out, buf, buf_size);
//     // Randomly select a command string to add as a header to the packet
//     // memcpy(data->mutated_out, commands[rand() % 3], 3);

//     memcpy(data->mutated_out, sent_packet, buf_size);

//     if (mutated_size > max_size) { mutated_size = max_size; }

//     *out_buf = data->mutated_out;
//     return mutated_size;

// }

// int try_connect(udp_send_mutator_t *mutator, int sock, int max_attempts) {
int try_connect(int max_attempts) {
    while (max_attempts > 0) {
        // if (connect(sock, (struct sockaddr*)&mutator->server_addr, sizeof(mutator->server_addr)) == 0) {
        //     return 0;
        // }

        // Even with AFL_CUSTOM_LATE_SEND=1, there is a race between the
        // application under test having started to listen for connections and
        // afl_custom_fuzz_send being called. To address this race, we attempt
        // to connect N times and sleep a short period of time in between
        // connection attempts.
        struct timespec t;
        t.tv_sec = 6;
        t.tv_nsec = 0;
        nanosleep(&t, NULL);
        --max_attempts;

        printf("=============== send custom udp! ===============\n");
    }
    return 1;
}

// I know that this is verrrrrrrry poor solution but.. 20241102
int try_wait(int max_attempts) {
    while (max_attempts > 0) {
        // if (connect(sock, (struct sockaddr*)&mutator->server_addr, sizeof(mutator->server_addr)) == 0) {
        //     return 0;
        // }

        // Even with AFL_CUSTOM_LATE_SEND=1, there is a race between the
        // application under test having started to listen for connections and
        // afl_custom_fuzz_send being called. To address this race, we attempt
        // to connect N times and sleep a short period of time in between
        // connection attempts.
        struct timespec t;
        t.tv_sec = 1;
        t.tv_nsec = 0;
        nanosleep(&t, NULL);
        --max_attempts;

        printf("=============== send custom udp! ===============\n");
    }
    return 1;
}

// random_int 값을 127.0.0.1:3000으로 전송하는 함수
void send_counts(int random_int) {
    int sock;
    struct sockaddr_in server_addr;

    // 소켓 생성
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        return;
    }

    memset(&server_addr, 0, sizeof(server_addr));

    // 서버 주소 설정
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(3000);
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    // 메시지 버퍼 생성
    char message[50];
    snprintf(message, sizeof(message), "Sent msg flow count: %d", random_int);

    // 메시지 전송
    if (sendto(sock, message, strlen(message), 0, 
               (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Failed to send message");
    } else {
        printf("Sent: \"%s\" to 127.0.0.1:3000\n", message);
    }

    // 소켓 종료
    close(sock);
}

void afl_custom_fuzz_send(udp_send_mutator_t *mutator, uint8_t *buf, size_t buf_size) {
    
    printf("==== afl_custom_fuzz_send ====\n\n");
    
    try_connect(1);

    int random_int = rand() % 101;
    send_counts(random_int);  // random_int 전송

    for (int i = 0; i<random_int; i++){
        try_wait(1);
        // start generate comand using python
        int ret = system("python3 /home/jun20/jun/kaist_research/CAFuzz/CAFuzz/generate_command_not_send.py");
        if (ret != 0) {
            fprintf(stderr, "Error executing Python script\n");
            // continue;
        }

        FILE *file = fopen("/tmp/sent_packet.bin", "rb");
        if (!file) {
            fprintf(stderr, "Error opening file\n");
            // continue;
        }

        // sent_packet 데이터를 저장할 배열 할당 (필요한 크기에 따라 조절)
        unsigned char sent_packet[1024];
        size_t bytesRead = fread(sent_packet, sizeof(unsigned char), sizeof(sent_packet), file);
        fclose(file);

        printf("%s\n\n", buf);
        // 1st sendto => mutated commands
        send_file_data(sent_packet, bytesRead, "127.0.0.1", 1234);
        printf("========================================\n\n");
    }

    // 2nd sendto
    // must send 0x1806c000000302220200 exit cFS command
    // Modify buffer for the 2nd sendto for exit cFS
    const char modified_buffer[10] = {0x18, 0x06, 0xc0, 0x00, 0x00, 0x03, 0x02, 0x22, 0x02, 0x00};
    send_file_data(modified_buffer, 10, "127.0.0.1", 1234);
}

void afl_custom_deinit(udp_send_mutator_t* mutator) {
    free(mutator);
}
