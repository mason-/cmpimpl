#include <stdio.h>
char *const a[] = {"a", "abc", "abcdef"};
int main(){
    printf("a         : %p - %s \n", a, a);
    printf("a[0]      : %p - %s \n", a[0], a[0]);
    printf("*a        : %p - %s \n", *a, *a);
    printf("**a       : %p - %c \n", **a, **a);
}

