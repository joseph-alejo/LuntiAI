import sys
from pathlib import Path
import numpy as np
import pytest
import shap
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'api'))
from xai import explain_prediction


@pytest.fixture(scope='module')
def example():
    rng = np.random.default_rng(42)
    x = rng.normal(size=(150, 8))
    y = np.argmax(x[:, :3], axis=1)
    model = RandomForestClassifier(n_estimators=12, max_depth=5, random_state=42).fit(x, y)
    explainer = shap.TreeExplainer(model, feature_perturbation='tree_path_dependent', model_output='raw')
    row = x[:1]
    probabilities = model.predict_proba(row)[0]
    return explainer, row, probabilities, ['A', 'B', 'C'], int(np.argmax(probabilities))


def test_complete_class_and_runner_up_reconstruction(example):
    result = explain_prediction(*example)
    parts = result['contributions']
    assert len(parts) == len({p['feature'] for p in parts}) == 8
    assert result['base_value'] + sum(p['value'] for p in parts) == pytest.approx(result['prediction_value'])
    alt = result['alternative']
    assert alt['base_gap'] + sum(p['difference'] for p in parts) == pytest.approx(alt['probability_gap'])
    assert alt['class'] != result['explained_class']
    assert result['max_additivity_error'] < 1e-5


def test_legacy_shap_list_shape(example):
    explainer, *args = example
    class Legacy:
        expected_value = explainer.expected_value
        feature_perturbation = explainer.feature_perturbation
        def shap_values(self, x):
            return list(np.moveaxis(explainer.shap_values(x), -1, 0))
    assert explain_prediction(Legacy(), *args)['prediction_value'] == explain_prediction(*example)['prediction_value']


@pytest.mark.parametrize('bad', [np.zeros((1, 7)), np.full((1, 8), np.nan)])
def test_invalid_input_rejected(example, bad):
    with pytest.raises(ValueError, match='eight-feature'):
        explain_prediction(example[0], bad, *example[2:])


def test_incorrect_attribution_rejected(example):
    explainer, *args = example
    class Broken:
        expected_value = explainer.expected_value
        def shap_values(self, x):
            return np.zeros((1, 8, 3))
    with pytest.raises(ValueError, match='reconstruct'):
        explain_prediction(Broken(), *args)
