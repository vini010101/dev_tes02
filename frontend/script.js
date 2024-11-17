document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("post-Form1");
    const postsList = document.getElementById("posts-list");

    // Função para buscar os posts da API
    async function fetchPosts() {
        try {
            const response = await fetch("/api/posts");
            const posts = await response.json();

            // Limpar posts atuais
            postsList.innerHTML = "";

            posts.forEach(post => {
                const postElement = document.createElement("div");
                postElement.classList.add("post");

                const postTitle = document.createElement("h2");
                postTitle.classList.add("post-title");
                postTitle.textContent = post.title;

                const postDescription = document.createElement("p");
                postDescription.classList.add("post-description");
                postDescription.textContent = post.description;

                postElement.appendChild(postTitle);
                postElement.appendChild(postDescription);

                postsList.appendChild(postElement);
            });
        } catch (error) {
            console.error("Erro ao carregar posts:", error);
            postsList.innerHTML = "<p>Erro ao carregar posts. Tente novamente mais tarde.</p>";
        }
    }

    // Chama a função para carregar posts ao iniciar a página
    fetchPosts();

    // Submissão do formulário
    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Impede o envio normal do formulário
    
        // Coleta os dados do formulário
        const title = document.getElementById("title").value.trim();
        const description = document.getElementById("description").value.trim();
    
        // Validação simples no lado do cliente
        if (!title || !description) {
            alert("Por favor, preencha todos os campos.");
            return;
        }
    
        // Criação do objeto de dados
        const postData = {
            title: title,
            description: description
        };
    
        try {
            // Envio da solicitação
            const response = await fetch("/api/create-post", { // Ajuste a URL se necessário
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(postData)
            });
    
            // Parsing da resposta
            const result = await response.json();
    
            if (response.ok) {
                // Exibe sucesso e atualiza a página
                alert("Post criado com sucesso!");
                form.reset(); // Limpar o formulário
                fetchPosts(); // Recarregar os posts
            } else {
                // Exibe erro retornado pela API
                alert("Erro ao criar post: " + (result.detail || "Erro desconhecido."));
            }
        } catch (error) {
            // Tratamento de erros inesperados
            console.error("Erro:", error);
            alert("Erro ao criar post. Verifique sua conexão ou tente novamente.");
        
        }
    });
});

document.getElementById("delete-all-posts-button").addEventListener("click", function () {
    if (confirm("Tem certeza de que deseja deletar todos os posts?")) {
        fetch('http://localhost:8000/posts/all', { // Substitua com sua URL correta
            method: 'DELETE',
        })
        .then(response => {
            if (response.ok) {
                alert("Todos os posts foram deletados com sucesso.");
                // Atualize a lista de posts após deletar
                document.getElementById("posts-list").innerHTML = "";
            } else {
                alert("Erro ao deletar os posts.");
            }
        })
        .catch(error => {
            alert("Erro de conexão com o servidor.");
        });
    }
});
