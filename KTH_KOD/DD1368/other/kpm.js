(function (js, css, url) {
  if (window.frameElement) {
    return;
  }
  let lang = document.documentElement.lang.startsWith("sv") ? "sv" : "en";
  // Hostnames can be found in panes/utils.ts
  const refPrefix =
    location.hostname.includes("-r.referens.sys") ||
    location.hostname.includes("kth.test.instructure") ||
    location.hostname === "localhost"
      ? "-r.referens.sys"
      : "";
  let links = [
    {
      className: "external",
      hostname: `https://www${refPrefix}.kth.se`,
      path: lang === "en" ? "/en" : "",
      label: "kth.se",
    },
    {
      className: "student-web",
      hostname: `https://www${refPrefix}.kth.se`,
      path: lang === "en" ? "/en/student" : "/student",
      label: lang === "en" ? "Student web" : "Studentwebben",
    },
    {
      className: "intranet",
      hostname: `https://intra${refPrefix}.kth.se`,
      path: lang === "en" ? "/en" : "",
      label: lang === "en" ? "Intranet" : "Intranät",
    },
  ];

  let lbls = {
    w: lang === "en" ? "Websites" : "Webbplatser",
    l: lang === "en" ? "Login" : "Logga in",
  };

  let cr = (t) => document.createElement(t);
  let root = document.querySelector(".kth-kpm");
  if (!root) {
    // <div id="kpm-6cf53" style="pointer-events: all"...>
    root = cr("div");
    root.classList.add("kth-kpm");
    document.body.style.setProperty("--kpm-bar-height", "2.5rem");
    document.body.classList.add("use-personal-menu");
    document.body.prepend(root);
  }

  root.id = "kpm-6cf53";
  let st = cr("link");
  st.rel = "stylesheet";
  st.href = css;
  document.head.appendChild(st);

  let s = root.style;
  s.pointerEvents = "all";
  s.inset = "0";
  s.position = "fixed";
  s.height = "2.5rem";

  let header = document.querySelector(".kth-header");
  let lis = links
    .map((link) => {
      let c = header?.classList.contains(link.className)
        ? "aria-current='true'"
        : "";

      return `<li><a href=${
        link.hostname + link.path
      } ${c} class="kth-menu-item">${link.label}</a></li>`;
    })
    .join("");

  let lis2 = links
    .map((link) => {
      return `<li><a href=${link.hostname + link.path}>${link.label}</a></li>`;
    })
    .join("");

  let login = `<a class="kth-menu-item kpm-login" href="${url}?nextUrl=${location.href}">${lbls.l}</a>`;
  let currentItem = links.find((link) =>
    header?.classList.contains(link.className)
  );
  let currentLabel = currentItem?.label ?? links[0].label;

  root.innerHTML = `
    <div class="kth-kpm__container kpm-logged-out">
    <nav class="kth-entrances-expandable kpm-entrances-expandable" aria-label="${lbls.w}">
    <button class="kth-menu-item dropdown" aria-expanded="false" aria-controls="kpm-6cf53-entrances">${currentLabel}</button>
    <div class="kpm-mini-dialog" id="kpm-6cf53-entrances"><ul>${lis2}</ul></div>
    </nav>
    <nav class="kpm-entrances kth-entrances" aria-label="${lbls.w}">
    <ul>${lis}</ul>
    </nav>
    ${login}
    </div>
  `;

  let btn = document.querySelector(
    "button[aria-controls='kpm-6cf53-entrances']"
  );
  btn.addEventListener("click", () => {
    btn.ariaExpanded = btn.ariaExpanded === "false" ? "true" : "false";
  });
})("https://app.kth.se/kpm/assets/index.a50c5c3d.js", "https://app.kth.se/kpm/assets/index.cc18ecff.css", "https://app.kth.se/kpm/auth/login");
