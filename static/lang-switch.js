/**
 * 中英切换增强:切换时优先映射到对方语言的同路径页面,页面不存在则回退对方首页。
 * Material 的 alternate 下拉默认使用 mkdocs.yml 里配置的静态链接,本脚本按需改写 href。
 * - /zh/<path> ↔ /en/<path> 同路径映射
 * - Skills 详情页(/zh/skills/*)英文站没有,保持跳转对方首页
 */
(function () {
  function init() {
    var links = document.querySelectorAll(".md-select__link[hreflang]");
    if (!links.length) return;
    var m = location.pathname.match(/^\/(zh|en)\/(.*)$/);
    if (!m) return; // 根路径跳转页无需处理
    var cur = m[1];
    var rest = m[2];
    Array.prototype.forEach.call(links, function (a) {
      var lang = a.getAttribute("hreflang");
      if (!lang || lang === cur) return;
      var fallback = a.getAttribute("href") || "/" + lang + "/";
      if (!rest || rest.indexOf("skills/") === 0) {
        a.setAttribute("href", fallback);
        return;
      }
      var candidate = "/" + lang + "/" + rest;
      fetch(candidate, { method: "HEAD" }).then(function (r) {
        if (r.ok) a.setAttribute("href", candidate);
      }).catch(function () {});
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
