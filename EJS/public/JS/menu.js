//JS do menu responsivo
const menuBtn = document.querySelector(".menu-btn");
const navigation = document.querySelector("nav");
const profile = document.querySelector(".profile");

menuBtn.addEventListener("click", () => {
    menuBtn.classList.toggle("active");
    navigation.classList.toggle("active");
});

//JS video slider
const btns = document.querySelectorAll(".slider-nav-btn");
const slides = document.querySelectorAll(".video-slide");
const contents = document.querySelectorAll(".content");

var sliderNav = function(manual) {
    btns.forEach((btn) => {
        btn.classList.remove("active");
    });

    slides.forEach((slide) => {
        slide.classList.remove("active");
    });

    contents.forEach((content) => {
        content.classList.remove("active");
    });

    btns[manual].classList.add("active");
    slides[manual].classList.add("active");
    contents[manual].classList.add("active");
}

btns.forEach((btn, i) => {
    btn.addEventListener("click", () => {
       sliderNav(i); 
    });
});

//Cadastro
let nome = document.getElementById("nome");
let sobrenome = document.getElementById("sobrenome");
let apelido = document.getElementById("apelido");
let email = document.getElementById("email");
let senha = document.getElementById("senha");

async function criarUsuario() {
    if (!nome.value) {
        alert("O nome é obrigatório");
        return;
    }

    if (!sobrenome.value) {
        alert("O sobrenome é obrigatório");
        return;
    }

    if (!apelido.value) {
        alert("O apelido é obrigatório");
        return;
    }

    if (!email.value) {
        alert("O e-mail é obrigatório");
        return;
    }

    if (!senha.value) {
        alert("A senha é obrigatória");
        return;
    }

    // Cria um objeto com os valores que serão enviados para o servidor.
    let dadosParaEnvio = {
        nome: nome.value,
        sobrenome: sobrenome.value,
        apelido: apelido.value,
        email: email.value,
        senha: senha.value
    };

    let opcoes = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dadosParaEnvio)
    };

    try {
        let response = await fetch("/criarUsuario", opcoes);

        if (response.ok) {
            // Limpa os campos para facilitar a criação da próxima pessoa.
            nome.value = "";
            sobrenome.value = "";
            apelido.value = "";
            email.value = "";
            senha.value = "";

            alert("Conta criada com sucesso!");
        } else {
            alert("Erro ao criar conta!");
        }
    } catch (ex) {
        alert("Erro de rede: " + ex.message);
    }
}