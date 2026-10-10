"""Calculate endpoint comparisons from explicit ordered series (stdlib only).

Input: {"series": [{"id": "carbon", "source": "table1", "indicator": "...",
"unit": "t", "kind": "model_estimate", "scale": "county", "observations":
[{"time": 2000, "value": 100}, {"time": 2020, "value": 120}]}]}.
The input order is chronological. No trend, significance or causality is inferred.
"""
from __future__ import annotations
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path


def number(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('Values must be finite numbers; missing values are not zero.')
    try: result=Decimal(str(value))
    except InvalidOperation as exc: raise ValueError('Invalid numeric value') from exc
    if not result.is_finite(): raise ValueError('Values must be finite.')
    return result


def numeric(value):
    # Decimal arithmetic avoids floating-point rounding in the reported delta.
    return float(value) if value is not None else None


def build_ledger(data):
    rows=[]
    seen=set()
    for series in data['series']:
        ident=series['id']
        if not isinstance(ident,str) or not ident or ident in seen:
            raise ValueError('Each series needs a unique nonempty string id.')
        seen.add(ident)
        for field in ('source','indicator','unit','kind','scale'):
            if field not in series or not isinstance(series[field],str) or not series[field]:
                raise ValueError(f'{ident}: missing string field {field}')
        if series['kind'] not in ('observed','model_estimate','scenario_estimate'):
            raise ValueError(f'{ident}: unsupported kind')
        observations=series['observations']
        if len(observations)<2: raise ValueError(f'{ident}: need at least two observations')
        times=[x['time'] for x in observations]
        if len(set(map(str,times)))!=len(times): raise ValueError(f'{ident}: duplicate time labels')
        # Numeric years/dates encoded as numbers must be in increasing order.
        try: numeric_times=[number(t) for t in times]
        except ValueError: numeric_times=None
        if numeric_times and any(a>=b for a,b in zip(numeric_times,numeric_times[1:])):
            raise ValueError(f'{ident}: numeric times must be strictly increasing')
        values=[number(x['value']) for x in observations]
        if series['unit']=='%' and any(x<0 or x>100 for x in values):
            raise ValueError(f'{ident}: percentage values must be on the 0–100 scale')
        delta=values[-1]-values[0]
        relative=delta/values[0]*100 if values[0]>0 else None
        differences=[b-a for a,b in zip(values,values[1:])]
        if len(values)==2:
            shape='two_endpoints_only'
        elif all(x>0 for x in differences): shape='increases_at_all_observed_times'
        elif all(x<0 for x in differences): shape='decreases_at_all_observed_times'
        elif all(x==0 for x in differences): shape='unchanged_at_all_observed_times'
        else: shape='non_monotone_or_contains_plateaus'
        limitations=['No statistical significance or causal effect inferred.',
                     'Values at unobserved times are unknown.']
        if numeric_times is None: limitations.append('Nonnumeric time labels retain supplied order; verify chronological order.')
        if relative is None: limitations.append('Relative percent change omitted because the initial value is nonpositive.')
        if series['kind']=='scenario_estimate': limitations.append('Scenario results are conditional estimates, not observed outcomes.')
        rows.append({'fact_id':ident, 'source':series['source'], 'indicator':series['indicator'],
                     'unit':series['unit'],'kind':series['kind'],'scale':series['scale'],
                     'initial_time':times[0],'final_time':times[-1],
                     'initial_value':numeric(values[0]),'final_value':numeric(values[-1]),
                     'absolute_change':numeric(delta),'relative_percent_change':numeric(relative),
                     'percentage_point_change':numeric(delta) if series['unit']=='%' else None,
                     'observation_count':len(values),'observed_sequence_shape':shape,
                     'limitations':limitations})
    return {'schema_version':1,'facts':rows}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    try: ledger=build_ledger(json.loads(args.input.read_text(encoding='utf-8-sig')))
    except (KeyError,ValueError,TypeError) as exc: parser.error(str(exc))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(ledger["facts"])} facts to {args.output}')


if __name__=='__main__': main()
