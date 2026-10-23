import csv
from pathlib import Path
rows=[('T2Tbase',1415.78,12,27,26),('T2Tbig',1515.43,84,201,192),('ELMo',517.66,336,275,262),('BERTbase_GPU',12041.51,79,1507,1438),('NAS_GPU',1515.43,274120,656347,626155)]
with Path('out/table3_recalculation.csv').open('w',newline='') as f:
 w=csv.writer(f)
 w.writerow(['model','power_W','hours_printed','energy_printed_kWh','CO2_printed_lb','energy_recalc_kWh','CO2_recalc_lb','energy_delta_recalc_minus_printed','CO2_delta_recalc_minus_printed_lb'])
 for name,p,t,e,c in rows:
  energy=p*t*1.58/1000;carbon=energy*.954
  w.writerow([name,p,t,e,c,energy,carbon,energy-e,carbon-c])
with Path('out/additional_checks.txt').open('w') as f:
 def record(label,value): f.write(f'{label}: {value}\n')
 record('BERT at 79.2h kWh',12041.51*79.2*1.58/1000)
 record('BERT at 79.2h lb',12041.51*79.2*1.58/1000*.954)
 record('NAS 979M/300k*10 TPU core hours',979e6/300000*10)
 record('NAS 979M/300k*84 8-GPU elapsed-equivalent hours',979e6/300000*84)
 record('626155 lb in kg',626155*.45359237)
 record('local GPU energy kWh',1.51543*84)
 record('local PUE-scaled kWh',1.51543*84*1.58)
 record('local estimated lb',1.51543*84*1.58*.954)
 record('local estimated kg',1.51543*84*1.58*.954*.45359237)
 record('201 facility kWh estimated lb',201*.954)
 record('201 facility kWh estimated kg',201*.954*.45359237)
 record('201 / GPU kWh ratio',201/(1.51543*84))
 record('Table4 mean hours',239942/4789)
 record('9998 GPU days in hours',9998*24)
 record('Table4 implied kWh from electricity dollars',9870/.12)
 record('Table4 implied average facility kW',9870/.12/239942)
 record('Table4 implied lb from electricity dollars',9870/.12*.954)
