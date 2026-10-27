"""Author-side falsification of an AI's shared-power assumption. No model/API use."""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
import json

def shown(x):
 with localcontext() as c:
  c.prec=45
  return {'fraction':str(x),'decimal':str(D(x.numerator)/D(x.denominator))}
def main():
 # Transcribed Table3, original PDF p4 / proceedings3648; not new measurements.
 fit=[{'model':'T2Tbig','hardware':'P100','g':8,'power_W':'1515.43'},
      {'model':'BERTbase','hardware':'V100','g':64,'power_W':'12041.51'}]
 validation={'model':'T2Tbase','hardware':'P100','g':8,'power_W':'1415.78'}
 g0,g1=[F(r['g']) for r in fit];p0,p1=[F(r['power_W']) for r in fit]
 pg=(p1-p0)/(g1-g0);overhead=p0-g0*pg
 predicted=overhead+F(validation['g'])*pg
 residual=predicted-F(validation['power_W'])
 assert residual==F('99.65')
 inverse=F('191.88')/F('.954');unrounded=F('1515.43')*84*F('1.58')/1000
 return {'scope':'conditional algebraic fit from two rows; no identification of measurement source',
 'source':'Strubell et al ACL2019 P19-1355 PDFp4 Table3; method PDFp2',
 'fit_rows':fit,'conditional_model':'Power_W = common_CPU_DRAM_W + g * common_GPU_W',
 'unsupported_assumptions':['common average GPU power across P100 and V100','common CPU/DRAM and workload conditions across rows'],
 'fit_parameters':{'common_GPU_W':shown(pg),'common_CPU_DRAM_W':shown(overhead)},
 'exact_fit_residuals_W':[shown(overhead+F(r['g'])*pg-F(r['power_W'])) for r in fit],
 'not_in_fit_validation_row':validation,'predicted_power_W':shown(predicted),'prediction_minus_table_W':shown(residual),
 'strict_two_decimal_display_tolerance_W':'0.01',
 'global_common_parameter_model_rejected_by_this_row':abs(residual)>F('.01'),
 'provenance':'not_identified; rejection of shared-parameter model does not prove direct reuse or any alternative source',
 'rounding_identity_check':{'191_88_div_factor_kWh':shown(inverse),'unrounded_T2Tbig_kWh':shown(unrounded),
 'exactly_equal':inverse==unrounded,'inverse_minus_unrounded_kWh':shown(inverse-unrounded),
 'unrounded_carbon_lb':shown(unrounded*F('.954')),'rounded_2_decimal_display':'191.88; approximate equality only'}}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
