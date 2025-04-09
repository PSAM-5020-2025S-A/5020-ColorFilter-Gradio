import gradio as gr
import re

# Euclidean distance between 2 RGB color tuples
def color_distance(c0, c1):
  return ((c0[0] - c1[0])**2 + (c0[1] - c1[1])**2 + (c0[2] - c1[2])**2) ** 0.5

# Turns a css color string in the form `#12AB56` or
#                                      `rgb(18, 171, 87)` or
#                                      `rgba(18, 171, 87, 1)`
#   into an RGB list [18, 171, 87]
def css_to_rgb(css_str):
  if css_str[0] == "#":
    return [int(css_str[i:i+2], 16) for i in range(1,6,2)]

  COLOR_PATTERN = r"([^(]+)\(([0-9.]+), ?([0-9.]+%?), ?([0-9.]+%?)(, ?([0-9.]+))?\)"
  match = re.match(COLOR_PATTERN, css_str)
  if not match:
    return [0,0,0]

  if "rgb" in match.group(1):
    return [int(float(match.group(i))) for i in range(2,5)]

  if "hsl" in match.group(1):
    print("hsl not supported")
    return [0,0,0]

def highlight_color(img, keep_color_str, threshold):
  keep_color = css_to_rgb(keep_color_str)

  filtpxs = []
  for r,g,b in img.getdata():
    if color_distance((r, g, b), keep_color) < threshold:
      filtpxs.append((r, g, b))
    else:
      l = (r + g + b) // 3
      filtpxs.append((l, l, l))
  img.putdata(filtpxs)
  return img


my_inputs = [
  gr.Image(type="pil", show_label=False),
  gr.ColorPicker(value="#ffdf00", label="keep_color"),
  gr.Slider(0, 255, value=150, step=5)
]

my_outputs = [
  gr.Image(type="pil", show_label=False)
]

my_examples = [
  ["./imgs/arara.jpg", "#0014A6", 95],
  ["./imgs/flowers.jpg", "#F165EB", 100],
  ["./imgs/hog.jpg", "#FBF44A", 130]
]

with gr.Blocks() as demo:
  gr.Interface(
    fn=highlight_color,
    inputs=my_inputs,
    outputs=my_outputs,
    cache_examples=True,
    examples=my_examples,
    allow_flagging="never",
    fill_width=True
  )

if __name__ == "__main__":
   demo.launch()
