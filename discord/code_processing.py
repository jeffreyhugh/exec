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
}}""",
        "java": """import java.io.*;
import java.util.*;
import java.util.concurrent.*;

public class Main {{
        public static void main(String[] args) {{
            {}
        }}
}}"""
    }

    regexes = {
        "cpp": "(?:int|void) main(?:\s*)\(.*\)",
        "c": "(?:int|void) main(?:\s*)\(.*\)",
        "go": "func main(?:\s*)\(.*\)",
        "rs": "fn main(?:\s*)\(.*\)",
        "java": "public static void main(?:\s*)\(.*\)"
    }

    try:
        default = defaults[lang]
        regex = regexes[lang]
    except KeyError:
        return code

    r = re.compile(regex, re.IGNORECASE)

    if r.search(code):
        # if we're using java...
        if (lang == "java"):
            # change the class name to Main
            code = re.sub("(?<=(public class ))(([A-Z]|[a-z])*)", "Main", code, count=1)
            # and remove any package declaration
            code = re.sub("package (.*)", "", code, count=1)
        
        return code
    else:
        return default.format(code)
