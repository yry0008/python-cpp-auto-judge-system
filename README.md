# 基于Python的自动批改C/C++作业的脚本

#### Requirements：

    System:Linux
    Compliter:GCC/G++
    Python3

如何运行

```Python
from cpp_checker import checker
c = checker(input_data, output_data, gcc_path, run_path, extra_args, check_float, ignore_space, time_limit, memory_limit)
c.autojudge("my.cpp")#自动评测一个名字为my.cpp的文件
```

| 参数名字 | 类别 |是否必须|描述|
| --- | ----------- | ------ | ----- |
| input_data | 字典 | Y | 输入的数据，见下方说明 |
| output_data | 字典 | Y | 输出的数据，见下方说明 |
| gcc_path | 字符串 | N (默认"/usr/bin/g++") | 编译器位置 |
| run_path | 字符串 | N (默认"/root/") | 程序运行位置 |
| extra_args | 列表 | N (默认["-lm"]) | 附加参数 |
| check_float | Bool | N (默认false) | Todo:是否检测浮点数 |
| ignore_space | Bool | N (默认true) | 是否忽略行末空格与换行符 |
| time_limit | Float | N (默认1.0)| 程序运行时间限制 |
| memory_limit | Float | N (默认1G)| Todo:程序运行内存限制 |

input_data格式
```python
input_data = {
    "测试case名字": {
            "stdin": "stdin数据，如无stdin要保留空串",
            "filename":"其他每个对应的文件",#可以没有附加文件
    },
    "测试case2名字": {
            "stdin": "stdin数据，如无stdin要保留空串",
            "filename":"其他每个对应的文件",#可以没有附加文件
    },
    # ……
}
```

output_data格式
```python
output_data = {
    "测试case名字": {
            "stdout": "正确的stdout数据，如无可为空",
            "filename":"其他每个对应的文件",#可以没有附加文件
    },
    "测试case2名字": {
            "stdout": "正确的stdout数据，如无可为空",
            "filename":"其他每个对应的文件",#可以没有附加文件
    },
    # ……
}
```

输出格式（编译成功）
```python
ouput = {
    'status':False, #是否通过评测
    'correct_cases': 3, #正确的cases
    'all_cases': 5, #总cases
    'error_data':[#每个有问题的cases
        {
            'status': False,
            'type': 'WA',#错误类型：有答案错误，无输出文件，超时间，超内存，运行错误
            'error_files': [#如果是WA每个错误文件
                {
                    'filename': 'stdout',
                    'text': ['9\n']
                }
            ],
            'case': '1'
        }, 
        {
            'status': False,
            'type': 'RE',
            'case': '4'
        },
    ]
}
```

输出格式（编译失败）
```python
ouput = {
    'status':False, #是否通过评测
    'type':'CE'
}
```