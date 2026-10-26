# 运行时注入 / hook(嵌入式解释器 & 冻结/编译程序,通用)

> **何时读**:目标是**嵌入式解释器打包的富客户端**(Python/Lua/JS/.NET/JVM 打进 exe),或**冻结/编译**的程序(PyInstaller/cx_Freeze/Nuitka/py2exe/自定义),你要在运行时改其行为(no-op 退出、翻转校验、补挂载 UI、读运行期数据)。native API hook 见 `frida-win`;本文补它没有的**解释层/编译层**手法。

## 1. 先判打包/编译方式(决定能不能改字节码)

同是"打包 Python",手段天差地别:
- **纯打包(PyInstaller/cx_Freeze/py2exe/自定义冻结)**:模块是**真字节码**(可能去了 pyc 头/自定义 marshal)。→ 可反编译、可改字节码、可 monkeypatch。
- **编译(Nuitka / Cython / .NET AOT)**:函数编译成**原生代码**,Python 层只剩占位 stub。识别:`func.__code__` 反汇编出 `RuntimeError('Compiled function bytecode used')`,或 `type(m.foo).__name__ == 'compiled_function'`。→ **改不了字节码**,但**仍是模块/类属性,可在 Python 层整体替换**(`Cls.method = my_func`)。
- **判定动作**:注入后先 introspect 一个目标函数的 `__code__`/`type()`,别假设。marshal.loads 解不开 + dis 是占位 = 编译型,别在反编译上耗轮次。

## 2. 进程内执行解释器代码(嵌入式解释器通用钥匙)

目标进程已加载解释器运行时(如 `pythonXX.dll`),你可在进程内直接驱动它执行代码,无需源码:
- **拿函数**:`GetModuleHandle(解释器dll)` + `GetProcAddress`。Python 例:`PyGILState_Ensure`/`PyGILState_Release`/`PyRun_SimpleString`/`Py_IsInitialized`。
- **GIL 是关键**:执行解释器代码前**必须持 GIL**。
  - 从**注入线程/Frida 线程**:`PyGILState_Ensure()` → `PyRun_SimpleString(code)` → `PyGILState_Release(st)`。目标主线程空闲在事件循环时 GIL 已释放,Ensure 能拿到。
  - ⚠️ 已知坑:`PyGILState_Ensure` 从"解释器不认识的线程"调**可能死锁**(CPython issue)。规避:要么在**解释器自身回调/hook 里**执行(那时目标线程正持 GIL),要么确保目标此刻 GIL 空闲。两种都试过可行。
- **注入代码必须纯 ASCII**:`PyRun_SimpleString` 按 UTF-8 解析源码;嵌中文路径的 GBK 字节 → 整段 `SyntaxError`,什么都不执行。日志/路径写无中文目录,或用 `\uXXXX` 转义。
- **等就绪**:后台注入线程要轮询 `Py_IsInitialized()` 为真 + 稍等,别在解释器没起来时就执行。

## 3. hook 点分层选择(别只会 native)

按"离决策点近 + 好改"选层,不要反射式只 hook native API:
- **解释层(常最有效)**:no-op 退出函数、整体替换方法、monkeypatch 校验函数返回、`sys.settrace`/`sys.excepthook` 观测。
- **运行时 C-API**:hook 解释器执行循环(如 `_PyEval_EvalFrameDefault`)在首次命中时注入并卸载——适合"想在目标线程持 GIL 时执行一段代码"。注意:目标空闲(事件循环在 C++ 层)时此函数**不被命中**,那就改用 §2 的 GIL-Ensure 直调。
- **native API**:文件/注册表/网络/crypto/退出 syscall——见 `frida-win`。
- 编译型函数(Nuitka)hook = §1 的**整体属性替换**,不是改字节码。

## 4. 观测运行期真实数据(别静态猜)

- **未捕获异常 → excepthook 抓局部变量**:注入 `sys.excepthook`(和 `threading.excepthook`)遍历 traceback 各帧,打印 `f_locals`——直接看是哪个变量/list 空了、值是什么。比静态猜"格式"强得多。
- **settrace 记录调用流**:注入 `sys.settrace`/`threading.settrace` 过滤记录目标模块的 `CALL`——看真实执行路径走到哪、哪个函数没被调。注意 `sys.settrace` 只对**当前线程**生效;要覆盖主线程需在主线程上下文设置(或用 excepthook 兜)。
- **introspect 活实例**:`gc.get_objects()` 找目标类实例,`dir()`/`getattr` 拿真实属性/方法——补挂载/替换前的必备步骤(拿真名,别猜)。

## 5. 跨线程操作 GUI(补挂载必踩)

从注入线程直接操作 GUI 控件会崩或无效——GUI 必须在**创建它的 UI 主线程**执行:
- **Qt/PySide**:`QTimer.singleShot(0, fn)` **在注入线程创建不触发**(timer 绑到无事件循环的注入线程)。正解:定义带 `Signal` 的 `QObject`,`moveToThread(app.thread())`,`sig.connect(slot, QueuedConnection)`,从注入线程 `emit` → slot 在主线程事件循环执行。
- 其他框架同理:用其"post 到 UI 线程"机制(WinForms `Control.Invoke`/`BeginInvoke`、WPF `Dispatcher.Invoke`、GTK `idle_add`)。
- 前提:UI 主线程有在跑的事件循环(窗口能响应即在跑)。

## 6. 保活:hook 会话不能中途 detach

非交互驱动 hook(`frida -q`/`&` 后台)会在 stdin EOF 时**立即 detach,hook 在用户操作前就死**——被误判成"这栈 hook 不了"。正解:**Python harness + 主线程阻塞循环**常驻,心跳区分"会话死"vs"活着没命中"。spawn 能在 init 前 hook(抓早期一次性调用);attach 用于已运行进程。细节见 `frida-win` §11。

## 收尾

每确认一个注入点/hook 结果,按 Rule 7 立即写回;无效手段 `[X]`+证据留痕。
