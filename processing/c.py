import re


def _c(code):
    r = re.compile("(?:int|void) main\(.*\)")
    default = """#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main() {{
  {}
}}"""

    if r.search(code, re.IGNORECASE):
        return code
    else:
        return default.format(code)
