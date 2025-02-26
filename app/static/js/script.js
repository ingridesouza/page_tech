document.addEventListener("DOMContentLoaded", function() {
    // Menu de navegação suave
    document.querySelectorAll('nav ul li a').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Formulário de contato com efeito de feedback
    document.getElementById("formContato").addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(this);
        
        fetch("/contato", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            let mensagem = document.createElement("div");
            mensagem.textContent = data.message;
            mensagem.classList.add("mensagem-sucesso");
            this.appendChild(mensagem);
            setTimeout(() => mensagem.remove(), 3000);
            this.reset();
        })
        .catch(error => console.error("Erro ao enviar mensagem:", error));
    });

    // Animação de entrada dos serviços com efeito interativo
    const servicos = document.querySelectorAll(".servico");
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("mostrar");
            }
        });
    }, { threshold: 0.3 });

    servicos.forEach(servico => {
        observer.observe(servico);
        servico.addEventListener("mouseover", function() {
            this.style.transform = "scale(1.05)";
            this.style.boxShadow = "0px 0px 20px rgba(0, 212, 255, 0.7)";
        });
        servico.addEventListener("mouseleave", function() {
            this.style.transform = "scale(1)";
            this.style.boxShadow = "none";
        });
    });

    // Efeito de fundo tecnológico
    const backgroundEffect = document.createElement("div");
    backgroundEffect.classList.add("background-animation");
    document.body.appendChild(backgroundEffect);
});
