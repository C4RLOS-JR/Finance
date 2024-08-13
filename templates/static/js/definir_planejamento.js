function modificar_valor_planejamento(id) { // Recebe o id da categoria
  valor = document.getElementById('valor-categoria-'+id).value  // Captura o valor do elemento pelo seu id
  
  fetch('/planejamento/modificar_valor_planejamento/'+id,{ // O fetch faz uma requisição para a url.
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({novo_valor: valor})
  }).then(function(result){
    if (result) {
      window.location.href = "/perfil/home";
    }
  })
}