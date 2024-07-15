const canvas = document.getElementById('signatureCanvas');
const ctx = canvas.getContext('2d');
let isDrawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', endDrawing);
canvas.addEventListener('mouseout', endDrawing);

function startDrawing(e) {
    isDrawing = true;
    draw(e);
}

function draw(e) {
    if (!isDrawing) return;
    ctx.lineWidth = 2;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#000';
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.offsetX, e.offsetY);
}

function endDrawing() {
    isDrawing = false;
    ctx.closePath();
}

function clearSignature() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}
function submitData() {
    // Retrieve form data
    var formData = {
        name: document.getElementById('name').value,
        contact: document.getElementById('contact').value,
        email: document.getElementById('email').value,
        signature: document.getElementById('signatureCanvas').toDataURL(), // Convert canvas to base64 data URL
        image: document.getElementById('imageUpload').files[0] // File object for image upload
    };

    // Store data in localStorage (for demonstration purposes only, use appropriate storage for production)
    localStorage.setItem('rentalFormData', JSON.stringify(formData));

    // Optionally, you can clear form fields after submission
    document.getElementById('name').value = '';
    document.getElementById('contact').value = '';
    document.getElementById('email').value = '';
    clearSignature(); // Clear signature canvas
    document.getElementById('imageUpload').value = ''; // Clear file input

    // Inform user or redirect to another page as needed
    alert('Product submitted successfully! We\'ll review your product and will let you know if you can sell it or not.');

    // Prevent form submission (if using <form> element)
    return false;
}

function clearSignature() {
    var canvas = document.getElementById('signatureCanvas');
    var context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
}
