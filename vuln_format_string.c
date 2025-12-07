#include "vulneribility.h"
#include "fuzzgoat.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

#ifdef BUG_FORMAT_STRING
void vuln_format_string(json_value* value){
    
    printf("string: ");
    // 若value->u.string.ptr包含格式化字符串，可能导致格式化字符串漏洞
    printf(value->u.string.ptr); 
    printf("\n");
}
#else
void vuln_format_string(json_value* value){
    printf("string: %s\n", value->u.string.ptr);
}
#endif