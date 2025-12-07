#include "fuzzgoat.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

// VULN_use-after-free=-DBUG_USE_AFTER_FREE
// VULN_invalid-free=-DBUG_INVALID_FREE
// VULN_null-deref=-DBUG_NULL_DEREF
// VULN_stack-overflow=-DBUG_STACK_OVERFLOW
// VULN_heap-overflow=-DBUG_HEAP_OVERFLOW
// VULN_integer-overflow=-DBUG_INTEGER_OVERFLOW
// VULN_format-string=-DBUG_FORMAT_STRING
// VULN_ORIGINAL=-DBUG_ORIGINAL
#if !defined(BUG_ORIGINAL) &&!defined(BUG_USE_AFTER_FREE) && \
    !defined(BUG_INVALID_FREE) && !defined(BUG_NULL_DEREF) && \
    !defined(BUG_STACK_OVERFLOW) && !defined(BUG_HEAP_OVERFLOW) && \
    !defined(BUG_INTEGER_OVERFLOW) &&  !defined(BUG_FORMAT_STRING) 

    #define BUG_ORIGINAL

#endif

void vuln_printf_string(json_value* value);



