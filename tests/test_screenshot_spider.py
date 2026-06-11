import json
import os
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from advertools import cli
from advertools import screenshot_spider as ss


def _command_value(command, name):
    prefix = name + "="
    for part in command:
        if part.startswith(prefix):
            return part[len(prefix) :]
    raise AssertionError(f"{name!r} not found in command: {command}")


def _json_arg_file(command, name):
    path = Path(_command_value(command, name))
    assert path.exists()
    return path


class _ScreenshotTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/robots.txt":
            self.send_response(404)
            self.end_headers()
            return
        if self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/target")
            self.end_headers()
            return
        if self.path == "/missing":
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><main id='ready'>missing</main></body></html>"
            )
            return
        if self.path == "/slow":
            time.sleep(1)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        body = b"""
        <html>
          <head><title>Screenshot fixture</title></head>
          <body style='min-height: 1400px'>
            <main id='ready'>ready</main>
          </body>
        </html>
        """
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


@pytest.fixture
def local_http_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _ScreenshotTestHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_crawl_screenshots_raises_on_wrong_file_extension():
    with pytest.raises(ValueError):
        ss.crawl_screenshots("https://example.com", "myfile.wrong")


@pytest.mark.parametrize(
    "url_list, match",
    [
        ([], "at least one"),
        (["https://example.com", 1], "index 1"),
        ([""], "index 0"),
        (["file:///tmp/example.html"], "http:// or https://"),
        (["ftp://example.com/file"], "http:// or https://"),
        (["example.com/path"], "http:// or https://"),
    ],
)
def test_crawl_screenshots_rejects_invalid_urls(url_list, match):
    with pytest.raises((TypeError, ValueError), match=match):
        ss.crawl_screenshots(url_list, "output.jl")


@pytest.mark.parametrize("image_type", ["gif", "jpg", "webp", ""])
def test_crawl_screenshots_rejects_invalid_image_type(image_type):
    with pytest.raises(ValueError, match="image_type"):
        ss.crawl_screenshots("https://example.com", "output.jl", image_type=image_type)


def test_crawl_screenshots_rejects_quality_for_png():
    with pytest.raises(ValueError, match="quality"):
        ss.crawl_screenshots("https://example.com", "output.jl", quality=80)


@pytest.mark.parametrize("quality", [-1, 101, 50.5, "80"])
def test_crawl_screenshots_rejects_bad_jpeg_quality(quality):
    with pytest.raises(ValueError, match="quality"):
        ss.crawl_screenshots(
            "https://example.com", "output.jl", image_type="jpeg", quality=quality
        )


@pytest.mark.parametrize("timeout", [-1, "1000", True])
def test_crawl_screenshots_rejects_invalid_timeout(timeout):
    with pytest.raises(ValueError, match="timeout"):
        ss.crawl_screenshots("https://example.com", "output.jl", timeout=timeout)


@pytest.mark.parametrize("wait_for_timeout", [-1, "1000", True])
def test_crawl_screenshots_rejects_invalid_wait_for_timeout(wait_for_timeout):
    with pytest.raises(ValueError, match="wait_for_timeout"):
        ss.crawl_screenshots(
            "https://example.com", "output.jl", wait_for_timeout=wait_for_timeout
        )


@pytest.mark.parametrize(
    "kwargs, match",
    [
        ({"browser_type": "opera"}, "browser_type"),
        ({"context_kwargs": []}, "context_kwargs"),
        ({"launch_options": []}, "launch_options"),
        ({"custom_settings": []}, "custom_settings"),
    ],
)
def test_crawl_screenshots_rejects_invalid_option_types(kwargs, match):
    with pytest.raises((TypeError, ValueError), match=match):
        ss.crawl_screenshots("https://example.com", "output.jl", **kwargs)


def test_screenshot_path_is_unique_and_filesystem_safe(tmp_path):
    urls = [
        "https://www.example.com/a page/?x=1,2",
        "https://www.example.com/a page/?x=3,4",
    ]
    paths = [
        ss._screenshot_path(url, i, str(tmp_path), "Run ID: 1", "png")
        for i, url in enumerate(urls)
    ]
    assert paths[0] != paths[1]
    for path in paths:
        basename = os.path.basename(path)
        assert basename.endswith(".png")
        assert re.match(r"^[a-z0-9._-]+$", basename)
        assert "run-id-1" in basename


def test_normalize_actions_supports_args_kwargs_and_extra_kwargs():
    actions = ss._normalize_actions(
        [
            {"method": "click", "args": ["#accept"], "timeout": 1000},
            {
                "method": "wait_for_selector",
                "args": ["main"],
                "kwargs": {"state": "visible"},
            },
        ]
    )
    assert actions == [
        {"method": "click", "args": ["#accept"], "kwargs": {"timeout": 1000}},
        {
            "method": "wait_for_selector",
            "args": ["main"],
            "kwargs": {"state": "visible"},
        },
    ]


@pytest.mark.parametrize(
    "actions, exc_type",
    [
        ({"method": "click"}, TypeError),
        (["click"], TypeError),
        ([{"args": ["#x"]}], ValueError),
        ([{"method": "click", "args": "#x"}], TypeError),
        ([{"method": "click", "kwargs": []}], TypeError),
        ([{"method": "screenshot"}], ValueError),
    ],
)
def test_normalize_actions_rejects_invalid_actions(actions, exc_type):
    with pytest.raises(exc_type):
        ss._normalize_actions(actions)


def test_crawl_screenshots_reports_missing_optional_dependency(monkeypatch, tmp_path):
    def missing_page_method():
        raise ImportError("missing")

    monkeypatch.setattr(ss, "_load_page_method", missing_page_method)
    with pytest.raises(ImportError, match=r"advertools\[screenshots\]"):
        ss.crawl_screenshots("https://example.com", tmp_path / "output.jl")


def test_crawl_screenshots_reports_unsupported_python(monkeypatch, tmp_path):
    monkeypatch.setattr(ss.sys, "version_info", (3, 9, 0))
    with pytest.raises(ImportError, match="Python >= 3.10"):
        ss.crawl_screenshots("https://example.com", tmp_path / "output.jl")


def test_screenshot_spider_loads_options_and_urls_from_files(tmp_path):
    options = {
        "screenshot_dir": str(tmp_path),
        "run_id": "run",
        "full_page": True,
        "image_type": "png",
        "quality": None,
        "wait_until": "load",
        "wait_for_timeout": None,
        "timeout": None,
        "actions": [],
        "context_kwargs": {},
    }
    options_file = tmp_path / "options.json"
    urls_file = tmp_path / "urls.json"
    options_file.write_text(json.dumps(options))
    urls_file.write_text(json.dumps(["https://example.com"]))

    spider = ss.ScreenshotSpider(
        url_list_file=str(urls_file),
        screenshot_options_file=str(options_file),
    )

    assert spider.start_urls == ["https://example.com"]
    assert spider.screenshot_options == options


def test_crawl_screenshots_prepares_filesystem_and_replaces_output(
    monkeypatch, tmp_path
):
    commands = []

    def fake_run(command, **kwargs):
        commands.append((command, kwargs))

    monkeypatch.setattr(ss, "_check_screenshot_dependencies", lambda: None)
    monkeypatch.setattr(ss.subprocess, "run", fake_run)

    output_file = tmp_path / "nested" / "output.jl"
    screenshot_dir = tmp_path / "shots"
    output_file.parent.mkdir()
    output_file.write_text("old data")

    ss.crawl_screenshots(
        "https://example.com/a,b?x=1",
        output_file,
        screenshot_dir=screenshot_dir,
    )

    assert screenshot_dir.is_dir()
    assert output_file.parent.is_dir()
    assert not output_file.exists()
    assert len(commands) == 1


def test_crawl_screenshots_rejects_screenshot_dir_file(monkeypatch, tmp_path):
    monkeypatch.setattr(ss, "_check_screenshot_dependencies", lambda: None)
    screenshot_dir = tmp_path / "shots"
    screenshot_dir.write_text("not a directory")
    with pytest.raises(ValueError, match="screenshot_dir"):
        ss.crawl_screenshots(
            "https://example.com",
            tmp_path / "output.jl",
            screenshot_dir=screenshot_dir,
        )


def test_crawl_screenshots_builds_command_settings_and_temp_files(
    monkeypatch, tmp_path
):
    commands = []
    files_seen = []

    def fake_run(command, **kwargs):
        commands.append((command, kwargs))
        url_file = _json_arg_file(command, "url_list_file")
        options_file = _json_arg_file(command, "screenshot_options_file")
        files_seen.extend([url_file, options_file])
        assert json.loads(url_file.read_text()) == [
            "https://example.com/a,b?x=1",
            "https://example.com/other",
        ]
        options = json.loads(options_file.read_text())
        assert options["run_id"] == "test-run"
        assert options["image_type"] == "jpeg"
        assert options["quality"] == 80
        assert options["wait_until"] == "networkidle"
        assert options["wait_for_timeout"] == 500
        assert options["timeout"] == 10000
        assert options["actions"][0]["method"] == "click"
        assert options["context_kwargs"]["viewport"]["width"] == 390

    monkeypatch.setattr(ss, "_check_screenshot_dependencies", lambda: None)
    monkeypatch.setattr(ss.subprocess, "run", fake_run)

    output_file = tmp_path / "output.jl"
    screenshot_dir = tmp_path / "shots"
    ss.crawl_screenshots(
        ["https://example.com/a,b?x=1", "https://example.com/other"],
        output_file,
        screenshot_dir=screenshot_dir,
        image_type="jpeg",
        quality=80,
        wait_until="networkidle",
        wait_for_timeout=500,
        timeout=10000,
        actions=[{"method": "click", "args": ["#accept"]}],
        browser_type="firefox",
        launch_options={"timeout": 10000},
        context_kwargs={"viewport": {"width": 390, "height": 844}},
        custom_settings={"LOG_FILE": "screenshots.log", "CONCURRENT_REQUESTS": 1},
        run_id="test run",
    )

    assert screenshot_dir.is_dir()
    assert len(commands) == 1
    command, kwargs = commands[0]
    assert command[:4] == [sys.executable, "-m", "scrapy", "runspider"]
    assert command[4] == ss.screenshot_spider_path
    assert kwargs == {"check": True}
    assert "LOG_FILE=screenshots.log" in command
    assert "CONCURRENT_REQUESTS=1" in command
    assert "PLAYWRIGHT_BROWSER_TYPE=firefox" in command
    assert "PLAYWRIGHT_MAX_PAGES_PER_CONTEXT=4" in command
    assert any(part.startswith("PLAYWRIGHT_LAUNCH_OPTIONS=") for part in command)
    assert files_seen
    assert all(not path.exists() for path in files_seen)


def test_crawl_screenshots_cleans_temp_files_on_subprocess_failure(
    monkeypatch, tmp_path
):
    files_seen = []

    def fake_run(command, **kwargs):
        files_seen.extend(
            [
                _json_arg_file(command, "url_list_file"),
                _json_arg_file(command, "screenshot_options_file"),
            ]
        )
        raise subprocess.CalledProcessError(returncode=9, cmd=command)

    monkeypatch.setattr(ss, "_check_screenshot_dependencies", lambda: None)
    monkeypatch.setattr(ss.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="playwright install chromium"):
        ss.crawl_screenshots(
            "https://example.com",
            tmp_path / "output.jl",
            screenshot_dir=tmp_path / "shots",
        )

    assert files_seen
    assert all(not path.exists() for path in files_seen)


def test_screenshot_file_info_reports_success_and_missing(tmp_path):
    screenshot = tmp_path / "shot.png"
    screenshot.write_bytes(b"png")
    assert ss._screenshot_file_info(str(screenshot)) == {
        "screenshot_success": True,
        "screenshot_exists": True,
        "screenshot_size_bytes": 3,
    }
    assert ss._screenshot_file_info(str(tmp_path / "missing.png")) == {
        "screenshot_success": False,
        "screenshot_exists": False,
        "screenshot_size_bytes": 0,
    }


def test_errback_rows_include_structured_error_fields(tmp_path):
    from scrapy import Request
    from twisted.python.failure import Failure

    spider = ss.ScreenshotSpider(
        url_list=json.dumps(["https://example.com"]),
        screenshot_options=json.dumps(
            {
                "screenshot_dir": str(tmp_path),
                "run_id": "run",
                "full_page": True,
                "image_type": "png",
                "quality": None,
                "wait_until": "load",
                "wait_for_timeout": None,
                "timeout": None,
                "actions": [],
                "context_kwargs": {},
            }
        ),
    )
    request = Request(
        "https://example.com",
        meta={
            "screenshot_path": str(tmp_path / "missing.png"),
            "screenshot_type": "png",
            "run_id": "run",
            "screenshot_index": 0,
        },
    )
    failure = Failure(ValueError("boom"))
    failure.request = request

    row = next(spider.errback(failure))

    assert row["error_type"] == "ValueError"
    assert row["error_message"] == "boom"
    assert row["screenshot_success"] is False
    assert row["screenshot_index"] == 0


def test_screenshots_cli_forwards_arguments(monkeypatch):
    captured = {}

    class Tty:
        def isatty(self):
            return True

    def fake_crawl_screenshots(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(cli.sys, "stdin", Tty())
    monkeypatch.setattr(cli.adv, "crawl_screenshots", fake_crawl_screenshots)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "advertools",
            "screenshots",
            "https://example.com",
            "output.jl",
            "--screenshot-dir",
            "shots",
            "--image-type",
            "jpeg",
            "--quality",
            "80",
            "--no-full-page",
            "--wait-until",
            "domcontentloaded",
            "--wait-ms",
            "1000",
            "--timeout-ms",
            "10000",
            "--browser-type",
            "webkit",
            "--actions-json",
            '[{"method": "click", "args": ["#ok"]}]',
            "--launch-options-json",
            '{"timeout": 10000}',
            "--context-kwargs-json",
            '{"viewport": {"width": 390, "height": 844}}',
            "--run-id",
            "cli-run",
            "--custom-settings",
            "LOG_FILE=screen.log",
        ],
    )

    cli.main()

    assert captured["url_list"] == ["https://example.com"]
    assert captured["output_file"] == "output.jl"
    assert captured["screenshot_dir"] == "shots"
    assert captured["image_type"] == "jpeg"
    assert captured["quality"] == 80
    assert captured["full_page"] is False
    assert captured["wait_until"] == "domcontentloaded"
    assert captured["wait_for_timeout"] == 1000
    assert captured["timeout"] == 10000
    assert captured["browser_type"] == "webkit"
    assert captured["actions"][0]["method"] == "click"
    assert captured["launch_options"]["timeout"] == 10000
    assert captured["context_kwargs"]["viewport"]["width"] == 390
    assert captured["run_id"] == "cli-run"
    assert captured["custom_settings"] == {"LOG_FILE": "screen.log"}


def test_screenshots_cli_accepts_json_files(monkeypatch, tmp_path):
    captured = {}
    actions_file = tmp_path / "actions.json"
    context_file = tmp_path / "context.json"
    launch_file = tmp_path / "launch.json"
    actions_file.write_text('[{"method": "wait_for_selector", "args": ["main"]}]')
    context_file.write_text('{"viewport": {"width": 390, "height": 844}}')
    launch_file.write_text('{"headless": true}')

    class Tty:
        def isatty(self):
            return True

    def fake_crawl_screenshots(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(cli.sys, "stdin", Tty())
    monkeypatch.setattr(cli.adv, "crawl_screenshots", fake_crawl_screenshots)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "advertools",
            "screenshots",
            "https://example.com",
            "output.jl",
            "--actions-json",
            "@" + str(actions_file),
            "--context-kwargs-json",
            "@" + str(context_file),
            "--launch-options-json",
            "@" + str(launch_file),
        ],
    )

    cli.main()

    assert captured["actions"][0]["method"] == "wait_for_selector"
    assert captured["context_kwargs"]["viewport"]["height"] == 844
    assert captured["launch_options"] == {"headless": True}


def test_screenshots_cli_prefers_arguments_when_stdin_is_not_tty(monkeypatch):
    captured = {}

    class NonTty:
        def isatty(self):
            return False

        def read(self):
            raise AssertionError("stdin should not be read when URLs are provided")

    def fake_crawl_screenshots(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(cli.sys, "stdin", NonTty())
    monkeypatch.setattr(cli.adv, "crawl_screenshots", fake_crawl_screenshots)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "advertools",
            "screenshots",
            "https://example.com",
            "output.jl",
        ],
    )

    cli.main()

    assert captured["url_list"] == ["https://example.com"]
    assert captured["output_file"] == "output.jl"


def test_screenshots_cli_reads_urls_from_stdin(monkeypatch):
    captured = {}

    class NonTty:
        def isatty(self):
            return False

        def read(self):
            return "https://example.com\nhttps://python.org\n"

    def fake_crawl_screenshots(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(cli.sys, "stdin", NonTty())
    monkeypatch.setattr(cli.adv, "crawl_screenshots", fake_crawl_screenshots)
    monkeypatch.setattr(sys, "argv", ["advertools", "screenshots", "output.jl"])

    cli.main()

    assert captured["url_list"] == ["https://example.com", "https://python.org"]
    assert captured["output_file"] == "output.jl"


@pytest.mark.parametrize(
    "args",
    [
        ["--actions-json", "{bad-json"],
        ["--actions-json", "@missing-file.json"],
    ],
)
def test_screenshots_cli_rejects_invalid_json(monkeypatch, args):
    called = False

    class Tty:
        def isatty(self):
            return True

    def fake_crawl_screenshots(**kwargs):
        nonlocal called
        called = True

    monkeypatch.setattr(cli.sys, "stdin", Tty())
    monkeypatch.setattr(cli.adv, "crawl_screenshots", fake_crawl_screenshots)
    monkeypatch.setattr(
        sys,
        "argv",
        ["advertools", "screenshots", "https://example.com", "output.jl", *args],
    )

    with pytest.raises(SystemExit):
        cli.main()
    assert called is False


@pytest.mark.skipif(
    not os.environ.get("ADV_TEST_SCREENSHOTS"),
    reason="set ADV_TEST_SCREENSHOTS=1 to run browser-based screenshot tests",
)
def test_crawl_screenshots_local_integration(local_http_server, tmp_path):
    pytest.importorskip("scrapy_playwright")
    browsers = os.environ.get("ADV_TEST_SCREENSHOTS_BROWSERS", "chromium").split(",")

    for browser in [browser.strip() for browser in browsers if browser.strip()]:
        output_file = tmp_path / f"screenshots_{browser}.jl"
        screenshot_dir = tmp_path / f"shots_{browser}"

        ss.crawl_screenshots(
            [
                local_http_server + "/",
                local_http_server + "/missing",
                local_http_server + "/redirect",
            ],
            output_file,
            screenshot_dir=screenshot_dir,
            browser_type=browser,
            image_type="jpeg",
            quality=80,
            full_page=False,
            timeout=10000,
            actions=[{"method": "wait_for_selector", "args": ["#ready"]}],
            context_kwargs={"viewport": {"width": 390, "height": 844}},
            custom_settings={"LOG_LEVEL": "ERROR"},
        )

        rows = [json.loads(line) for line in output_file.read_text().splitlines()]
        assert len(rows) == 3
        assert {row["status"] for row in rows} == {200, 404}
        assert any(row["final_url"].endswith("/target") for row in rows)
        for row in rows:
            screenshot_path = Path(row["screenshot_path"])
            assert screenshot_path.exists()
            assert screenshot_path.stat().st_size > 0
            assert row["screenshot_type"] == "jpeg"
            assert row["screenshot_success"] is True
            assert row["screenshot_exists"] is True
            assert row["screenshot_size_bytes"] > 0
            assert row["error_type"] is None
            assert row["screenshot_index"] in [0, 1, 2]


@pytest.mark.skipif(
    not os.environ.get("ADV_TEST_SCREENSHOTS"),
    reason="set ADV_TEST_SCREENSHOTS=1 to run browser-based screenshot tests",
)
def test_crawl_screenshots_timeout_integration(local_http_server, tmp_path):
    pytest.importorskip("scrapy_playwright")
    output_file = tmp_path / "timeout.jl"

    ss.crawl_screenshots(
        local_http_server + "/slow",
        output_file,
        screenshot_dir=tmp_path / "timeout_shots",
        timeout=1,
        custom_settings={"LOG_LEVEL": "ERROR"},
    )

    rows = [json.loads(line) for line in output_file.read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["screenshot_success"] is False
    assert rows[0]["error_type"]
    assert rows[0]["error_message"]
