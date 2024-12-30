 
 // Récupération des éléments des villes
 const villeDepart = document.getElementById('ville_depart');
 const villeArrivee = document.getElementById('ville_arrivee');

 // Fonction pour mettre à jour les options de ville d'arrivée
 villeDepart.addEventListener('change', function () {
     const selectedDepart = this.value; // Ville de départ choisie

     // Réinitialiser les options de la ville d'arrivée
     villeArrivee.innerHTML = `
         <option value="">Choisir</option>
         <option value="DOUALA" ${selectedDepart === 'DOUALA' ? 'disabled' : ''}>DOUALA</option>
         <option value="YAOUNDE" ${selectedDepart === 'YAOUNDE' ? 'disabled' : ''}>YAOUNDE</option>
     `;
 });



 //blocage sur le choix de la date

 // Récupérer le champ de date
const dateVoyage = document.getElementById('date_voyage');

// Obtenir la date actuelle
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0'); // Mois (1-12)
const day = String(today.getDate()).padStart(2, '0'); // Jour du mois

// Formater la date au format YYYY-MM-DD
const minDate = `${year}-${month}-${day}`;

// Définir la date minimale pour le champ
dateVoyage.setAttribute('min', minDate);
