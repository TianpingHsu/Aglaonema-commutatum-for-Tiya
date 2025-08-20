#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天气查询脚本（基于高德地图 Web 服务 API）
"""

import argparse
import json
import sys
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

API_BASE = "https://restapi.amap.com/v3/weather/weatherInfo"


class WeatherError(Exception):
    """自定义天气查询异常"""
    pass


def build_url(city: str, key: str, extensions: str = "base", output: str = "JSON") -> str:
    """构造请求 URL"""
    params = {
        "city": city,
        "key": key,
        "extensions": extensions,
        "output": output
    }
    return f"{API_BASE}?{urlencode(params)}"


def fetch(url: str, timeout: int = 10) -> dict:
    """发起 HTTP GET 请求并返回 JSON"""
    try:
        with urlopen(Request(url, headers={"User-Agent": "weather-cli/1.0"}), timeout=timeout) as resp:
            if resp.status != 200:
                raise WeatherError(f"HTTP {resp.status} {resp.reason}")
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("status") != "1":
                raise WeatherError(f"API 返回错误：{data.get('info')}（{data.get('infocode')}）")
            return data
    except (URLError, HTTPError) as e:
        raise WeatherError(f"网络错误：{e}")


def format_live(live: dict) -> str:
    """格式化实况天气"""
    return (
        f"城市：{live['province']}·{live['city']}\n"
        f"天气：{live['weather']}\n"
        f"温度：{live['temperature']}°C\n"
        f"风向：{live['winddirection']} {live['windpower']}级\n"
        f"湿度：{live['humidity']}%\n"
        f"发布时间：{live['reporttime']}"
    )


def format_forecast(forecast: dict) -> str:
    """格式化预报天气"""
    lines = [f"城市：{forecast['province']}·{forecast['city']}  发布时间：{forecast['reporttime']}\n"]
    for cast in forecast["casts"]:
        lines.append(
            f"{cast['date']}（{cast['week']}） "
            f"{cast['dayweather']}→{cast['nightweather']}  "
            f"{cast['daytemp']}°C / {cast['nighttemp']}°C  "
            f"{cast['daywind']}{cast['daypower']}级"
        )
    return "\n".join(lines)


def main():
    try:
        key = "a945b2eade3beb81a4a4d5eac268ef78"
        city = "330110"
        url = build_url(city, key, "base", "JSON")
        data = fetch(url)
        print(data)
        print(format_live(data["lives"][0]))
    except WeatherError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()