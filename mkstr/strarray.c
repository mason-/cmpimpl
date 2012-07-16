#include <stdio.h>
#include <string.h>
#include <windows.h>

// for (i = 0; i < argc; i++) {
//     printf(argv[i]);
//     putchar(' ');
// }
char buf[] = {
    0x56,                    // push esi
    0x8b, 0x74, 0x24, 0x14,  // mov esi, dword ptr[esp+20]
    0xff, 0x36,              // 0:  push dword ptr[esi]
    0x83, 0xc6, 0x04,        //     add esi, 4
    0xff, 0x54, 0x24, 0x0c,  //     call [esp+12]
    0x83, 0xc4, 0x04,        //     add esp, 0x4
    0x6a, 0x20,              //     push 32
    0xff, 0x54, 0x24, 0x10,  //     call [esp+16]
    0x83, 0xc4, 0x04,        //     add esp, 0x4
    0xff, 0x4c, 0x24, 0x10,  //     dec dword ptr[esp+16]
    0x75, 0xe5,              //     jnz 0b
    0x5e,                    // pop esi
    0xc3,                    // ret
};

int main(int argc, char *argv[]) {
    char *p = (char *)VirtualAlloc(
        0, sizeof(buf), MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    memcpy(p, buf, sizeof(buf));
    ((void (*)(void *, void *, int, void *))p)(
        printf, putchar, argc, argv);
    VirtualFree(p, 0, MEM_RELEASE);
    printf("\n");
    return 0;
}
