// Obtém a data atual
const hoje = new Date();

// Formata a data para o formato esperado pelo campo date (YYYY-MM-DD)
const dia = String(hoje.getDate()).padStart(2, '0');
const mes = String(hoje.getMonth() + 1).padStart(2, '0'); // Mês começa em 0
const ano = hoje.getFullYear();

// Define o valor padrão do campo date para a data atual
const dataAtual = `${ano}-${mes}-${dia}`;
document.getElementById('data').value = dataAtual;