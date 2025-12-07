CC=afl-gcc
DEPS=main.c fuzzgoat.c
ASAN=-fsanitize=address
CFLAGS=-I.
LIBS=-lm

# 定義漏洞源文件映射
VULN_SOURCES=vuln_printf_string.c 
			  
VULN_OBJECTS=$(VULN_SOURCES:.c=.o)

# 定義漏洞類型與編譯選項的映射

VULN_ORIGINAL=-DBUG_ORIGINAL
VULN_stack-overflow=-DBUG_STACK_OVERFLOW
VULN_format-string=-DBUG_FORMAT_STRING


# 所有漏洞類型
BUGS=stack-overflow format-string


# all: $(DEPS)
# 	$(CC) -o fuzzgoat $(CFLAGS) $^ $(LIBS)
# 	$(CC) $(ASAN) -o fuzzgoat_ASAN $(CFLAGS) $^ $(LIBS)

# afl: fuzzgoat
# 	afl-fuzz -i in -o out ./fuzzgoat @@

# ===============================================

# 預設編譯所有版本
all: fuzzgoat fuzzgoat_ASAN

# 原始版本（包含所有漏洞）
fuzzgoat: main.c fuzzgoat.c $(VULN_SOURCES) vulneribility.h
	$(CC) -DBUG_ORIGINAL -o $@ $(CFLAGS) main.c fuzzgoat.c $(VULN_SOURCES) $(LIBS)

fuzzgoat_ASAN: main.c fuzzgoat.c $(VULN_SOURCES) vulneribility.h
	$(CC) -DBUG_ORIGINAL $(ASAN) -o $@ $(CFLAGS) main.c fuzzgoat.c $(VULN_SOURCES) $(LIBS)

# 編譯特定漏洞版本的模式規則
fuzzgoat-%: main.c fuzzgoat.c $(VULN_SOURCES) vulneribility.h
	$(CC) $(VULN_$*) -o $@ $(CFLAGS) main.c fuzzgoat.c $(VULN_SOURCES) $(LIBS)

fuzzgoat-%-ASAN: main.c fuzzgoat.c $(VULN_SOURCES) vulneribility.h
	$(eval BUG_NAME := $(patsubst %-ASAN,%,$*))
	$(CC) $(VULN_$(BUG_NAME)) $(ASAN) -o fuzzgoat-$(BUG_NAME)_ASAN $(CFLAGS) main.c fuzzgoat.c $(VULN_SOURCES) $(LIBS)

fuzzgoat-%-UBSAN: main.c fuzzgoat.c $(VULN_SOURCES) vulneribility.h
	$(eval BUG_NAME := $(patsubst %-UBSAN,%,$*))
	$(CC) $(VULN_$(BUG_NAME)) $(UBSAN) -o fuzzgoat-$(BUG_NAME)_UBSAN $(CFLAGS) main.c fuzzgoat.c $(VULN_SOURCES) $(LIBS)

# 編譯所有漏洞版本（包含sanitizer版本）
build-all: fuzzgoat fuzzgoat_ASAN $(BUGS)
	@for bug in $(BUGS); do \
		echo "Building $$bug variants..."; \
		$(MAKE) fuzzgoat-$$bug; \
		$(MAKE) fuzzgoat-$${bug}-ASAN; \
	done

# 個別漏洞目標（同時編譯 normal 和 ASAN 版本）
use-after-free: fuzzgoat-use-after-free fuzzgoat-use-after-free-ASAN
invalid-free: fuzzgoat-invalid-free fuzzgoat-invalid-free-ASAN
null-deref: fuzzgoat-null-deref fuzzgoat-null-deref-ASAN
stack-overflow: fuzzgoat-stack-overflow fuzzgoat-stack-overflow-ASAN
heap-overflow: fuzzgoat-heap-overflow fuzzgoat-heap-overflow-ASAN
integer-overflow: fuzzgoat-integer-overflow fuzzgoat-integer-overflow-UBSAN
format-string: fuzzgoat-format-string fuzzgoat-format-string-ASAN






# ===============================================

afl: fuzzgoat
	afl-fuzz -i in -o out ./fuzzgoat @@


.PHONY: clean

clean:
	rm ./fuzzgoat ./fuzzgoat_ASAN
