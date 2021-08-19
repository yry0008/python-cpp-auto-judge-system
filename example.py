from cpp_checker import checker
c = checker({
    "1": {
            "stdin": "3 5"
    },
    "2": {
        "stdin": "5 13"
    },
    "3": {
        "stdin": "123 176"
    },
    "4": {
        "stdin": "1276 5"
    },
    "5": {
        "stdin": "1114514 1919810"
    }
},
    {
        "1": {
            "stdout": "8"
        },
        "2": {
            "stdout": "18"
        },
        "3": {
            "stdout": "299"
        },
        "4": {
            "stdout": "1281"
        },
        "5": {
            "stdout": "3034324"
        }
}, run_path="/root/",ignore_space=False)
output = c.autojudge("/root/myres/cpp-test/test.cpp")
print(str(output))
