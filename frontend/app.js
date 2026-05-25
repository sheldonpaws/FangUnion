// ===== FangUnion — Союз Клыков =====

const API = "http://127.0.0.1:8000/api";

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString("ru-RU", {
        day: "numeric", month: "long", year: "numeric",
        hour: "2-digit", minute: "2-digit",
    });
}

// ===== Посты =====

async function loadPosts() {
    try {
        const res = await fetch(`${API}/posts/`);
        if (!res.ok) throw new Error("Ошибка сервера");
        const posts = await res.json();
        const container = document.getElementById("posts-container");

        if (posts.length === 0) {
            container.innerHTML = `
                <div class="card" style="text-align:center;">
                    <p style="color:var(--text-muted);">Лента пуста. Будь первым в стае! 🐾</p>
                </div>`;
            return;
        }

        container.innerHTML = posts.map(post => `
            <div class="card post">
                <div class="post-header">
                    <div class="post-avatar">🐾</div>
                    <div>
                        <div class="post-author">${escapeHtml(post.author_email)}</div>
                        <div class="post-date">${formatDate(post.created_at)}</div>
                    </div>
                </div>
                <div class="post-content">${escapeHtml(post.content)}</div>
                ${post.image_url ? `<img class="post-image" src="${escapeHtml(post.image_url)}" alt="">` : ""}
            </div>
        `).join("");
    } catch (err) {
        console.error("Ошибка загрузки постов:", err);
    }
}

async function createPost() {
    const content = document.getElementById("post-content").value.trim();
    if (!content) { alert("Напиши что-нибудь!"); return; }

    const authorId = parseInt(localStorage.getItem("user_id")) || 1;

    try {
        const res = await fetch(`${API}/posts/?author_id=${authorId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content }),
        });
        if (res.ok) {
            document.getElementById("post-content").value = "";
            loadPosts();
        } else {
            const err = await res.json();
            alert(err.detail || "Ошибка");
        }
    } catch (err) {
        alert("Ошибка связи с сервером");
    }
}

// ===== Инициализация =====

document.addEventListener("DOMContentLoaded", () => {
    loadPosts();
});
