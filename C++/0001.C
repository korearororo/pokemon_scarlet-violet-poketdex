#include <stdio.h>
#include <stdlib.h> // malloc, free, exit 함수를 위해 필요
#include <string.h> // strlen, strcpy, strstr, strcspn 함수를 위해 필요

int main() {
    int N;
    // 1. 정수 N 입력
    scanf("%d", &N);

    // 2. 검색할 문자열 X를 정적 배열에 입력 (최대 100자 + 널 문자)
    char X[101];
    scanf("%s", X);

    // 3. scanf가 입력 버퍼에 남긴 줄바꿈 문자를 제거 (이후 fgets를 위함)
    getchar(); 

    // 4. 문자열 포인터 배열 Y를 동적으로 할당 (요구사항: Y의 저장소는 동적 할당)
    char **Y = (char **)malloc(N * sizeof(char *));



    char temp_buffer[102]; // N개의 문자열을 임시로 읽을 버퍼 (100자 + \n + \0)
    int max_count = 0;     // X가 가장 많이 발견된 횟수
    int max_index = -1;    // max_count를 가진 문자열의 인덱스
    
    // 6. X 문자열의 길이를 미리 계산 (strstr 연산에 사용)
    // 요구사항: strlen 함수 1회 이상 사용
    int x_len = strlen(X); 

    for (int i = 0; i < N; i++) {
        // 7. 한 줄씩 문자열 입력 (공백 포함, 최대 100자)
        if (fgets(temp_buffer, sizeof(temp_buffer), stdin) == NULL) {
            // 입력 오류 처리
            break; 
        }

        // 8. fgets로 읽은 문자열의 끝에 있는 줄바꿈 문자(\n) 제거
        temp_buffer[strcspn(temp_buffer, "\n")] = '\0';

        // 9. 현재 읽은 문자열의 길이를 계산
        // 요구사항: strlen 함수 1회 이상 사용 (여기서 두 번째 사용, 1회 이상이므로 OK)
        int current_len = strlen(temp_buffer);

        // 10. 문자열을 저장할 공간을 "필요한 만큼만" 동적 할당 (요구사항)
        Y[i] = (char *)malloc((current_len + 1) * sizeof(char));

        // 11. 동적 할당 성공 여부 확인 (요구사항)
        if (Y[i] == NULL) {
            fprintf(stderr, "메모리 할당 실패\n");
            // 이전에 할당된 메모리 해제
            for (int j = 0; j < i; j++) {
                free(Y[j]);
            }
            free(Y);
            return 1;
        }

        // 12. 임시 버퍼의 문자열을 동적 할당된 공간으로 복사
        // 요구사항: strcpy 함수 1회 이상 사용
        strcpy(Y[i], temp_buffer);

        // 13. Y[i] 문자열에서 X 문자열이 "겹치지 않게" 몇 번 나오는지 계산
        int current_count = 0;
        if (x_len > 0) { // 검색할 문자열의 길이가 0이 아닐 때만
            char *ptr = Y[i]; // 검색 시작 위치를 가리키는 포인터
            
            // strstr로 X를 찾고, 찾으면 포인터를 X의 길이만큼 이동시켜 다음 검색
            while ((ptr = strstr(ptr, X)) != NULL) {
                current_count++; // 카운트 증가
                ptr += x_len;    // 포인터를 찾은 문자열의 끝 다음으로 이동
            }
        }

        // 14. 최대값 갱신
        // (current_count > max_count) 조건은
        // 횟수가 같을 경우(>=) 갱신하지 않으므로, "가장 먼저 입력된 문자열"이 유지됨.
        if (current_count > max_count) {
            max_count = current_count;
            max_index = i;
        }
    }

    // 15. 결과 출력
    // max_index가 -1이라는 것은 max_count가 0으로 유지되었다는 의미 (한 번도 못 찾음)
    if (max_index != -1) {
        printf("%s\n", Y[max_index]);
    } else {
        printf("NONE\n");
    }

    // 16. 동적으로 할당된 모든 메모리 해제 (요구사항)
    for (int i = 0; i < N; i++) {
        free(Y[i]); // N개의 각 문자열 메모리 해제
    }
    free(Y); // 포인터 배열 자체의 메모리 해제

    return 0; // 정상 종료
}