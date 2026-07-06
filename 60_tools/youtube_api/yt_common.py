# -*- coding: utf-8 -*-
"""YouTube Data API v3 공통 모듈 — 키 로딩(.env)·호출·24h 캐시·실행 로그·쿼터 계측
표준 라이브러리만 사용(외부 의존성 0). 키는 절대 출력·커밋하지 않는다.
"""
import os, sys, json, time, hashlib, io, datetime, urllib.request, urllib.parse

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_logs", "run.log")
API_BASE = "https://www.googleapis.com/youtube/v3/"
CACHE_TTL = 24 * 3600  # 동일 요청 24h 내 재호출 금지
COST = {"search": 100, "videos": 1, "channels": 1, "commentThreads": 1}

# Windows 콘솔 cp949 대비
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_api_key():
    """YOUTUBE_API_KEY — 환경변수 우선, 없으면 저장소 루트 .env 파싱."""
    key = os.environ.get("YOUTUBE_API_KEY")
    if key:
        return key.strip()
    env = os.path.join(ROOT, ".env")
    if os.path.exists(env):
        for line in io.open(env, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line.startswith("YOUTUBE_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _log(msg):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    io.open(LOG_FILE, "a", encoding="utf-8").write(f"[{ts}] {msg}\n")


def call(endpoint, params, use_cache=True):
    """API 호출 + 캐시 + 로그. 반환: (json dict, 쿼터 비용, 캐시 여부)"""
    key = load_api_key()
    if not key:
        print("오류: YOUTUBE_API_KEY 없음 — .env 또는 환경변수에 설정하세요 (README 참조).")
        sys.exit(2)
    q = dict(params)
    cache_id = hashlib.sha1((endpoint + json.dumps(q, sort_keys=True, ensure_ascii=False)).encode("utf-8")).hexdigest()[:16]
    cpath = os.path.join(CACHE_DIR, f"{endpoint}_{cache_id}.json")
    if use_cache and os.path.exists(cpath) and time.time() - os.path.getmtime(cpath) < CACHE_TTL:
        _log(f"CACHE {endpoint} {q.get('q', q.get('id', ''))!r} (비용 0)")
        return json.load(io.open(cpath, encoding="utf-8")), 0, True
    q["key"] = key
    url = API_BASE + endpoint + "?" + urllib.parse.urlencode(q, doseq=True)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:400]
        _log(f"ERROR {endpoint} HTTP {e.code}: {body}")
        print(f"API 오류 HTTP {e.code}: {body}")
        sys.exit(1)
    os.makedirs(CACHE_DIR, exist_ok=True)
    json.dump(data, io.open(cpath, "w", encoding="utf-8"), ensure_ascii=False)
    cost = COST.get(endpoint, 1)
    _log(f"CALL {endpoint} {q.get('q', q.get('id', ''))!r} (비용 {cost})")
    return data, cost, False


def iso_dur_to_min(d):
    """PT13M4S → '13:04'"""
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return d or ""
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return (f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}")


def out_path(*parts):
    p = os.path.join(ROOT, *parts)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p
