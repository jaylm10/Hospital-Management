if(window.location.pathname =="/"){
    document.getElementById("registrationForm").onsubmit = async(e)=>{
        e.preventDefault();
        const data = {
            name : document.getElementById("name").value,
            age: document.getElementById('age').value,
            contact: document.getElementById('contact').value,
            address: document.getElementById('address').value,
            time_slot: document.getElementById('time_slot').value
        }

        const response = await fetch('/register',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        const result = await response.json();

        if (result.success) {
            window.location.href = `/symptoms/${result.patient_id}`; 
        } else {
            showAlert('Registration failed. Please try again.');
        }

    };

} else if (window.location.pathname.startsWith("/symptoms")) {
    document.getElementById("symptomsForm").onsubmit = async (e) => {
        e.preventDefault();

        // Get patient_id from the URL
        const patient_id = window.location.pathname.split('/')[2];

        // Collect form data
        const data = {
            patient_id: patient_id,  // Send patient_id as a string
            illness: document.getElementById("illness").value,
            urgency: document.getElementById("urgency").value
        };

        // Send data to the Flask backend
        const response = await fetch('/add_symptoms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Handle the response
        const result = await response.json();
        if (result.success) {
            window.location.href = result.redirect_url;  // Redirect to queue page
        } else {
            alert('Submission failed. Please try again.');
        }
    };
}