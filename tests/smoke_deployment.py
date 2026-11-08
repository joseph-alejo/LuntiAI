"""Exercise a running demo with a disposable account; never print credentials."""
import argparse
import json
import secrets
import time
from pathlib import Path
import requests

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('base_url')
parser.add_argument('--require-xai',action='store_true')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
base=args.base_url.rstrip('/')
session=requests.Session()
checks=[]
report={'base_url':base,'checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'checks':checks}
payload={'N':131.3,'P':44.1,'K':120.5,'temperature':28.22,'humidity':81.6,'ph':5.42,'rainfall':199.36,'OM':4.38,'barangay':'Madaum'}
username='check-'+secrets.token_hex(7)
password=secrets.token_urlsafe(24)
created=False

def request(method,path,expected=200,**kwargs):
    response=session.request(method,base+path,timeout=45,**kwargs)
    assert response.status_code==expected,(method,path,response.status_code)
    return response

try:
    health=request('GET','/health').json()
    assert health['model_loaded'] and health['label_encoder_loaded']
    if args.require_xai:assert health['explanation_available']
    checks.append('model health')
    assert len(request('GET','/app/').content)>1000
    checks.append('frontend delivered')
    assert request('GET','/barangays').json()['total']==23
    weather=request('GET','/weather/Madaum').json()['weather']
    report['weather']={key:weather.get(key) for key in ['source','rainfall_source','is_live','rainfall_estimate']}
    checks.append('barangay and weather endpoints')
    request('POST','/predict',expected=401,json=payload)
    checks.append('prediction requires login')
    registered=request('POST','/register',json={'username':username,'display_name':'Disposable verification','password':password}).json()
    created=True
    session.headers['Authorization']='Bearer '+registered['access_token']
    login=request('POST','/login',json={'username':username,'password':password}).json()
    session.headers['Authorization']='Bearer '+login['access_token']
    assert request('GET','/me').json()['user']['username']==username
    checks.append('register login and profile')
    request('POST','/predict',expected=422,json={**payload,'N':999})
    checks.append('invalid inputs rejected')
    for i in range(4):
        result=request('POST','/predict',json=payload).json()
        assert result['best_crop']=='Banana'
        assert result['confidence']==99.21
        assert result['is_quota_limited']==(i==3)
        explanation=result.get('shap_explanation')
        if args.require_xai:
            assert result['explanation_status']=='available'
            assert len(explanation['contributions'])==8
            reconstructed=explanation['base_value']+sum(x['value'] for x in explanation['contributions'])
            assert abs(reconstructed-explanation['prediction_value'])<1e-5
            alt=explanation['alternative']
            assert abs(alt['base_gap']+sum(x['difference'] for x in explanation['contributions'])-alt['probability_gap'])<1e-5
    report['prediction']={'crop':result['best_crop'],'probability_percent':result['confidence'],
        'complete_xai':bool(explanation and 'contributions' in explanation),
        'max_additivity_error':explanation.get('max_additivity_error') if explanation else None}
    checks.append('real model prediction and daily quota')
    if args.require_xai:checks.append('complete class and runner-up reconstruction under quota')
    request('GET','/history',expected=403)
    assert request('POST','/redeem',json={'code':'LUNTIAI2026'}).json()['user']['tier']=='premium'
    assert request('GET','/history').json()['total']==4
    checks.append('premium redemption and prediction history')
    print(json.dumps(report,indent=2),flush=True)
finally:
    if created:
        assert request('GET','/me').json()['user']['username']==username
        request('DELETE','/me')
        checks.append('disposable account removed')
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2),encoding='utf-8')
