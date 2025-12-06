CC=afl-clang-fast        # 建議使用這個，不要再用 afl-gcc
DEPS=main.c fuzzgoat.c
CFLAGS=-g -O0 -Wall -I.
LIBS=-lm

ASAN_FLAGS=-fsanitize=address

all: fuzzgoat fuzzgoat_ASAN

fuzzgoat: $(DEPS)
	$(CC) -o $@ $(CFLAGS) $^ $(LIBS)

fuzzgoat_ASAN: $(DEPS)
	clang -o $@ $(ASAN_FLAGS) $(CFLAGS) $^ $(LIBS)

run:
	afl-fuzz -i in -o out -- ./fuzzgoat @@

clean:
	rm -f fuzzgoat fuzzgoat_ASAN

