from rgb_dsa import xatLabsRGBDSAController
import time

c = xatLabsRGBDSAController("COM4", debug=True)
time.sleep(3)
c.sync()
c.set_text(0, [{"text": "mgys", "color": "ff0040"},{"text": " beste", "color": "00ff00"},{"text": " :D"}], c.ALIGN_CENTER, 1000)
c.set_text(1, "Text ist zu lang", c.ALIGN_CENTER, 1000)