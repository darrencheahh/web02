function purchase(eventId, availableTickets) {
    const quantityInput = prompt('Enter quantity to purchase:', availableTickets);

    // Check if the user pressed "Cancel" or entered an invalid quantity
    if (quantityInput === null || isNaN(quantityInput)) {
        alert('Invalid quantity!');
        return;
    }

    const quantity = parseInt(quantityInput);

    if (quantity > 0 && quantity <= availableTickets) {
        const formData = new FormData();
        formData.append('quantity', quantity);

        console.log(formData);  // Add this line to check the form data

        fetch(`/purchase-event`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams(formData),
        })
        .then((res) => res.json())
        .then((data) => {
            // Handle the response, update UI, etc.
            console.log(data);
        });
    } else {
        alert('Invalid quantity!');
    }
}