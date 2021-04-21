import re


def _c(code):
    r = re.compile("\b(int|void)\b main\(.*\)")
    default = """#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {{}
  {}
{}}"""

    if r.search(code):
        return code
    else:
        return default.format(code)
