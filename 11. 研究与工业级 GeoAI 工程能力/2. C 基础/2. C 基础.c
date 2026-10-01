/* C 基础演示：变量、指针、数组、结构体、函数、内存
   编译运行：gcc demo.c -o demo && ./demo
*/
#include <stdio.h>
#include <stdlib.h>

// 结构体：组合多个字段
struct Point {
    int x;
    int y;
};

// 函数：传指针（修改调用方的值）
void add_one(int *p) {
    *p = *p + 1;   // 通过指针修改原值
}

int main() {
    /* 1. 变量与指针 */
    int x = 10;
    int *p = &x;               // p 指向 x 的内存地址
    printf("x = %d\n", x);
    printf("&x = %p（x 的内存地址）\n", (void*)&x);
    printf("p  = %p（指针存的就是地址）\n", (void*)p);
    printf("*p = %d（通过指针取值）\n", *p);

    /* 2. 通过指针修改原值 */
    add_one(p);
    printf("add_one 后 x = %d（指针改了原值）\n", x);

    /* 3. 数组：连续内存 */
    int arr[3] = {1, 2, 3};
    printf("arr[0] = %d, arr[1] = %d, arr[2] = %d\n", arr[0], arr[1], arr[2]);
    printf("arr == &arr[0]：%p vs %p\n", (void*)arr, (void*)&arr[0]);

    /* 4. 结构体 */
    struct Point pt = {112, 28};
    printf("Point = (%d, %d)\n", pt.x, pt.y);

    /* 5. 栈 vs 堆：堆上手动分配内存 */
    int *heap_arr = (int*)malloc(3 * sizeof(int));  // 堆上分配
    heap_arr[0] = 10;
    heap_arr[1] = 20;
    heap_arr[2] = 30;
    printf("堆上 heap_arr[1] = %d\n", heap_arr[1]);
    free(heap_arr);   // 手动释放（忘了会内存泄漏）

    return 0;
}
