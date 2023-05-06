import colorlover as cl
import colorsys
import webcolors

'''def adjust_saturation(colors, saturation_factor):
    adjusted_colors = []
    
    for color in colors:
        r, g, b = [x / 255.0 for x in cl.to_numeric(color)]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        s = min(max(s * saturation_factor, 0), 1)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        adjusted_colors.append(cl.to_html([(int(r * 255), int(g * 255), int(b * 255))])[0])
    
    return adjusted_colors'''


def adjust_saturation(colors, saturation_factor):
    adjusted_colors = []
    
    for hex_color in colors:
        # Convert hex to RGB and normalize to range [0, 1]
        r, g, b = [x / 255.0 for x in webcolors.hex_to_rgb(hex_color)]
        
        # Convert RGB to HSV
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        # Adjust saturation
        s = min(max(s * saturation_factor, 0), 1)
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        # Convert back to hex and append to the adjusted_colors list
        adjusted_colors.append(webcolors.rgb_to_hex((int(r * 255), int(g * 255), int(b * 255))))
    
    return adjusted_colors



def create_color_groups(base_colors, group_count, saturation_factors):
    color_groups = []
    for i in range(group_count):
        saturation_factor = saturation_factors[i % len(saturation_factors)]
        group_colors = adjust_saturation(base_colors, saturation_factor)
        color_groups.extend(group_colors)
    return color_groups

def distribute_colors(colors):
    num_colors = len(colors)
    new_colors = [colors[i::num_colors//2] for i in range(num_colors//2)]
    distributed_colors = [color for sublist in zip(*new_colors) for color in sublist]
    return distributed_colors
    

# base_colors = cl.scales['9']['qual']['Set1']
# saturation_factors = [1.2, 1.5]  # Define saturation factors for alternating color groups
# group_count = 4

# colors = create_color_groups(base_colors, group_count, saturation_factors)
# distributed_colors = distribute_colors(colors)