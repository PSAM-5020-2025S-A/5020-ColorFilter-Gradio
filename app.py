import gradio as gr

# Euclidean distance between 2 RGB color tuples
def color_distance(c0, c1):
  return ((c0[0] - c1[0])**2 + (c0[1] - c1[1])**2 + (c0[2] - c1[2])**2) ** 0.5

# Turns a color hex string in the form `#12AB56`
#   into an RGB tuple (18, 171, 87)
def hex_string_to_rgb(hex_str):
  return (
    int(hex_str[1:3], 16),
    int(hex_str[3:5], 16),
    int(hex_str[5:7], 16),
  )

def highlight_color(img, keep_color_str, threshold):
  keep_color = hex_string_to_rgb(keep_color_str)

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
  gr.ColorPicker(value="#ffdf00", label="keep_color", interactive=True),
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
