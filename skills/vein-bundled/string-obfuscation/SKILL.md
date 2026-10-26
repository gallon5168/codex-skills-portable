---
name: "string-obfuscation"
description: "String obfuscation techniques including XOR, AES, RC4 encryption, base64 encoding, and function hashing to evade static analysis"
version: "1.0.0"
---

# String Obfuscation

> 字符串混淆是一种基本的静态反分析技术，涉及加密、编码或构建敏感字符串（如API函数名、C2 URL、路径）以避免静态分析工具、YARA规则和启发式扫描程序的检测。

## 概述

许多安全工具分析二进制文件中的字符串以识别恶意行为：
- **API函数名**：CreateRemoteThread、VirtualAlloc、GetProcAddress
- **C2 URLs**：http://malicious-c2.com/beacon
- **文件路径**：C:\\Windows\\System32\\cmd.exe
- **命令**：whoami、net user、powershell

## XOR加密

### 基本XOR

XOR是最简单和最常见的混淆方法。它是可逆的（使用相同密钥XOR两次返回原始数据）。

### 加密过程

```cpp
// 使用XOR加密字符串
void XorEncrypt(char* str, char key) {
    for (size_t i = 0; str[i] != '\0'; i++) {
        str[i] ^= key;
    }
}

// 使用
char apiName[] = "CreateRemoteThread";
XorEncrypt(apiName, 0xAA);
// 结果：加密字符串

// 解密
XorEncrypt(apiName, 0xAA);
// 结果：回到"CreateRemoteThread"
```

### 原地解密

```cpp
#include <windows.h>

const char* GetResolvedString() {
    // 加密字符串（静态分析将看到此）
    static char encrypted[] = {0x73^0xAA, 0x65^0xAA, 0x63^0xAA, 
                               0x72^0xAA, 0x65^0xAA, 0x74^0xAA};
    char key = 0xAA;

    // 原地解密（仅运行时）
    for (int i = 0; i < 6; i++) {
        encrypted[i] ^= key;
    }

    return (const char*)encrypted; // 返回"secret"
}
```

### 密钥调度

简单XOR通常被检测。使用密钥调度（一系列密钥）来混淆分析。

```cpp
void XorEncryptWithSchedule(char* str, size_t len, 
                          const char* keySchedule, size_t keyLen) {
    for (size_t i = 0; i < len; i++) {
        str[i] ^= keySchedule[i % keyLen];
    }
}

// 示例密钥调度
char schedule[] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF};

// 加密
XorEncryptWithSchedule(apiName, strlen(apiName), 
                       schedule, sizeof(schedule));
```

## AES加密

AES（高级加密标准）提供更强的加密，但需要更多设置。

### C++示例

```cpp
#include <windows.h>
#include <wincrypt.h>

void AesEncryptString(const char* plaintext, BYTE** outCipher, DWORD* outLen) {
    HCRYPTPROV hProv = 0;
    HCRYPTKEY hKey = 0;

    // 获取加密上下文
    CryptAcquireContext(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT);

    // 生成随机AES密钥
    CryptGenKey(hProv, CALG_AES_256, 0, &hKey);

    // 获取密钥大小和缓冲区
    DWORD blockSize, keySize;
    CryptGetKeyParam(hKey, KP_BLOCKLEN, (BYTE*)&blockSize, &keySize, 0);

    // 加密
    DWORD dataLen = strlen(plaintext);
    *outLen = dataLen + blockSize;
    *outCipher = (BYTE*)malloc(*outLen);
    memcpy(*outCipher, plaintext, dataLen);

    CryptEncrypt(hKey, 0, TRUE, 0, *outCipher, outLen);

    // 清理
    CryptDestroyKey(hKey);
    CryptReleaseContext(hProv, 0);
}
```

## RC4加密

RC4是一种流密码，因其简单性和速度而被广泛使用。

### C实现

```c
#include <stdint.h>

// RC4密钥调度算法（KSA）
void rc4_ksa(uint8_t* s, const uint8_t* key, size_t keyLen) {
    for (int i = 0; i < 256; i++) {
        s[i] = i;
    }

    uint8_t j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j + s[i] + key[i % keyLen]) & 0xFF;
        uint8_t temp = s[i];
        s[i] = s[j];
        s[j] = temp;
    }
}

// RC4伪随机生成算法（PRGA）
void rc4_prga(uint8_t* s, uint8_t* data, size_t dataLen) {
    uint8_t i = 0, j = 0;
    for (size_t k = 0; k < dataLen; k++) {
        i = (i + 1) & 0xFF;
        j = (j + s[i]) & 0xFF;
        uint8_t temp = s[i];
        s[i] = s[j];
        s[j] = temp;
        data[k] ^= s[(s[i] + s[j]) & 0xFF];
    }
}

// 加密/解密（RC4的相同操作）
void rc4_crypt(const uint8_t* key, size_t keyLen, 
              uint8_t* data, size_t dataLen) {
    uint8_t s[256];
    rc4_ksa(s, key, keyLen);
    rc4_prga(s, data, dataLen);
}
```

## Base64编码

Base64编码不是加密，但常用于混淆字符串。

### C++示例

```cpp
#include <windows.h>
#include <wincrypt.h>

std::string Base64Encode(const std::string& input) {
    DWORD outLen = 0;
    CryptBinaryToStringA(
        (const BYTE*)input.c_str(),
        input.size(),
        CRYPT_STRING_BASE64 | CRYPT_STRING_NOCRLF,
        NULL,
        &outLen
    );

    std::string output(outLen, '\0');
    CryptBinaryToStringA(
        (const BYTE*)input.c_str(),
        input.size(),
        CRYPT_STRING_BASE64 | CRYPT_STRING_NOCRLF,
        &output[0],
        &outLen
    );

    return output;
}

std::string Base64Decode(const std::string& input) {
    DWORD outLen = 0;
    CryptStringToBinaryA(
        input.c_str(), 0, CRYPT_STRING_BASE64,
        NULL, &outLen, NULL, NULL
    );

    std::string output(outLen, '\0');
    CryptStringToBinaryA(
        input.c_str(), 0, CRYPT_STRING_BASE64,
        (BYTE*)&output[0], &outLen, NULL, NULL
    );

    return output;
}
```

## 动态字符串构建

不将完整字符串放在二进制文件中，而是在运行时构建。

### 简单构建

```cpp
void ConstructString() {
    char part1[] = {'C', 'r', 'e', 'a', 't', 'e'};
    char part2[] = {'R', 'e', 'm', 'o', 't', 'e'};
    char part3[] = {'T', 'h', 'r', 'e', 'a', 'd'};

    char result[100];
    sprintf(result, "%s%s%s", part1, part2, part3);
    // result = "CreateRemoteThread"

    HMODULE hKernel32 = GetModuleHandleA("kernel32.dll");
    GetProcAddress(hKernel32, result);
}
```

### 混淆构建

```cpp
void ObfuscatedConstruction() {
    // 将ASCII码转换为字符
    char api[19];
    int codes[] = {67, 114, 101, 97, 116, 101, 82, 101, 109, 111, 
                   116, 101, 84, 104, 114, 101, 97, 100, 0};

    for (int i = 0; i < 18; i++) {
        api[i] = (char)codes[i];
    }

    // api = "CreateRemoteThread"
}
```

## 函数哈希

不以明文存储函数名，而是哈希函数名并动态解析。

### 简单哈希函数

```cpp
// DJB2哈希
DWORD HashFunctionName(const char* funcName) {
    DWORD hash = 5381;
    int c;
    while ((c = *funcName++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return hash;
}

// 使用
FARPROC GetProcAddressViaHash(HMODULE hModule, DWORD hash) {
    // 需要解析PE的导出表
    // 遍历导出函数，为每个函数计算哈希
    // 返回匹配哈希的函数

    PIMAGE_DOS_HEADER pDos = (PIMAGE_DOS_HEADER)hModule;
    PIMAGE_NT_HEADERS pNt = (PIMAGE_NT_HEADERS)((DWORD_PTR)hModule + pDos->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY pExport = (PIMAGE_EXPORT_DIRECTORY)
        ((DWORD_PTR)hModule + pNt->OptionalHeader.DataDirectory
        [IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);

    DWORD* pFunctions = (DWORD*)((DWORD_PTR)hModule + pExport->AddressOfFunctions);
    DWORD* pNames = (DWORD*)((DWORD_PTR)hModule + pExport->AddressOfNames);
    WORD* pOrdinals = (WORD*)((DWORD_PTR)hModule + pExport->AddressOfNameOrdinals);

    for (DWORD i = 0; i < pExport->NumberOfNames; i++) {
        char* name = (char*)((DWORD_PTR)hModule + pNames[i]);
        if (HashFunctionName(name) == hash) {
            return (FARPROC)((DWORD_PTR)hModule + pFunctions[pOrdinals[i]]);
        }
    }

    return NULL;
}
```

### 示例

```cpp
// CreateRemoteThread的预计算哈希
#define HASH_CreateRemoteThread 0x12345678 // 示例值

void UseHashedAPI() {
    HMODULE hKernel32 = GetModuleHandleA("kernel32.dll");
    FARPROC pFunc = GetProcAddressViaHash(hKernel32, HASH_CreateRemoteThread);
    // ...
}
```

## 检测与对抗

### 检测方法

1. **熵分析**：字符串的熵值高于正常文本（XOR、加密）
2. **基于签名**：匹配已知混淆模式的字符串（如常见密钥如0xAA）
3. **仿真**：运行解密并检查结果
4. **API跟踪**：监控解密函数调用
5. **内存扫描**：在运行时扫描解密的字符串

### 对抗策略

- 使用自定义加密算法（不仅仅是简单XOR）
- 混合多种技术（XOR + AES + Base64）
- 每个payload使用唯一密钥
- 在不同时间加密（不是全部在启动时）
- 混淆加密代码本身

### 最佳实践

```cpp
// 组合混淆策略
void AdvancedObfuscation() {
    // 1. AES加密字符串
    BYTE* cipher;
    DWORD cipherLen;
    AesEncryptString("CreateRemoteThread", &cipher, &cipherLen);

    // 2. XOR结果
    for (DWORD i = 0; i < cipherLen; i++) {
        cipher[i] ^= 0x55;
    }

    // 3. Base64编码整个密文
    std::string result = Base64Encode(std::string((char*)cipher, cipherLen));

    // 4. 将结果存储为二进制中的字符串
    const char* stored = result.c_str();

    // 运行时（逆过程）
    std::string decoded = Base64Decode(stored);
    for (size_t i = 0; i < decoded.size(); i++) {
        ((char*)decoded.c_str())[i] ^= 0x55;
    }

    // 现在使用AES密钥解密（未显示）
    // ...
}
```

## 参考资源

- [PayloadsAllTheThings - String Obfuscation](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Obfuscation/README.md)
- [Veil Framework](https://github.com/Veil-Framework/Veil) - AV免杀框架
- [Crypto++ Library](https://www.cryptopp.com/) - C++加密库
- [OpenSSL](https://www.openssl.org/) - 加密工具包
