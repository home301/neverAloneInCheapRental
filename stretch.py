from PIL import Image

def stretch_lower_half(img_path, cut_y, scale_factor, out_path):
    img = Image.open(img_path)
    width, height = img.size
    
    # top part
    top = img.crop((0, 0, width, cut_y))
    
    # bottom part
    bottom = img.crop((0, cut_y, width, height))
    
    # resize bottom part
    new_bottom_height = int((height - cut_y) * scale_factor)
    bottom_resized = bottom.resize((width, new_bottom_height), Image.LANCZOS)
    
    # new image
    new_img = Image.new('RGB', (width, cut_y + new_bottom_height))
    new_img.paste(top, (0, 0))
    new_img.paste(bottom_resized, (0, cut_y))
    
    new_img.save(out_path)

input_img = r"C:\Users\cmk11\.gemini\antigravity\brain\8474edd3-2410-4ec2-8441-a5b9642aede7\ghost_front_v3_1_1772324508239.png"
base_dir = r"C:\Users\cmk11\.gemini\antigravity\brain\f61d2014-e28c-434f-888a-cc932f9a6632"

stretch_lower_half(input_img, 280, 1.4, base_dir + r"\ghost_stretch_var1.png")
stretch_lower_half(input_img, 320, 1.6, base_dir + r"\ghost_stretch_var2.png")
stretch_lower_half(input_img, 360, 1.8, base_dir + r"\ghost_stretch_var3.png")

print("Done generating variations.")
