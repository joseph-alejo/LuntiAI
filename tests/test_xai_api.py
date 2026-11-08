import numpy as np
import pytest
from test_auth_quota_api import client, PREDICTION_PAYLOAD


def test_available_failed_and_quota_locked_explanations(client, monkeypatch):
    import main
    class Explainer:
        expected_value = np.array([0.3, 0.3, 0.4])
        feature_perturbation = 'tree_path_dependent'
        def shap_values(self, x):
            values = np.zeros((1, 8, 3))
            values[0, 0] = np.array([0.9, 0.08, 0.02]) - self.expected_value
            return values
    monkeypatch.setattr(main, 'explainer', Explainer())
    registered = client.post('/register', json={'username': 'xai-check', 'display_name': 'XAI', 'password': 'test-password-2026'})
    assert registered.status_code == 200
    headers = {'Authorization': 'Bearer ' + registered.json()['access_token']}
    for _ in range(4):
        result = client.post('/predict', json=PREDICTION_PAYLOAD, headers=headers)
        assert result.status_code == 200
        assert result.json()['explanation_status'] == 'available'
        assert len(result.json()['shap_explanation']['contributions']) == 8
    def broken(x):
        raise RuntimeError('deliberate test failure')
    monkeypatch.setattr(main.explainer, 'shap_values', broken)
    failed = client.post('/predict', json=PREDICTION_PAYLOAD, headers=headers).json()
    assert failed['explanation_status'] == 'unavailable'
    assert failed['shap_explanation'] is None
    assert failed['confidence'] == pytest.approx(90)
