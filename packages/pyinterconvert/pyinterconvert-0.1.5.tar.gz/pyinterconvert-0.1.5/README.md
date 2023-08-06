# PyInterconvert
> A simple tool for interconversion of binary, decimal, hexadecimal and octal

## Current functions
- BinToDec
- BinToOct
- BinToHex
- DecToBin
- DecToOct
- DecTohex
- HexToBin
- OctToBin

For other Hexadecimal and Octal conversions the given functions can be used together as follows:-

```python
BinToDec(HexToBin(arg)) #Hexadecimal to Decimal
BinToOct(HexToBin(arg)) #Hexadecimal to Octal
BinToDec(OctToBin(arg)) #Octal to Decimal
BinToHex(OctToBin(arg)) #Octal to Hexadecimal
```
**Arg is of type string**

## Sample Usage
```python
from pyinterconvert import ConvClient

c = ConvClient()

print(c.BinToOct(1010101))
#prints 125
```

