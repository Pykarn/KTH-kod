(function() {
function update(a, b) { for (var p in b) { a[p] = b[p] } }
window.$kundo_chat = window.$kundo_chat || {};
window.$kundo_chat.flows = window.$kundo_chat.flows || {};
window.$kundo_chat.custom_texts = window.$kundo_chat.custom_texts||{};
update(window.$kundo_chat, {
  "DEFAULT_AVATAR_URL": "https://static.kundo.se/static/images/avatar-default.svg",
  "HOST_URL": "https://chat.kundo.se",
  "ORG_HUB_URL": "https://org-{org_id}.chat.kundo.se",
  "SENTRY_ENVIRONMENT": "production",
  "SENTRY_PUBLIC_DSN": "https://e89bf43ec165bdbb899f988407e7fbd4@sentry.kundo.se/4508251915944016",
  "SENTRY_RELEASE": "534dbb061c06ad90824f6fa410cc5b8cfe37294c",
  "STATIC_URL": "https://static-chat.kundo.se/static",
  "_tmpOrgId": 1199,
  "org": 1199
});
update(window.$kundo_chat.custom_texts, {
  "CLOSE_TEXT": "St\u00e4ng",
  "CONTINUE_TEXT": "Forts\u00e4tt",
  "LOAD_TEXT_DEFAULT": "",
  "SELECT_FLOW_TEXT_DEFAULT": "V\u00e4lkommen! St\u00e4ll g\u00e4rna en fr\u00e5ga till oss.\r<br>Welcome! Chat with us here.",
  "START_TEXT_DEFAULT": "Chatta med oss"
});
}());

function loadWidgetScript() {
  

var script = document.createElement('script');
script.charset = "utf-8";
script.async = false; // important: we want to execute translations first

  script.src = "https://static-chat.kundo.se/static/widget.d63a3409478d.js";

var firstScript = document.scripts[0];
firstScript.parentNode.insertBefore(script, firstScript);

  
var link = document.createElement("link");
link.rel = "stylesheet"

  link.href = "https://static-chat.kundo.se/static/widget.1c6faca249d3.css";


var firstHead = document.head || document.getElementsByTagName('head')[0];
firstHead.appendChild(link);

}

if (document.readyState !== 'loading') {
  loadWidgetScript()
} else {
  document.addEventListener('DOMContentLoaded', loadWidgetScript)
}
