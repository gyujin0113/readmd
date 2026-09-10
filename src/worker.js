// http → https, www → apex 강제 전환 + HSTS. 나머지는 정적 자산(public/) 그대로 서빙.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.protocol === 'http:' || url.hostname === 'www.readmd.kr') {
      url.protocol = 'https:';
      if (url.hostname === 'www.readmd.kr') url.hostname = 'readmd.kr';
      return Response.redirect(url.toString(), 301);
    }
    const res = await env.ASSETS.fetch(request);
    const headers = new Headers(res.headers);
    headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers });
  },
};
