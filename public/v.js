// 신규/재방문 집계: ID 없이 "마지막 방문일"(KST 날짜) 하나만 localStorage에 기억하고, 하루 한 번 서버에 알림.
(function () {
  var KEY = 'readmd.lastVisit';
  try {
    var today = new Date(Date.now() + 9 * 3600 * 1000).toISOString().slice(0, 10);
    var last = localStorage.getItem(KEY) || '';
    if (last === today) return;
    localStorage.setItem(KEY, today);
    if (localStorage.getItem(KEY) !== today) return; // 저장이 안 되는 환경이면 매번 "첫 방문"이 되므로 보내지 않음
    var body = JSON.stringify({ last: last });
    if (!(navigator.sendBeacon && navigator.sendBeacon('/api/v', new Blob([body], { type: 'application/json' })))) {
      fetch('/api/v', { method: 'POST', body: body, headers: { 'content-type': 'application/json' }, keepalive: true }).catch(function () {});
    }
  } catch (e) {}
})();
