// ===== FangUnion — Союз Клыков =====

const API = "http://localhost:8000/api";

// ===== Посты =====

async function loadPosts() {
    try {
        const res = await fetch(`${API}/posts/`);
        const posts = await res.json();
        const container = document.getElementById("posts-container");

        if (posts.length === 0) {
            container.innerHTML = `
                <div class="card">
                    <p style="text-align:center; color: var(--text-light);">
                        Лента пуста. Будь первым товарищем! ☭
                    </p>
                </div>`;
            return;
        }

        container.innerHTML = posts.map(post => `
            <div class="card post">
                <div class="post-header">
                    <div class="post-avatar">🐾</div>
                    <div>
                        <div class="post-author">${escapeHtml(post.author_username)}</div>
                        <div class="post-date">${formatDate(post.created_at)}</div>
                    </div>
                </div>
                <div class="post-content">${escapeHtml(post.content)}</div>
                ${post.image_url ? `<img class="post-image" src="${escapeHtml(post.image_url)}" alt="Изображение">` : ""}
            </div>
        `).join("");
    } catch (err) {
        console.error("Ошибка загрузки постов:", err);
    }
}

async function createPost() {
    const content = document.getElementById("post-content").value.trim();
    if (!content) {
        alert("Напиши что-нибудь, товарищ!");
        return;
    }

    // TODO: заменить на реальный user_id из сессии
    const authorId = 1;

    try {
        const res = await fetch(`${API}/posts/?author_id=${authorId}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ content }),
        });
        if (res.ok) {
            document.getElementById("post-content").value = "";
            loadPosts();
        }
    } catch (err) {
        console.error("Ошибка создания поста:", err);
    }
}

// ===== Утилиты =====

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateStr) {
    const d = new Date(dateStr);
    return d.toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
}

// ===== Инициализация =====

document.addEventListener("DOMContentLoaded", () => {
    loadPosts();
});
