let Client;

async function loadModule() {
  try {
    const module = await import("https://cdn.jsdelivr.net/npm/@gradio/client/dist/index.min.js");
    Client = module.Client;
  } catch (error) {
    console.error("Failed to load module:", error);
  }
}

loadModule();
