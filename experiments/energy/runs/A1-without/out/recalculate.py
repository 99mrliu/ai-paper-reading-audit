import csv,json
from decimal import Decimal as D
rows=[('T2Tbase','1415.78','12','27','26'),('T2Tbig','1515.43','84','201','192'),('ELMo','517.66','336','275','262'),('BERTbase GPU','12041.51','79','1507','1438'),('NAS GPU','1515.43','274120','656347','626155')]
with open('out/table3-recalculation.csv','w') as f:
 w=csv.writer(f);w.writerow(['model','power_W','hours','printed_kWh_PUE','printed_lb','nominal_kWh_PUE','nominal_lb','energy_delta_calc_minus_print','lb_delta_calc_minus_print','printed_energy_times_0.954'])
 for name,p,t,e,c in rows:
  calc=D(p)*D(t)*D('1.58')/1000;co=calc*D('.954')
  vals=[name,p,t,e,c,calc,co,calc-D(e),co-D(c),D(e)*D('.954')];w.writerow(vals);print(vals)
extra={
 'NAS_printed_lb_in_kg':D('626155')*D('.45359237'),
 'ELMo_energy_using_517W':D('517')*336*D('1.58')/1000,
 'BERT_energy_using_79.2h':D('12041.51')*D('79.2')*D('1.58')/1000,
 'local_gpu_energy_kWh':D('1.51543')*84,
 'local_facility_estimate_kWh':D('1.51543')*84*D('1.58'),
 'local_estimate_lb':D('1.51543')*84*D('1.58')*D('.954'),
 'local_estimate_kg':D('1.51543')*84*D('1.58')*D('.954')*D('.45359237'),
 'local_meter_lb':D('201')*D('.954'),
 'local_meter_kg':D('201')*D('.954')*D('.45359237'),
 'local_meter_to_gpu_ratio':D('201')/(D('1.51543')*84),
 'table4_full_average_hours':D('239942')/4789,
 'table4_52h_total':D(4789)*52,
 'table4_electric_implied_facility_kWh':D('9870')/D('.12'),
 'table4_electric_implied_avg_IT_W':D('9870')/D('.12')/D('239942')/D('1.58')*1000,
 'table1_full_pipeline_implied_kWh':D('78468')/D('.954'),
 'NAS_steps_nominal_TPU_hours':D('979000000')/300000*10,
}
open('out/additional-calculations.json','w').write(json.dumps(extra,default=str,indent=2))
for k,v in extra.items():print(k,v)
