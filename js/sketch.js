let mClient;
let mImgIn;
let mImgOut;

async function preload() {
  mImgIn = loadImage("https://raw.githubusercontent.com/PSAM-5020-2025S-A/5020-Gradio/refs/heads/main/imgs/arara.jpg");
  let Gradio = await import("https://cdn.jsdelivr.net/npm/@gradio/client/dist/index.min.js");
  mClient = await Gradio.Client.connect("5020A/5020-Gradio");
}

let mColor;
let mSlider;
let mButton;

function setup() {
  createCanvas(windowWidth, windowHeight);
  mImgIn.resize(0, height / 2);
  mImgIn.loadPixels();

  mColor = createColorPicker("#ffdf00");
  mColor.position(mImgIn.width + 10, 10);
  mColor.size(200, 40);

  mSlider = createSlider(0, 255, 100, 5);
  mSlider.position(mImgIn.width + 10, 60);
  mSlider.size(200, 20);

  mButton = createButton("Filter");
  mButton.position(mImgIn.width + 10, 100);
  mButton.size(200, 40);
  mButton.mouseReleased(filterImage);
}

function draw() {
  background(220);

  image(mImgIn, 0, 0);

  if (mImgOut) {
    image(mImgOut, 0, mImgIn.height);
  }
}

function filterImage() {
  mImgIn.canvas.toBlob(runFilter);
}

async function runFilter(imgBlob) {
  let inputs = {
    img: imgBlob,
    keep_color_str: mColor.value(),
    threshold: mSlider.value()
  }

  let filterRes = await mClient.predict("/predict", inputs);
  mImgOut = loadImage(filterRes.data[0].url);
}

function mouseReleased() {
  if (mouseX > mImgIn.width || mouseY > mImgIn.height) return;

  let imgIdx = 4 * (mouseY * mImgIn.width + mouseX);

  let pxColor = "#";
  for (let c = 0; c < 3; c += 1) {
    pxColor += `00${(mImgIn.pixels[imgIdx + c]).toString(16)}`.slice(-2);
  }
  mColor.value(pxColor);
}
