document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('recommendationForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const payload = {
            seatingCapacity: parseFloat(document.getElementById('Capacity').value), // Parse as float for consistency
            fuelType: document.getElementById('fuelType').value.trim(), // Trim for cleaner inputs
            startingPrice: parseInt(document.getElementById('startingPrice').value),
            endingPrice: parseInt(document.getElementById('endingPrice').value),
            transmissionType: document.getElementById('transmissionType').value.trim(),
            bodyType: document.getElementById('bodyType').value.trim()
        };

        fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            const carList = document.getElementById('carList');
            carList.innerHTML = '';

            if (data.recommendations && data.recommendations.length === 0) {
                carList.innerHTML = '<p>No cars match your criteria.</p>';
            } else if (data.recommendations) {
                data.recommendations.forEach(car => {
                    const li = document.createElement('li');
                    li.textContent = `Car Name: ${car.car_name}, Fuel Type: ${car.fuel_type}, Transmission: ${car.transmission_type}, Seating Capacity: ${car.seating_capacity}, Price Range: ${car.starting_price} - ${car.ending_price}`;
                    carList.appendChild(li);
                });
            } else {
                carList.innerHTML = '<p>An unexpected error occurred.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Recommendation failed. Please check your input or try again later.');
        });
    });
});
