document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('recommendationForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const payload = {
            seatingCapacity: document.getElementById('Capacity').value,
            fuelType: document.getElementById('fuelType').value,
            startingPrice: document.getElementById('startingPrice').value,
            endingPrice: document.getElementById('endingPrice').value,
            transmissionType: document.getElementById('transmissionType').value,
            bodyType: document.getElementById('bodyType').value
        };

        fetch('http://127.0.0.1:5000/recommend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response data:', data);
            const carList = document.getElementById('carList');
            carList.innerHTML = '';

            if (data.recommendations && data.recommendations.length === 0) {
            } else if (data.recommendations) {
                data.recommendations.forEach(car => {
                    const li = document.createElement('li');
                    li.textContent = `Car Name: ${car.car_name}, Fuel Type: ${car.fuel_type}, Transmission Type: ${car.transmission_type}, Seating Capacity: ${car.seating_capacity}, Price Range: ${car.starting_price} - ${car.ending_price}`;
                    carList.appendChild(li);
                });
            } 
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Recommendation failed.');
        });
    });
});
