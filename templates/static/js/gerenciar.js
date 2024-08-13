function confirmarExcluir() {
    return confirm('Você tem certeza que deseja excluir essa conta?');
}

function selecionado(checkbox, otherCheckboxId) {
  if (checkbox.checked) {
    document.getElementById(otherCheckboxId).checked = false;
  }
}