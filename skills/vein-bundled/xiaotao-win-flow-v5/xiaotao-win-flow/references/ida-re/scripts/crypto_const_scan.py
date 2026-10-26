"""
crypto_const_scan.py — Findcrypt-style scan for known cryptographic constants.

The fastest way to recognize cryptography without reading it: search the binary for the fixed
tables and magic values that crypto algorithms embed (S-boxes, init states, round-constant
tables, fixed alphabets), and report which functions reference them. Read-only: it locates and
reports, it does not edit the database.

WHAT IT FINDS
  AES S-box / inverse S-box, MD5/SHA-1/SHA-256/SHA-512 init states and round tables,
  Blowfish P-array (pi digits), CRC32 (IEEE) table, Base64 alphabets (standard + URL-safe),
  ChaCha/Salsa20 "expand .. -byte k" constants.

WHAT IT CANNOT FIND
  Algorithms with no static constants — notably RC4 (its S-box is built at runtime as an
  identity permutation, then swapped). Catch those behaviorally: a 256-iteration init loop
  followed by a swap loop.

HOW TO RUN
  In IDA:    File > Script file... > crypto_const_scan.py
  Via MCP:   paste into py_eval(code=...); it prints hits. Or call scan().
"""

try:
    import idautils
    import idc
    import ida_segment
    import ida_bytes
    import ida_funcs
except ImportError:
    raise SystemExit("This script must be run inside IDA Pro (IDAPython).")

# Distinctive byte signatures (little-endian where the source is a word/dword/qword table).
# Each entry: (name, signature_bytes). Kept short but unique to avoid false positives.
SIGNATURES = [
    ("AES S-box",
     bytes.fromhex("637c777bf26b6fc53001672bfed7ab76")),
    ("AES inverse S-box",
     bytes.fromhex("52096ad53036a538bf40a39e81f3d7fb")),
    ("MD5/SHA-1 init state (A,B,C,D)",
     bytes.fromhex("0123456789abcdeffedcba9876543210")),
    ("MD5 T-table (sine constants)",
     bytes.fromhex("78a46ad756b7c7e8")),
    ("SHA-256 init state",
     bytes.fromhex("67e6096a85ae67bb")),
    ("SHA-256 K-table",
     bytes.fromhex("982f8a4291443771")),
    ("SHA-512 init state",
     bytes.fromhex("08c9bcf367e6096a")),
    ("Blowfish P-array (pi)",
     bytes.fromhex("886a3f24d308a385")),
    ("CRC32 (IEEE) table",
     bytes.fromhex("963007772c610eee")),
    ("Base64 alphabet (standard)",
     b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"),
    ("Base64 alphabet (URL-safe)",
     b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"),
    ("ChaCha/Salsa20 sigma (32-byte)", b"expand 32-byte k"),
    ("ChaCha/Salsa20 tau (16-byte)", b"expand 16-byte k"),
]


def _iter_seg_bytes():
    for seg_ea in idautils.Segments():
        seg = ida_segment.getseg(seg_ea)
        if not seg:
            continue
        data = ida_bytes.get_bytes(seg.start_ea, seg.end_ea - seg.start_ea)
        if data:
            yield seg.start_ea, data


def _func_label(ea):
    f = ida_funcs.get_func(ea)
    if f:
        return "%s (0x%X)" % (idc.get_func_name(f.start_ea), f.start_ea)
    nm = idc.get_name(ea)
    return nm if nm else "(no function)"


def scan():
    hits = []  # (name, ea)
    for base, data in _iter_seg_bytes():
        for name, sig in SIGNATURES:
            if not sig:
                continue
            start = 0
            while True:
                i = data.find(sig, start)
                if i == -1:
                    break
                hits.append((name, base + i))
                start = i + 1

    print("=" * 60)
    print("CRYPTO CONSTANT SCAN")
    print("=" * 60)
    if not hits:
        print("No known crypto constants found.")
        print("Note: RC4 and other table-less ciphers won't show up here — look for a")
        print("256-byte identity-init loop plus a swap loop instead.")
        print("=" * 60)
        return []

    for name, ea in hits:
        print("  [%-32s] 0x%X  in %s" % (name, ea, _func_label(ea)))
    print("-" * 60)
    print("Next: name the referencing functions (e.g. aes_decrypt, sha256_init) and comment")
    print("the constant. Confirm mode/key/IV by reading the surrounding code.")
    print("=" * 60)
    return hits


if __name__ == "__main__":
    scan()
