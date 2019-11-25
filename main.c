#include <errno.h>
#include <libc.h>
int main(void)
{
	printf("ret = %d\n", printf("sssssss = %ls\n", L"Ō"));
	wchar_t *s = L"Ō";
	printf("d = %ld\n", sizeof(wchar_t));
	printf("sd = %.4x\n", *s);

}
