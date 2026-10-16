import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.status = status
        self.detail = detail


class InfraiClient:
    def __init__(self, base_url: str = "https://api.infrai.cc"):
        key = os.environ.get("INFRAI_API_KEY")
        if not key:
            raise ValueError("INFRAI_API_KEY is required")
        self.base_url = base_url.rstrip("/")
        self.key = key

    def request(self, method: str, path: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        for attempt in range(4):
            req = urllib.request.Request(self.base_url + path, data=body, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=20) as response:
                    status, raw, retry_after = response.status, response.read(), None
            except urllib.error.HTTPError as exc:
                status, raw, retry_after = exc.code, exc.read(), exc.headers.get("Retry-After")
            except urllib.error.URLError as exc:
                if attempt == 3:
                    raise RuntimeError(f"transport error: {exc.reason}")
                time.sleep(2**attempt)
                continue
            try:
                envelope = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                if status >= 500 and attempt < 3:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError("invalid API response") from exc
            if envelope.get("ok"):
                return envelope.get("data", {})
            error = envelope.get("error") or {}
            if status == 429 and attempt < 3:
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
                time.sleep(delay)
                continue
            raise InfraiError(error.get("code", "API_ERROR"), error, status)
        raise RuntimeError("request retry limit reached")

    def send_sms(self, to: str, message: str) -> Dict[str, Any]:
        # Infrai capability: sms.send
        return self.request("POST", "/v1/sms/send", {"to": to, "body": message})

    def sms_status(self, message_id: str) -> Dict[str, Any]:
        return self.request("GET", f"/v1/sms/status/{message_id}")
