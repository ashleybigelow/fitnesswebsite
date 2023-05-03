
var modal = document.getElementById('id01');

function dropDown() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
  else if (event.target == modal) {
    modal.style.display = "none";
  }
}

function deleteWorkout(workoutId){
  fetch('/delete-workout', {
    method: 'POST',
    body: JSON.stringify({workoutId: workoutId})
  }).then((_res)=> {
    window.location.href = '/history'
  })
}

function deleteAccount(){
  fetch('/delete-acct', {
    method: 'POST',
  }).then((_res)=> {
    window.location.href = '/'
  })
}