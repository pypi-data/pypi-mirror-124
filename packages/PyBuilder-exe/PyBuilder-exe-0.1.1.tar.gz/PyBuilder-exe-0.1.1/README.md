# 背景
最近东家要求源码保密，要求连除项目经理外的其他成员也只能看到自己负责的那部分源码，于是乎就只能将源码编译或制成库后引入项目，最后还要求项目打包制成可执行程序。为了方便使用，本人将其制成了包，[源码地址](https://github.com/leocll/PyBuilder)。

# [PyBuilder-exe](https://github.com/leocll/PyBuilder)
简化`python`程序的打包，支持`.py`译成`.so`，保护源码

### 依赖
- `Cython`: `python`源码编译
- `PyInstaller`: `python`程序打包

### Hooks
```
# build data将开始解析时
def hook_data(data: BuildData): ...
# 已解析出项目中excludes项时
def hook_excludes(target: typing.List[str], data: BuildData) -> typing.List[str]: ...
# 已解析出项目中ignores项时
def hook_ignores(target: typing.List[str], data: BuildData) -> typing.List[str]: ...
# 已解析出项目中的包路径项时
def hook_build_lib_path(target: typing.List[str], data: BuildData) -> typing.List[str]: ...
# 已解析出项目中的资源文件时
def hook_build_data(target: typing.List[typing.Tuple[str, str]],
                    data: BuildData) -> typing.List[typing.Tuple[str, str]]: ...
# 已解析出项目中的隐藏导入项时
def hook_build_imports(target: typing.List[str], data: BuildData) -> typing.List[str]: ...
# 将开始编译时
def hook_pre_compile(data: BuildData): ...
# 已编译完成时
def hook_compiled(data: BuildData): ...
# 将开始build时
def hook_pre_build(data: BuildData): ...
# 已build完成时
def hook_built(data: BuildData): ...
```

### 使用
具体使用可参照[example](https://github.com/leocll/PyBuilder/tree/master/tests)
- 安装
```
pip install PyBuilder-exe
```
- 在`python`脚本中调用
```
from PyBuilder import run

# run函数定义
def run(name, target_file='', src_dir='', build_dir='', hook_file='', excludes_file='',
        ignores_file='', single=_default_config.single, no_compile=_default_config.no_compile):
    """
    打包
    :param name: 打包后的程序名
    :param target_file: 入口文件相对于`src_dir`的相对路径
    :param src_dir: 源文件根目录路径，默认为运行环境的根目录路径
    :param build_dir: build目录路径，默认为与运行环境的根目录同级的`builder`目录
    :param hook_file: hook文件路径
    :param excludes_file: `excludes`文件路径
    :param ignores_file: `ignore`文件路径
    :param single: 是否build为单文件程序，默认为False
    :param no_compile: 是否不编译.py文件，默认为False
    :return:
    """
    ...
```
- 命令行调用
```
PyBuilder -h
```
```
[PyBuilder-exe]Python build tools

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  the execution name.
  -tf TARGET_FILE, --target-file TARGET_FILE
                        the target file path relative the sources
                        dir.(default: main.py)
  -sd SRC_DIR, --src-dir SRC_DIR
                        the sources dir path.
  -bd BUILD_DIR, --build-dir BUILD_DIR
                        the build dir path.
  -hf HOOK_FILE, --hook-file HOOK_FILE
                        the .py file of hook build.
  -ef EXCLUDES_FILE, --excludes-file EXCLUDES_FILE
                        the excludes file path.
  -if IGNORES_FILE, --ignores-file IGNORES_FILE
                        the ignores file path.
  -F                    build a single file execution.(default: False)
  -nc, --no-compile     not compile, only build.(default: False)
```

### 注意
- [源码运行时和打包程序运行时的注意项](https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#run-time-information)
- `__file__`的使用，可参照[example](https://github.com/leocll/PyBuilder/tree/master/tests/example2-1)，也根据`PyInstaller`官方文档[关于`__file__`的注意事项](https://pyinstaller.readthedocs.io/en/stable/runtime-information.html#using-file)

### 参考
- [`python`源码加密](https://www.fythonfang.com/blog/2018/11/3/encrypt-protect-python-code)
- [`python`项目打包程序分析](https://docs.python-guide.org/shipping/freezing/)
- [PyInstaller官方文档](https://pyinstaller.readthedocs.io/en/stable/)