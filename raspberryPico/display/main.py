
from machine import Pin,UART
from nanoguilib.color_setup import ssd
from nanoguilib.nanogui import refresh
from nanoguilib.writer import CWriter
import uasyncio as asyncio
from nanoguilib.colors import *
import nanoguilib.arial10 as arial10
from nanoguilib.label import Label
from nanoguilib.textbox import Textbox
import time

pargs = (2, 2, 124, 7) # Row, Col, Width, nlines
tbargs = {
    'fgcolor' : YELLOW,
    'bdcolor' : RED,
    'bgcolor' : DARKGREEN,
}


async def init():
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
    uart.init(bits=8, parity=None, stop=2)
    return uart


async def wrap(wri):
    s = '''init text'''
    tb = Textbox(wri, *pargs, clip=False, **tbargs)
    tb.append(s, ntrim=100, line=0)
    refresh(ssd)
    while True:
        await asyncio.sleep(1)
        if not tb.scroll(1):
            break
        refresh(ssd)


async def radar():
    return


async def clip(wri, uart):
    ss = ()
    tb = Textbox(wri, *pargs, clip=True, **tbargs)
    while True:
        tb.append(uart.read(), ntrim=100)
        refresh(ssd)
        await asyncio.sleep(1)
    ##for s in ss:
        ##tb.append(s, ntrim=100)
        ##refresh(ssd)
        ##await asyncio.sleep(1)


async def main(wri, uart):
    await wrap(wri)
    await clip(wri, uart)


def test():
    refresh(ssd, True)
    CWriter.set_textpos(ssd, 0, 0)
    wri CWriter(ssd, arial10, verbose=False)
    wri.set_clip(True, True, False)
    uart = init()
    asyncio.run(main(wri, uart))


test()