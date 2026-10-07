(() => {
  if (window.__siteVisitBeaconInstalled) return;
  window.__siteVisitBeaconInstalled = true;
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1" || navigator.webdriver) return;

  const body = JSON.stringify({path: window.location.pathname || "/"});
  fetch("https://events.transduction.systems/api/analytics/pageview", {
    method: "POST",
    mode: "cors",
    credentials: "omit",
    keepalive: true,
    referrerPolicy: "origin",
    headers: {"Content-Type": "text/plain;charset=UTF-8"},
    body
  }).catch(() => {});
})();
