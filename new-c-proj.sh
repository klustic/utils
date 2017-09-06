#!/bin/bash
TARGET=$1
PATHNAME=${2:-$(pwd -P)}

if [[ -z TARGET ]]; then echo "Usage: $0 <target> [basepath]"; exit 1; fi

mkdir "${PATHNAME}"/{inc,src,obj}
cat <<EOF >"${PATHNAME}/src/main.c"
#include <stdio.h>
int main(int argc, char *argv[])
{
  puts("Hello World");
  return 0;
}
EOF
cat <<"EOF" | sed "s/__TARGET__/$1/" >"${PATHNAME}/Makefile"
INC = inc
OBJ = obj
SRC = src
TARGET = "__TARGET__"
OBJECTS =
INCLUDES = -I $(INC)
LDFLAGS = 
CFLAGS = -Wall

.PHONY: clean tidy

$(TARGET): $(OBJECTS) $(SRC)/main.c
	$(CC) $(CFLAGS) $(INCLUDES) -o $@ $^ $(LDFLAGS)

$(OBJ)/%.o: $(SRC)/%.c
	$(CC) -c $(CFLAGS) $(INCLUDES) -o $@ $^ $(LDFLAGS)

tidy:
	rm -f $(OBJ)/*.o
clean: tidy
	rm -f $(TARGET)
EOF
