#include "vulneribility.h"
#include "fuzzgoat.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

// ============================================================================
// Format String Vulnerability
// ============================================================================
void vuln_printf_string(json_value* value)
{
    #ifdef BUG_ORIGINAL
        printf("string: %s\n", value->u.string.ptr);
    #else

        #ifdef BUG_FORMAT_STRING
        printf("string: ");
        printf(value->u.string.ptr);
        printf("\n");

        #else
        #ifdef BUG_STACK_OVERFLOW
        // printf("using stack buffer to copy string\n");
        char buffer[1024];
        strcpy(buffer, value->u.string.ptr);
        
        printf("string: %s\n", buffer);

        #endif
        #endif


    
    #endif

}
