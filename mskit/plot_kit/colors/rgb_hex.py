
def hex_to_rgb(hex_color, base=256):
    return tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5))


def rgb_to_hex(rgb, rgb_base=255, with_sharp=True, upper=True):
    # Check channel num to be 3
    channel_num = len(rgb)
    if channel_num != 3:
        raise ValueError(f'The input rgb value {rgb} need three channels, now has {channel_num}')

    # Trans each rgb channel to 255 based number
    if rgb_base != 255:
        rgb = [int(one_channel * 255 / rgb_base) for one_channel in rgb]

    # Trans to hex code and check if length of hex code is 1
    hex_list = [hex(one_channel)[2:] for one_channel in rgb]
    for i in range(channel_num):
        if len(hex_list[i]) == 1:
            hex_list[i] = f'0{hex_list[i]}'

    # Join hex codes to full hex color
    hex_code = ''.join(hex_list)
    if with_sharp:
        hex_code = '#' + hex_code
    if upper:
        hex_code = hex_code.upper()
    return hex_code
