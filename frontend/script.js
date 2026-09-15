const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.strokeStyle = "white";
ctx.lineWidth = 18;
ctx.lineCap = "round";

let drawing = false;

canvas.addEventListener("mousedown", () => (drawing = true));
canvas.addEventListener("mouseup", () => (drawing = false));
canvas.addEventListener("mouseleave", () => (drawing = false));
canvas.addEventListener("mousemove", draw);

function draw(e) {
  if (!drawing) return;
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  ctx.lineTo(x, y);
  ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x, y);
}

canvas.addEventListener("mousedown", (e) => {
  const rect = canvas.getBoundingClientRect();
  ctx.beginPath();
  ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
});

document.getElementById("clearBtn").addEventListener("click", () => {
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  document.getElementById("result").innerText = "Prediction: —";
});

document.getElementById("predictBtn").addEventListener("click", async () => {
  canvas.toBlob(async (blob) => {
    const formData = new FormData();
    formData.append("file", blob, "digit.png");

    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      document.getElementById("result").innerText = "Error predicting";
      return;
    }

    const data = await res.json();
    document.getElementById("result").innerText =
      `Prediction: ${data.digit} (confidence: ${(data.confidence * 100).toFixed(1)}%)`;
  }, "image/png");
});