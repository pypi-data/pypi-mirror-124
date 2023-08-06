import unittest
import pandas as pd
from sklearn.metrics import r2_score

from lightwood.api.high_level import code_from_json_ai, json_ai_from_problem, predictor_from_code
from lightwood.api.types import ProblemDefinition


class TestBasic(unittest.TestCase):
    def test_0_mean_ensemble(self):

        df = pd.read_csv('tests/data/concrete_strength.csv')

        target = 'concrete_strength'

        json_ai = json_ai_from_problem(df, ProblemDefinition.from_dict({
            'target': target,
            'time_aim': 80
        }))

        json_ai.outputs[target].ensemble = {
            'module': 'MeanEnsemble',
            "args": {
                'dtype_dict': '$dtype_dict'
            }
        }

        code = code_from_json_ai(json_ai)
        predictor = predictor_from_code(code)
        predictor.learn(df)
        predictions = predictor.predict(df)

        self.assertTrue(r2_score(df[target], predictions['prediction']) > 0.5)
