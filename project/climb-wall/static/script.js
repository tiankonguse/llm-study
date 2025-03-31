
let selectedImage = null;
let drawing = false;
let startPoint = { x: 0, y: 0 };
const boxes = [];
const box = document.createElement("div");

box.style.position = "absolute";
box.style.pointerEvents = "none";
document.getElementById("image-container").appendChild(box);

// Disable default browser usage
document.getElementById('preview').ondragstart = function() { return false; };

class Deque {
    constructor(maxlen) {
        this.items = [];
        this.maxlen = maxlen;
    }
    push_left(item) {
        if (this.items.length < this.maxlen) {
            this.items.unshift(item);
        }
        else {
            this.pop();
            this.items.unshift(item);
        }
    }
    push(item) {
        if (this.items.length < this.maxlen) {
            this.items.push(item);
        }
        else {
            this.pop_left();
            this.items.push(item);
        }
    }
    pop_left() {
        if (this.isEmpty()) {
            return null;
        }
        return this.items.shift();
    }
    pop() {
        if (this.isEmpty()) {
            return null;
        }
        return this.items.pop();
    }
    isEmpty() {
        return this.items.length === 0;
    }
    size() {
        return this.items.length;
    }
}

const max_deque_len = 1000;
let mode = "box"; // Default mode is 'point', 'point'/'box'
let queue = new Deque(max_deque_len); // Undo / do list
let trackDataNum = new Deque(max_deque_len);
let lastMouseX = 0;
let lastMouseY = 0;

// For dragging image to move in the image-container
let ctrlPressed = false;
let dragging = false;
let prevMouseX;
let prevMouseY;


// Capture mouse click position on the image
const points = [];

function rgbToCSS(r, g, b) {
    return `rgb(${r}, ${g}, ${b})`;
}

$("#preview").attr("src", getDefaultDarkImageBase64());
$("#load-image").click(function () {
    $("#input-image").trigger("click");
});
$("#input-image").change(function () {
    document.getElementById("image-name").textContent = this.files[0].name;
    readURL(this);
});


$("#preview").mouseenter(function () {
    console.log("preview mouseenter");
});
$("#preview").mouseleave(function () {
    console.log("preview mouseleave");
});
$("#preview").mousedown(function (e) {
    if (selectedImage === null) {
        alert("请先上传一面墙或者从墙列表中选择一面墙.");
        return;
    }
    if (e.which === 1 && mode === "box") { // Left mouse button
        drawing = true;
        startPoint.x = e.pageX - $(this).offset().left;
        startPoint.y = e.pageY - $(this).offset().top;
        box.style.border = "3px solid red";
        box.style.width = "0px";
        box.style.height = "0px";
        box.style.left = startPoint.x + "px";
        box.style.top = startPoint.y + "px";
    }
    console.log("preview mousedown, mode=" +  mode + ", drawing=" + drawing);
});
$("#preview").click(function(e) {
    if ($('#input-image')[0].files.length === 0 && $("#preview").attr("src") == "#") {
        $("#input-image").trigger("click");
    }
});

$("#preview").mousemove(function (e) {
    // console.log("preview mousemove");
    const offset = $(this).offset();
    lastMouseX = e.pageX - offset.left;
    lastMouseY = e.pageY - offset.top;

    if (drawing && mode === "box") {
        const currentX = e.pageX - $(this).offset().left;
        const currentY = e.pageY - $(this).offset().top;
        const width = currentX - startPoint.x;
        const height = currentY - startPoint.y;
        box.style.width = Math.abs(width) + "px";
        box.style.height = Math.abs(height) + "px";
        box.style.left = (width < 0 ? currentX : startPoint.x) + "px";
        box.style.top = (height < 0 ? currentY : startPoint.y) + "px";
    }
});
$("#preview").mouseup(function (e) {
    console.log("preview mouseup");
    var coor_temp;
    if (drawing && mode === "box") {
        drawing = false;
        const endX = e.pageX - $(this).offset().left;
        const endY = e.pageY - $(this).offset().top;
        const coordinates = {
            x1: Math.min(startPoint.x, endX),
            y1: Math.min(startPoint.y, endY),
            x2: Math.max(startPoint.x, endX),
            y2: Math.max(startPoint.y, endY)
        };
        var img = $("#preview")[0];
        var scaleX = img.naturalWidth / img.clientWidth;
        var scaleY = img.naturalHeight / img.clientHeight;
        coor_temp = coordinates;
        sendBoundingBoxCoordinates(coordinates);
    }
    if (mode === "box") {
        // Create a new box
        const newBox = document.createElement("div");
        newBox.classList.add("box");
        newBox.style.position = "absolute";
        newBox.style.border = `3px solid ${rgbToCSS(22, 154, 224)}`;
        newBox.style.pointerEvents = "none";
        newBox.style.width = box.style.width;
        newBox.style.height = box.style.height;
        newBox.style.left = box.style.left;
        newBox.style.top = box.style.top;
        document.getElementById("image-container").appendChild(newBox);
        // Store the original positions and sizes
        newBox.dataset.originalX1 = parseFloat(coor_temp.x1 * scaleX);
        newBox.dataset.originalY1 = parseFloat(coor_temp.y1 * scaleY);
        newBox.dataset.originalX2 = parseFloat(coor_temp.x2 * scaleX);
        newBox.dataset.originalY2 = parseFloat(coor_temp.y2 * scaleY);
        // Set box to invisible
        box.style.border = "none";
        boxes.push(newBox);
        // Hide zoomBox after drawing the bounding box
        // zoomBox.style.display = "none";
        // push to queue (for undo)
        queue.push("box");
    }
    console.log("preview mousedown, mode=" +  mode + ", drawing=" + drawing);
});
function sendBoundingBoxCoordinates(coordinates) {
    console.log(coordinates);
    // Send the coordinates to the server
    var img = $("#preview")[0];
    var scaleX = img.naturalWidth / img.clientWidth;
    var scaleY = img.naturalHeight / img.clientHeight;
    $.ajax({
        url: '/box_receive',
        type: 'POST',
        data: JSON.stringify({ 
            x1: coordinates.x1 * scaleX, y1: coordinates.y1 * scaleY, 
            x2: coordinates.x2 * scaleX, y2: coordinates.y2 * scaleY, 
        }),
        contentType: 'application/json',
        success: function(response) {
            console.log(response);
        }
    });
}
const container = document.getElementById("image-container");
container.addEventListener('mousedown', (e) => {
    console.log("container mousedown");
});

container.addEventListener('mousemove', (e) => {
    // console.log("container mousemove");
    if (dragging) {
        const deltaX = e.clientX - prevMouseX;
        const deltaY = e.clientY - prevMouseY;
        container.scrollLeft -= deltaX;
        container.scrollTop -= deltaY;
        prevMouseX = e.clientX;
        prevMouseY = e.clientY;
        e.preventDefault(); // Prevent other mouse events
    }
});
container.addEventListener('mouseup', (e) => {
    console.log("container mouseup");
});

$("#inference").click(async function() {
    // Disable buttons and mouse event when processing
    toggleProcessingButtons(true);
    $("#preview").css("pointer-events", "wait");
    $("#preview").css("cursor", "wait");

    await processButtonClick("inference");
    togglePointsAndBoxesVisibility(false);
    console.log("trackDataNum ", trackDataNum.size());
    if (trackDataNum.size() > 0) {
        var PrevDataNum = trackDataNum.pop();
    }
    else {
        var PrevDataNum = {"p": 0, "b": 0};
    }
    var thisTimeInputNum = {
        "p": points.length - PrevDataNum["p"],
        "b": boxes.length - PrevDataNum["b"]
    };
    var currDataNum = {
        "p": points.length, 
        "b": boxes.length
    };
    trackDataNum.push(currDataNum);
    console.log("This time inference: ", thisTimeInputNum["p"], thisTimeInputNum["b"]);
    var info = "inference-" + thisTimeInputNum["p"] + "-" + thisTimeInputNum["b"];
    queue.push(info);

    // Enable buttons and mouse events after processing
    toggleProcessingButtons(false);
    clear_original_display_style();
    $("#preview").css("pointer-events", "auto");
    $("#preview").css("cursor", "crosshair");
});


function clear_original_display_style() {
    const imageContainer = document.getElementById("image-container");
    const pointsAndBoxes = imageContainer.querySelectorAll(".point, .box");
    pointsAndBoxes.forEach(element => {
        const $element = $(element); // Wrap the element with jQuery
        $element.removeData("original-display-style");
    });
}


function toggleProcessingButtons(disabled) {
    $("button").prop("disabled", disabled);
    if (disabled) {
        $("button").addClass("processing");
    } else {
        $("button").removeClass("processing");
    }
}

function togglePointsAndBoxesVisibility(enable) {
    const imageContainer = document.getElementById("image-container");
    const pointsAndBoxes = imageContainer.querySelectorAll(".point, .box");

    pointsAndBoxes.forEach(element => {
        const $element = $(element); // Wrap the element with jQuery
        const currentDisplayStyle = $element.css("display");

        if (enable) {
            // Retrieve the original display style from the data attribute
            const originalDisplayStyle = $element.data("original-display-style");
            if (originalDisplayStyle) {
                // Set the original display style back to the element
                $element.css("display", originalDisplayStyle);
                $element.removeData("original-display-style");
            }
        } 
        else {
            if (!$element.data("original-display-style")) {
                // Store the current display style in a data attribute
                $element.data("original-display-style", currentDisplayStyle);
                $element.css("display", "none");
            }
        }
    });
}

function getDefaultDarkImageBase64() {
    let canvas = document.getElementById('default-preview-canvas');
    let ctx = canvas.getContext('2d');
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/png');
}

function readURL(input) {
    clearAllBoxes();

    if (!input.files || !input.files[0]) {
        return
    }
    selectedImage = input.files[0]; // Store the selected file
    let reader = new FileReader();
    reader.onload = function (e) {
        const preview = document.getElementById("preview");
        const imgContainer = document.getElementById("image-container");
        $('#preview').attr('src', e.target.result);
        // Update the zoomImage src when the preview image changes

        var img = new Image();
        img.src = e.target.result;
        img.onload = function () {
            // Store the original width and height
            $('#preview').data('originalWidth', this.width);
            $('#preview').data('originalHeight', this.height);

            // Call resizeImageContainer when the image is loaded
            resizeImageContainer(this.width, this.height);
            updateCanvasSize();
        }
    };
    reader.readAsDataURL(input.files[0]);

    // Init server after upload image
    var form_data = new FormData();
    form_data.append("image", input.files[0]);

    $.ajax({
        url: "/upload_image",
        type: "POST",
        data: form_data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {
            console.log(response);
            SelectBoxModel();
        },
    });

}

function SelectBoxModel(){
    processButtonClick("box");
    toggleSelectedModeButton("button_box");
    disableBrush();
    mode = "box";
}

// Add click event listeners for other buttons
async function processButtonClick(button_id) {
    if (selectedImage === null) {
        alert("请先上传一面墙或者从墙列表中选择一面墙.");
        return;
    }
    if (button_id !== null) {
        const image_jpeg = "jpeg";
        const image_png= "png";
        const image_type = image_png;
        await $.ajax({
            url: "/button_click",
            type: "POST",
            data: JSON.stringify({ 
                button_id: button_id,
                image_type: image_type,
             }),
            contentType: "application/json",
            success: function (response) {
                const image = new Image();
                if(image_type == image_jpeg){
                    image.src = "data:image/jpeg;base64," + response.image;
                }else if(image_type == image_png){
                    image.src = "data:image/png;base64," + response.image;
                }else{
                    alert("unknown image type " + image_type);
                }
                image.onload = function () {
                    $("#preview").attr("src", image.src);
                    // $('#zoom-image').attr('src', image.src);
                };
            },
        });
    }
}


function toggleSelectedModeButton(buttonId) {
    // Remove the 'selected-Mode' class from all Mode buttons
    $("#button4, #button5, #button_box, #brush").removeClass("selected-view");
    // Add the 'selected-Mode' class to the clicked Mode button
    $(`#${buttonId}`).addClass("selected-view");
}


// For drawing bounding boxes
function clearAllBoxes() {
    boxes.forEach(box => {
        box.remove();
    });
    boxes.length = 0;
    box.style.width = "0px";
    box.style.height = "0px";
    box.style.left = "0px";
    box.style.top = "0px";
    box.style.border = "none";
}


function resizeImageContainer(originalWidth, originalHeight) {
    const preview = document.getElementById("preview");
    const imgContainer = document.getElementById("image-container");

    // Calculate the new width and height while maintaining the aspect ratio
    const aspectRatio = originalWidth / originalHeight;
    const maxHeight = window.innerHeight * 0.8 - 10;
    const maxWidth = window.innerWidth * 0.8;
    let newHeight = maxHeight;
    let newWidth = newHeight * aspectRatio;

    if (newWidth > maxWidth) {
        newWidth = maxWidth;
        newHeight = newWidth / aspectRatio;
    }

    // Set the new width and height for the preview image
    preview.style.width = newWidth - 8 + 'px';
    preview.style.height = newHeight - 8 + 'px';
    imgContainer.style.width = newWidth + 'px';
    imgContainer.style.height = newHeight + 'px';
}
