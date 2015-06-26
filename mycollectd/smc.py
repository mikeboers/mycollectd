import os
import re
import sys
from subprocess import Popen, PIPE
from plistlib import readPlistFromString as plist_loads


# see: http://www.parhelia.ch/blog/statics/k3_keys.html
# see: https://stackoverflow.com/questions/28568775/description-for-apples-smc-keys
KEY_TO_NAME = dict(line.strip().split(None, 1) for line in '''


F0Ac    Fan0 RPM
F0Mn    Fan0 Min RPM
F0Mx    Fan0 Max RPM
F1Ac    Fan1 RPM
F1Mn    Fan1 Min RPM
F1Mx    Fan1 Max RPM

ALT0    Ambient Light 0
ALT1    Ambient Light 1

TCXC    PECI CPU
TCXc    PECI CPU
TC0P    CPU 1 Proximity
TC0H    CPU 1 Heatsink
TC0D    CPU 1 Die
TC0E    CPU 1
TC0F    CPU 1
TC1C    CPU Core 1
TC2C    CPU Core 2
TC3C    CPU Core 3
TC4C    CPU Core 4
TC5C    CPU Core 5
TC6C    CPU Core 6
TC7C    CPU Core 7
TC8C    CPU Core 8
TCAH    CPU 1 Heatsink Alt.
TCAD    CPU 1 Die Alt.
TC1P    CPU 2 Proximity
TC1H    CPU 2 Heatsink
TC1D    CPU 2 Die
TC1E    CPU 2
TC1F    CPU 2
TCBH    CPU 2 Heatsink Alt.
TCBD    CPU 2 Die Alt.

TCSC    PECI SA
TCSc    PECI SA
TCSA    PECI SA

TCGC    PECI GPU
TCGc    PECI GPU
TG0P    GPU 1 Proximity
TG1P    GPU 2 Proximity
TG0D    GPU 1 Die
TG1D    GPU 2 Die
TG0H    GPU 1 Heatsink
TG1H    GPU 2 Heatsink

Ts0S    Memory Proximity
TM0P    Mem Bank A1
TM1P    Mem Bank A2
TM8P    Mem Bank B1
TM9P    Mem Bank B2
TM0S    Mem Module A1
TM1S    Mem Module A2
TM8S    Mem Module B1
TM9S    Mem Module B2

TN0D    Northbridge Die
TN0P    Northbridge Proximity 1
TN1P    Northbridge Proximity 2
TN0C    MCH Die
TN0H    MCH Heatsink
TP0D    PCH Die
TPCD    PCH Die
TP0P    PCH Proximity

TA0P    Airflow 1
TA1P    Airflow 2
Th0H    Heatpipe 1
Th1H    Heatpipe 2
Th2H    Heatpipe 3

Tm0P    Mainboard Proximity
Tp0P    Powerboard Proximity
Ts0P    Palm Rest
Tb0P    BLC Proximity

TL0P    LCD Proximity
TW0P    Airport Proximity
TH0P    HDD Bay 1
TH1P    HDD Bay 2
TH2P    HDD Bay 3
TH3P    HDD Bay 4
TO0P    Optical Drive

TB0T    Battery TS_MAX
TB1T    Battery 1
TB2T    Battery 2
TB3T    Battery
Tp0P    Power Supply 1
Tp0C    Power Supply 1 Alt.
Tp1P    Power Supply 2
Tp1C    Power Supply 2 Alt.
Tp2P    Power Supply 3
Tp3P    Power Supply 4
Tp4P    Power Supply 5
Tp5P    Power Supply 6

TS0C    Expansion Slots
TA0S    PCI Slot 1 Pos 1
TA1S    PCI Slot 1 Pos 2
TA2S    PCI Slot 2 Pos 1
TA3S    PCI Slot 2 Pos 2


VC0C    CPU Core 1
VC1C    CPU Core 2
VC2C    CPU Core 3
VC3C    CPU Core 4
VC4C    CPU Core 5
VC5C    CPU Core 6
VC6C    CPU Core 7
VC7C    CPU Core 8
VV1R    CPU VTT

VG0C    GPU Core

VM0R    Memory

VN1R    PCH
VN0C    MCH

VD0R    Mainboard S0 Rail
VD5R    Mainboard S5 Rail
VP0R    12V Rail
Vp0C    12V Vcc
VV2S    Main 3V
VR3R    Main 3.3V
VV1S    Main 5V
VH05    Main 5V
VV9S    Main 12V
VD2R    Main 12V
VV7S    Auxiliary 3V
VV3S    Standby 3V
VV8S    Standby 5V
VeES    PCIe 12V

VBAT    Battery
Vb0R    CMOS Battery


IC0C    CPU Core
IC1C    CPU VccIO
IC2C    CPU VccSA
IC0R    CPU Rail
IC5R    CPU DRAM
IC8R    CPU PLL
IC0G    CPU GFX
IC0M    CPU Memory

IG0C    GPU Rail

IM0C    Memory Controller
IM0R    Memory Rail

IN0C    MCH

ID0R    Mainboard S0 Rail
ID5R    Mainboard S5 Rail
IO0R    Misc. Rail

IB0R    Battery Rail
IPBR    Charger BMON
PC0C    CPU Core 1
PC1C    CPU Core 2
PC2C    CPU Core 3
PC3C    CPU Core 4
PC4C    CPU Core 5
PC5C    CPU Core 6
PC6C    CPU Core 7
PC7C    CPU Core 8
PCPC    CPU Cores
PCPG    CPU GFX
PCPD    CPU DRAM
PCTR    CPU Total
PCPL    CPU Total
PC1R    CPU Rail
PC5R    CPU S0 Rail
PGTR    GPU Total
PG0R    GPU Rail
PM0R    Memory Rail
PN0C    MCH
PN1R    PCH Rail
PC0R    Mainboard S0 Rail
PD0R    Mainboard S0 Rail
PD5R    Mainboard S5 Rail
PH02    Main 3.3V Rail
PH05    Main 5V Rail
Pp0R    12V Rail
PD2R    Main 12V Rail
PO0R    Misc. Rail
PBLC    Battery Rail
PB0R    Battery Rail

PDTR    DC In Total
PSTR    System Total



'''.strip().splitlines() if line.strip())


def sample_smc():

    exec_ = os.path.expanduser('~/Applications/smcFanControl.app/Contents/Resources/smc')
    proc = Popen([exec_, '-l'], stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()

    if proc.returncode:
        return

    res = {}
    for line in out.splitlines():

        m = re.match(r'^\s+(\S{4})\s+\[(....)\]\s+(.+)\s*$', line)
        if not m:
            continue

        key, type_, value = m.groups()
        if key not in KEY_TO_NAME:
            continue

        encoded = value.split('(')[0].strip()
        if not encoded:
            continue

        try:
            value = float(encoded)
        except:
            print >> sys.stderr, '#', m.groups()
            raise

        res[key + " " + KEY_TO_NAME[key]] = value

    return res



