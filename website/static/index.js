$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})

function deleteChore(choreID) {
  fetch("/delete-chore", {
    method: "POST",
    body: JSON.stringify({ choreID: choreID }),
  }).then((_res) => {
    window.location.href = "/chores-board";
  });
}

function checkChore(choreID) {
  fetch("/check-chore", {
    method: "POST",
    body: JSON.stringify({ choreID: choreID }),
  }).then((_res) => {
    window.location.href = "/chores-board";
  });
}
function uncheckChore(choreID) {
  fetch("/uncheck-chore", {
    method: "POST",
    body: JSON.stringify({ choreID: choreID }),
  }).then((_res) => {
    window.location.href = "/chores-board";
  });
}