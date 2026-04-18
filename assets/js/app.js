/* ============================================
   Business PT Notes - SPA router
   ============================================ */

// 강의 목차 데이터 - 자료가 추가되면 이곳을 업데이트합니다.
// sections: 사이드바에 표시될 섹션 구조.
// items.file: content/ 폴더 내부의 HTML 파일 경로(상대).
const TOC = {
  lastUpdated: "2026-04-18",
  sections: [
    {
      heading: "시작하기",
      items: [
        { id: "home", title: "홈", file: null }, // null = placeholder
        { id: "about", title: "아카이브 소개", file: "content/about.html" },
      ],
    },
    {
      heading: "정리 문서",
      items: [
        { id: "my-framework", title: "내 관점의 전체 프레임", file: "content/my-framework.html" },
        { id: "glossary", title: "용어 정리", file: "content/glossary.html" },
        { id: "topic-system", title: "주제 시스템 (AI · 책)", file: "content/topic-system.html" },
      ],
    },
    {
      heading: "강의 정리",
      items: [
        { id: "lecture-1", title: "1강 · 비즈니스PT 종합 정리 (1주차)", file: "content/lecture-1.html" },
      ],
    },
    {
      heading: "도구",
      items: [
        { id: "traffic-calculator", title: "트래픽 계산기", file: "content/traffic-calculator.html" },
      ],
    },
  ],
};

/* ============================================
   DOM helpers
   ============================================ */

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/* ============================================
   Navigation rendering
   ============================================ */

function renderNav() {
  const nav = $("#nav");
  const fragments = TOC.sections.map((section) => {
    const items = section.items.length
      ? section.items
          .map(
            (item) =>
              `<a class="nav__item" href="#${item.id}" data-id="${item.id}">${escapeHtml(
                item.title
              )}</a>`
          )
          .join("")
      : `<div class="nav__item" style="color: var(--text-3); font-style: italic; cursor: default;">자료 준비 중...</div>`;
    return `
      <div class="nav__section">
        <div class="nav__heading">${escapeHtml(section.heading)}</div>
        ${items}
      </div>
    `;
  });
  nav.innerHTML = fragments.join("");

  $("#lastUpdated").textContent = TOC.lastUpdated;

  // Click handlers
  $$(".nav__item[data-id]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      const id = el.dataset.id;
      navigate(id);
      // Close sidebar on mobile
      if (window.innerWidth <= 900) {
        $("#sidebar").classList.remove("is-open");
      }
    });
  });
}

/* ============================================
   Router
   ============================================ */

function findItem(id) {
  for (const s of TOC.sections) {
    for (const it of s.items) {
      if (it.id === id) return { section: s, item: it };
    }
  }
  return null;
}

async function navigate(id) {
  const match = findItem(id) || findItem("home");
  if (!match) return;

  // Update active nav
  $$(".nav__item").forEach((el) => el.classList.remove("is-active"));
  const activeEl = $(`.nav__item[data-id="${match.item.id}"]`);
  if (activeEl) activeEl.classList.add("is-active");

  // Update breadcrumb
  const bc = $("#breadcrumb");
  bc.innerHTML = `${escapeHtml(match.section.heading)} <span style="color: var(--text-3); margin: 0 6px;">›</span> <strong>${escapeHtml(
    match.item.title
  )}</strong>`;

  // Update URL hash without page jump
  if (location.hash !== `#${match.item.id}`) {
    history.replaceState(null, "", `#${match.item.id}`);
  }

  // Load content
  const content = $("#content");
  if (match.item.file) {
    try {
      content.innerHTML = `<div class="empty"><div class="empty__icon">⏳</div>불러오는 중...</div>`;
      const res = await fetch(match.item.file);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const html = await res.text();
      content.innerHTML = html;
      content.scrollTop = 0;
      window.scrollTo({ top: 0, behavior: "instant" });
    } catch (err) {
      content.innerHTML = `
        <div class="warn-card">
          <h3>콘텐츠를 불러올 수 없습니다</h3>
          <p>파일을 찾지 못했거나 접근할 수 없습니다: <code>${escapeHtml(match.item.file)}</code></p>
          <p style="color: var(--text-3); font-size: 12px; margin-top: 8px;">
            (참고: 일부 브라우저는 <code>file://</code>에서 fetch를 차단합니다.
            로컬 서버로 열거나 <code>python -m http.server</code> 등을 사용해보세요.)
          </p>
        </div>`;
    }
  } else {
    // Home / placeholder
    content.innerHTML = homeHtml();
  }
}

function homeHtml() {
  // "시작하기" 외 섹션을 모두 강의 섹션으로 간주
  const lectureSections = TOC.sections.filter((s) => s.heading !== "시작하기");
  const lectureItems = lectureSections.flatMap((s) => s.items);
  const hasLectures = lectureItems.length > 0;

  const lectureCards = hasLectures
    ? `<div class="cards-grid">${lectureItems
        .map(
          (it) =>
            `<a class="card" href="#${it.id}" onclick="event.preventDefault(); navigate('${it.id}');">
              <div class="card__title">${escapeHtml(it.title)}</div>
              <div class="card__desc">자세히 보기 →</div>
            </a>`
        )
        .join("")}</div>`
    : `<div class="info-card">
        <h3>강의 자료가 아직 없습니다</h3>
        <p>자료가 추가되면 이곳에 강의 목록이 표시됩니다.</p>
      </div>`;

  return `
    <article class="placeholder">
      <h1>비지니스 PT 강의 정리</h1>
      <p class="lead">강의에서 배운 내용을 주제별로 구조화하여 정리하는 아카이브입니다.</p>

      <h2 style="border: none; padding: 0; margin-top: 28px;">강의 목록</h2>
      ${lectureCards}

      <h2>사용 안내</h2>
      <div class="info-card">
        <h3>이용 방법</h3>
        <ul>
          <li>왼쪽 <strong>사이드바</strong>에서 주제를 선택하면 해당 강의 내용을 볼 수 있습니다.</li>
          <li>상단 <strong>검색창</strong>에서 키워드로 현재 페이지 내용을 빠르게 필터링할 수 있습니다.</li>
          <li>원본 자료는 <code>raw/</code> 폴더에, 정리된 내용은 <code>content/</code> 폴더에 보관됩니다.</li>
        </ul>
      </div>

      <h2>자료 반영 방법</h2>
      <p>강의 노트, 채팅 로그, 개인 메모 등을 <code>C:\\Dev\\bizpt\\raw\\</code> 폴더에 넣거나 채팅으로 전달해주시면 주제별로 구조화하여 이 아카이브에 반영합니다.</p>
    </article>`;
}

/* ============================================
   Search (현재 페이지 내 하이라이트)
   ============================================ */

function setupSearch() {
  const input = $("#searchInput");
  input.addEventListener("input", (e) => {
    const q = e.target.value.trim();
    clearHighlights();
    if (q.length >= 2) highlightInContent(q);
  });
}

function clearHighlights() {
  $$(".search-hit").forEach((el) => {
    const parent = el.parentNode;
    parent.replaceChild(document.createTextNode(el.textContent), el);
    parent.normalize();
  });
}

function highlightInContent(query) {
  const content = $("#content");
  const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
    acceptNode: (node) => {
      if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
      if (node.parentElement.closest("script, style")) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    },
  });
  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);

  const re = new RegExp(escapeRegExp(query), "gi");
  nodes.forEach((node) => {
    const text = node.nodeValue;
    if (!re.test(text)) return;
    re.lastIndex = 0;
    const frag = document.createDocumentFragment();
    let lastIdx = 0;
    let m;
    while ((m = re.exec(text)) !== null) {
      if (m.index > lastIdx) frag.appendChild(document.createTextNode(text.slice(lastIdx, m.index)));
      const mark = document.createElement("span");
      mark.className = "search-hit";
      mark.textContent = m[0];
      frag.appendChild(mark);
      lastIdx = m.index + m[0].length;
    }
    if (lastIdx < text.length) frag.appendChild(document.createTextNode(text.slice(lastIdx)));
    node.parentNode.replaceChild(frag, node);
  });
}

/* ============================================
   Mobile sidebar
   ============================================ */

function setupSidebarToggle() {
  $("#menuToggle").addEventListener("click", () => {
    $("#sidebar").classList.toggle("is-open");
  });
  $("#sidebarToggle").addEventListener("click", () => {
    $("#sidebar").classList.remove("is-open");
  });
}

/* ============================================
   Utils
   ============================================ */

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}
function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Expose for inline onclick in homeHtml
window.navigate = navigate;

/* ============================================
   Boot
   ============================================ */

document.addEventListener("DOMContentLoaded", () => {
  renderNav();
  setupSidebarToggle();
  setupSearch();

  const hash = location.hash.replace("#", "") || "home";
  navigate(hash);

  window.addEventListener("hashchange", () => {
    const id = location.hash.replace("#", "") || "home";
    navigate(id);
  });
});
