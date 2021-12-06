import re


def _processing(lang, code):
    defaults = {
        "cpp": """#include <iostream>
#include <cstdlib>
#include <cmath>
#include <cstring>
using namespace std;

int main() {{
    {}
}}""",
        "c": """#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main() {{
  {}
}}""",
        "go": """package main
        
import (
  "fmt"
  "math"
  "strings"
)

var _, _ = fmt.Printf("")
var _ = math.Abs(1)
var _ = strings.ToLower("")

func main() {{
    {}
}}""",
        "rs": """fn main() {{
    {}
}}"""
    }

    regexes = {
        "cpp": "(?:int|void) main\(.*\)",
        "c": "(?:int|void) main\(.*\)",
        "go": "func main\(.*\)",
        "rs": "fn main\(.*\)"
    }

    try:
        default = defaults[lang]
        regex = regexes[lang]
    except KeyError:
        return code

    r = re.compile(regex)

    if r.search(code, re.IGNORECASE):
        return code
    else:
        return default.format(code)
