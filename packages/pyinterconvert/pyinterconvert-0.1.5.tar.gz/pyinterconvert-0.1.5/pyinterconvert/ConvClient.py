def _createMap(bin_oct_map):
    bin_oct_map["000"] = '0'
    bin_oct_map["001"] = '1'
    bin_oct_map["010"] = '2'
    bin_oct_map["011"] = '3'
    bin_oct_map["100"] = '4'
    bin_oct_map["101"] = '5'
    bin_oct_map["110"] = '6'
    bin_oct_map["111"] = '7'

def _createMap2(bin_hex_map):
    bin_hex_map["0000"] = '0'
    bin_hex_map["0001"] = '1'
    bin_hex_map["0010"] = '2'
    bin_hex_map["0011"] = '3'
    bin_hex_map["0100"] = '4'
    bin_hex_map["0101"] = '5'
    bin_hex_map["0110"] = '6'
    bin_hex_map["0111"] = '7'
    bin_hex_map["1000"] = '8'
    bin_hex_map["1001"] = '9'
    bin_hex_map["1010"] = 'A'
    bin_hex_map["1011"] = 'B'
    bin_hex_map["1100"] = 'C'
    bin_hex_map["1101"] = 'D'
    bin_hex_map["1110"] = 'E'
    bin_hex_map["1111"] = 'F'

def _createMap3(bin_hex_map):
    bin_hex_map["0"] = '0000'
    bin_hex_map["1"] = '0001'
    bin_hex_map["2"] = '0010'
    bin_hex_map["3"] = '0011'
    bin_hex_map["4"] = '0100'
    bin_hex_map["5"] = '0101'
    bin_hex_map["6"] = '0110'
    bin_hex_map["7"] = '0111'
    bin_hex_map["8"] = '1000'
    bin_hex_map["9"] = '1001'
    bin_hex_map["A"] = '1010'
    bin_hex_map["B"] = '1011'
    bin_hex_map["C"] = '1100'
    bin_hex_map["D"] = '1101'
    bin_hex_map["E"] = '1110'
    bin_hex_map["F"] = '1111'

def _createMap4(bin_oct_map):
    bin_oct_map["0"] = '000'
    bin_oct_map["1"] = '001'
    bin_oct_map["2"] = '010'
    bin_oct_map["3"] = '011'
    bin_oct_map["4"] = '100'
    bin_oct_map["5"] = '101'
    bin_oct_map["6"] = '110'
    bin_oct_map["7"] = '111'
    
class ConvClient:
    def __init__(self):
        self._createMap = _createMap
        self._createMap2 = _createMap2
        self._createMap3 = _createMap3
        self._createMap4 = _createMap4
        
    #Binary Conversions
    def BinToDec(self,num):
        s = 0
        a = len(str(num)) - 1
        for i in str(num):
          add = 2**a * int(i)
          s += add
          a -= 1
        return str(s)

    def BinToOct(self,num):
        nu = str(num)
        l = len(nu)

        len_left = l

        for i in range(1, (3 - len_left % 3) % 3 + 1):
              nu = '0' + nu

        bin_oct_map = {}
        self._createMap(bin_oct_map)
        i = 0
        octal = ""

        while (True) :
          octal += bin_oct_map[nu[i:i + 3]]
          i += 3
          if (i == len(nu)):
            break
        return str(octal)

    def BinToHex(self,num):
        nu = str(num)
        l = len(nu)

        len_left = l

        for i in range(1, (4 - len_left % 4) % 4 + 1):
              nu = '0' + nu

        bin_hex_map = {}
        self._createMap2(bin_hex_map)
        i = 0
        hex = ""

        while (True) :
          hex += bin_hex_map[nu[i:i + 4]]
          i += 4
          if (i == len(nu)):
            break
        return str(hex)

    #Decimal Conversions
    def DecToBin(self,num):
        dec = int(num)
        binn = ""
        while dec>1:
          x = dec%2
          binn += str(x)
          dec //=2
        binn += str(dec)
        return "".join(reversed(binn))

    def DecToHex(self,num):
        n = int(num)
        x = (n % 16)
        ch = ""
        if (x < 10):
            ch = x
        if (x == 10):
            ch = "A"
        if (x == 11):
            ch = "B"
        if (x == 12):
            ch = "ch"
        if (x == 13):
            ch = "D"
        if (x == 14):
            ch = "E"
        if (x == 15):
            ch = "F"
        if (n - x != 0):
            return self.DecToHex(n // 16) + str(ch)
        else:
            return str(ch)

    def DecToOct(self,num):
        octalnum = ""
        i = 0
        n = int(num)
        while n!=0:
          octalnum += str(n % 8)
          n = int(n / 8)
          i += 1
        return ''.join(reversed(octalnum))

    #Hexadecimal conversions
    def HexToBin(self,num):
        nu = str(num)
        bin_hex_map = {}
        self._createMap3(bin_hex_map)
        bina = ""
        for i in nu:
          bina += bin_hex_map[i]
        return bina

    #Octal conversions
    def OctToBin(self,num):
        nu = str(num)
        bin_oct_map = {}
        self._createMap4(bin_oct_map)
        deca = ""
        for i in nu:
          deca += bin_oct_map[i]
        return deca
