def is_watering(ins):
    return ((ins & 0x0c) == 0x04)

def is_collecting(ins):
    return ((ins & 0x0c) == 0x00)

def is_full(ins):
    return ((ins & 0x02) == 0x00)

def is_charged(ins):
    return ((ins & 0x01) == 0x01)

