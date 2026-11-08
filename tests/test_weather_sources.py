import sys
from pathlib import Path
from unittest.mock import Mock
import pytest
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'api'))
import weather_service as weather


def test_offline_weather_is_labeled_as_preset():
    result=weather.get_weather_data(7.45,125.81,api_key='')
    assert result['is_live'] is False
    assert 'preset' in result['source']
    assert result['rainfall_source'] == 'Monthly climate preset'


def test_live_weather_keeps_hourly_rain_separate(monkeypatch):
    response=Mock()
    response.json.return_value={'main':{'temp':28.1,'humidity':77},'rain':{'1h':12},'weather':[{'description':'rain','icon':'10d'}]}
    monkeypatch.setattr(weather.requests,'get',lambda *a,**k:response)
    result=weather.get_weather_data(7.45,125.81,api_key='test-key')
    assert result['is_live'] is True
    assert result['temp']==28.1 and result['humidity']==77
    assert result['current_rain_1h_mm']==12
    assert result['rainfall_estimate'] in [v['rainfall'] for v in weather.TAGUM_CLIMATE_NORMALS.values()]
    assert result['rainfall_source']=='Monthly climate preset'


def test_weather_failure_returns_labeled_fallback(monkeypatch, capsys):
    def fail(*args,**kwargs):raise requests.Timeout('request URL with appid=test-key')
    monkeypatch.setattr(weather.requests,'get',fail)
    assert weather.get_weather_data(7.45,125.81,api_key='test-key')['is_live'] is False
    assert 'test-key' not in capsys.readouterr().out


def test_translations_do_not_claim_unmeasured_accuracy():
    text=(Path(__file__).resolve().parents[1]/'frontend/app.js').read_text(encoding='utf-8')
    assert '±15-20%' not in text
