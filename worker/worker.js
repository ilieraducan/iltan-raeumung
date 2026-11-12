// Cloudflare Worker: Iltan Räumung – Raumscan
// Receives 1–6 JPEG frames from the /scan/ page, asks Claude for a volume estimate, returns JSON.
// Secrets/vars (set in Cloudflare dashboard → Worker → Settings → Variables):
//   ANTHROPIC_API_KEY  (secret, required)
//   MODEL              (optional, default below)
//   DAILY_LIMIT        (optional, default 8 estimates per IP per day)
// Binding: KV namespace "RL" (for the per-IP daily limit).

const DEFAULT_MODEL = 'claude-sonnet-5-5';
const ALLOWED = ['https://iltan-raeumung.de', 'https://www.iltan-raeumung.de'];
const LANGS = { de: 'German', ru: 'Russian', ro: 'Romanian' };

function cors(origin) {
  const ok = ALLOWED.includes(origin) || /^http:\/\/localhost(:\d+)?$/.test(origin || '');
  return {
    'Access-Control-Allow-Origin': ok ? origin : ALLOWED[0],
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Vary': 'Origin',
  };
}
const json = (obj, status, origin) =>
  new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', ...cors(origin) } });

function prompt(lang, area, floor) {
  const L = LANGS[lang] || 'German';
  return [
    'You are an estimator for a German house-clearance company (Entrümpelung). The images are frames from one short phone video (or photos) of rooms to be cleared.',
    'Identify every piece of furniture, appliance and clutter that would have to be carried out. Group identical items. Estimate the loaded transport volume in cubic metres for each item (disassembled where usual, e.g. wardrobe ~1.2–2 m³, double bed ~1.5 m³, 3-seat sofa ~1.5 m³, fridge ~0.6 m³, moving box ~0.06 m³).',
    'Also estimate loose clutter (bags, piles, small items) as one number. Do not double-count items visible in several frames.',
    'Estimate the floor area of the room(s) shown as a range.' + (area ? ` The customer says the area is about ${area} m²; use it.` : ''),
    `Floor without elevator: ${floor}.`,
    `Write all names, questions and the note in ${L}. Ask 1–3 short follow-up questions only if they change the estimate.`,
    'If the images do not show rooms or furniture, return an empty items list and explain in the note.',
    'Reply with only JSON of this shape, nothing else:',
    '{"room":"…","area_min":18,"area_max":22,"confidence":"low|medium|high","items":[{"name":"…","count":1,"m3_each":1.6}],"clutter_m3":1.0,"questions":["…"],"note":"…"}',
  ].join('\n');
}

function parseJSON(text) {
  try { return JSON.parse(text); } catch (_) {}
  const m = text.match(/```(?:json)?\s*([\s\S]*?)```/); if (m) { try { return JSON.parse(m[1]); } catch (_) {} }
  const a = text.indexOf('{'), b = text.lastIndexOf('}');
  if (a >= 0 && b > a) { try { return JSON.parse(text.slice(a, b + 1)); } catch (_) {} }
  return null;
}

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors(origin) });
    const url = new URL(req.url);
    if (req.method !== 'POST' || url.pathname !== '/estimate') return json({ error: 'not_found' }, 404, origin);
    if (!env.ANTHROPIC_API_KEY) return json({ error: 'not_configured' }, 500, origin);

    // per-IP daily limit
    const ip = req.headers.get('CF-Connecting-IP') || 'unknown';
    const day = new Date().toISOString().slice(0, 10);
    const key = `rl:${day}:${ip}`;
    const limit = Number(env.DAILY_LIMIT || 8);
    if (env.RL) {
      const used = Number((await env.RL.get(key)) || 0);
      if (used >= limit) return json({ error: 'limit' }, 429, origin);
      await env.RL.put(key, String(used + 1), { expirationTtl: 60 * 60 * 26 });
    }

    let body;
    try { body = await req.json(); } catch (_) { return json({ error: 'bad_request' }, 400, origin); }
    const imgs = Array.isArray(body.images) ? body.images.slice(0, 6) : [];
    if (!imgs.length) return json({ error: 'no_images' }, 400, origin);
    for (const b64 of imgs) {
      if (typeof b64 !== 'string' || b64.length > 2_000_000) return json({ error: 'image_too_large' }, 413, origin);
    }
    const lang = LANGS[body.lang] ? body.lang : 'de';
    const area = Number(body.area) > 0 && Number(body.area) < 1000 ? Math.round(Number(body.area)) : 0;
    const floor = String(body.floor || 'ground floor / elevator').slice(0, 60);

    const content = imgs.map((data) => ({ type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data } }));
    content.push({ type: 'text', text: prompt(lang, area, floor) });

    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
      body: JSON.stringify({ model: env.MODEL || DEFAULT_MODEL, max_tokens: 1500, messages: [{ role: 'user', content }] }),
    });
    if (!r.ok) return json({ error: 'ai_error', status: r.status }, 502, origin);
    const out = await r.json();
    const text = (out.content || []).filter((c) => c.type === 'text').map((c) => c.text).join('');
    const data = parseJSON(text);
    if (!data || !Array.isArray(data.items)) return json({ error: 'ai_format' }, 502, origin);
    // Images are not stored anywhere: they exist only in this request.
    return json(data, 200, origin);
  },
};
