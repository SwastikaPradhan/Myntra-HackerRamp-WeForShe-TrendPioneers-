document.addEventListener("DOMContentLoaded", function () {
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

    window.clearSignature = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    window.validateSignature = function () {
        const signatureError = document.getElementById('signatureError');
        const isEmpty = isCanvasBlank(canvas);

        if (isEmpty) {
            signatureError.style.display = 'block';
            return false;
        } else {
            signatureError.style.display = 'none';
            return true;
        }
    }

    function isCanvasBlank(canvas) {
        const blank = document.createElement('canvas');
        blank.width = canvas.width;
        blank.height = canvas.height;
        return canvas.toDataURL() === blank.toDataURL();
    }

    // Form submission handler
    document.getElementById('rentalForm').addEventListener('submit', function (event) {
        if (!validateSignature()) {
            event.preventDefault(); // Prevent form submission if signature is not valid
        } else {
            submitData();
        }
    });

    function submitData() {
        var formData = {
            name: document.getElementById('name').value,
            contact: document.getElementById('contact').value,
            email: document.getElementById('email').value,
            signature: canvas.toDataURL(), 
            image: document.getElementById('imageUpload').files[0] 
        };

        localStorage.setItem('rentalFormData', JSON.stringify(formData));

        document.getElementById('name').value = '';
        document.getElementById('contact').value = '';
        document.getElementById('email').value = '';
        clearSignature(); // Clear signature canvas
        document.getElementById('imageUpload').value = ''; // Clear file input

        // Inform user or redirect to another page as needed
        alert('Product submitted successfully! We\'ll review your product and will let you know if you can sell it or not.');
    }
});
