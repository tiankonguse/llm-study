// Add this to the beginning of your script
const imageCanvas = document.getElementById('image-canvas');
const imageCtx = imageCanvas.getContext('2d');
const brushPreviewCanvas = document.getElementById('brush-preview-canvas');
const brushPreviewCtx = brushPreviewCanvas.getContext('2d');
const brushSizeSlider = document.getElementById('brush-size-slider');
brushPreviewCanvas.style.pointerEvents = 'none';

const maxUndoStackSize = 1000; // Set the maximum number of elements for the undo stack
const undoStack = [];
let AllStrokes = [];
let currStrokeData = {};
let currentStroke = [];
const drawColor = {r: 255, g:0, b:0, a:0.2};
const deleteColor = {r: 0, g:0, b:255, a:0.2};
let brushColor = drawColor;
const magic_value = 8;

// Variables for the brush tool
let isBrushEnabled = false;
let isDrawing = false;

// Add event listeners for the brush tool
imageCanvas.addEventListener('mousedown', startCanvasDraw);
imageCanvas.addEventListener('mousemove', canvasDrawing);
imageCanvas.addEventListener('mouseup', stopCanvasDraw);



// Function to start drawing
function startCanvasDraw(e) {
    if (!isBrushEnabled) return;
}


// Function to draw
function canvasDrawing(e) {
    const offset = $('#preview').offset();
    lastMouseX = e.pageX - offset.left;
    lastMouseY = e.pageY - offset.top;
    if (!isDrawing) return;
}

// Function to stop drawing
function stopCanvasDraw() {
    if (!isBrushEnabled) return;
}

// Get mosue pos relative to the canvas
function getMousePos(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
        x: (event.clientX - rect.left) * scaleX,
        y: (event.clientY - rect.top) * scaleY
    };
}

// Get mouse pos relative to the original image
function getTrueMousePos(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const scaleX = $('#preview').data('originalWidth') / canvas.width;
    const scaleY = $('#preview').data('originalHeight') / canvas.height;
    return {
        x: (event.clientX - rect.left) * scaleX,
        y: (event.clientY - rect.top) * scaleY
    };
}


// Update the canvas size after loading the image
function updateCanvasSize() {
    // Save the current canvas content
    const currentCanvasContent = imageCtx.getImageData(0, 0, imageCanvas.width, imageCanvas.height);

    // Update the canvas size
    imageCanvas.width = $('#preview').width();
    imageCanvas.height = $('#preview').height();
    imageCtx.lineWidth = brushSizeSlider.value;
    
    // Update the brush preview canvas size
    updateBrushPreviewCanvasSize();

    // Draw the saved content back onto the canvas
    imageCtx.putImageData(currentCanvasContent, 0, 0);
}

function updateBrushPreviewCanvasSize() {
    brushPreviewCanvas.width = imageCanvas.width;
    brushPreviewCanvas.height = imageCanvas.height;
    brushPreviewCtx.lineWidth = brushSizeSlider.value;
    brushPreviewCtx.lineCap = 'round';
}

// Function to disable the brush tool
function disableBrush() {
    isBrushEnabled = false;
    imageCanvas.style.pointerEvents = 'none';
    brushPreviewCanvas.style.display = 'none';
}


// Function to enable the brush tool
function enableBrush() {
    isBrushEnabled = true;
    imageCanvas.style.pointerEvents = 'auto';
    imageCtx.strokeStyle = `rgba(${brushColor.r}, ${brushColor.g}, ${brushColor.b}, ${brushColor.a})`;
    imageCtx.lineWidth = brushSizeSlider.value; // Change this to the brush width you want
    imageCtx.lineJoin = 'round';
    imageCtx.lineCap = 'round';
    brushPreviewCanvas.style.display = 'block';
    brushPreviewCtx.lineWidth = brushSizeSlider.value;
    brushPreviewCtx.lineCap = 'round';
}