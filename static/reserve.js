 function loadReservationPage() {
        fetch('..../reservation/templates/index.html')
            .then(response => response.text())
            .then(data => {
                document.getElementById('reservationContent').innerHTML = data;
            });
    }

    document.querySelector('.menu-toggle').addEventListener('click', () => {
        document.querySelector('.nav-links').classList.toggle('show');
    });
    
    document.querySelector('.menu-toggle').addEventListener('click', () => {
    document.querySelector('.nav-links').classList.toggle('show');
});

// Logic to disable the same city selection for departure and arrival
const villeDepartSelect = document.getElementById('ville_depart');
const villeArriveeSelect = document.getElementById('ville_arrivee');

villeDepartSelect.addEventListener('change', () => {
    const selectedVilleDepart = villeDepartSelect.value;
    Array.from(villeArriveeSelect.options).forEach(option => {
        option.disabled = option.value === selectedVilleDepart;
    });
});

villeArriveeSelect.addEventListener('change', () => {
    const selectedVilleArrivee = villeArriveeSelect.value;
    Array.from(villeDepartSelect.options).forEach(option => {
        option.disabled = option.value === selectedVilleArrivee;
    });
});
