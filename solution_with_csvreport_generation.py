import typing
from dataclasses import dataclass 
from collections import defaultdict
from pprint import pprint

@dataclass
class FinancialRecord:
    year:int
    company:str = ''
    revenue:float = 0.0

@dataclass
class FinancialReports:
    data:str = 'year, company, revenue' # assumes first line as header
    
    def __post_init__(self):
        data = [ row.split(',') for row in self.data.split('\n') ]
        self.records = [FinancialRecord(year=int(year.strip()),company=company.strip(), revenue=float(revenue.strip())) for year, company, revenue in data[1:] ]

    def revenueByCompany(self):
        output = defaultdict(lambda: 0.0)
        for rec in self.records:
            output[rec.company] = output[rec.company] + rec.revenue
        return output

    def revenueByYear(self):
        output = defaultdict(lambda: 0.0)
        for rec in self.records:
            output[rec.year] = output[rec.year] + rec.revenue
        return output
        
    def generateReport(self, key, outputFilePath='report.csv'):
        import csv
        fields = [key, 'Revenue']
        rows = [[key, value] for key, value in getattr(self, f"revenueBy{key}")()]
        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
            csvwriter.writerow(fields) 
            csvwriter.writerows(rows)

def read_file(filename):
    with open(filename) as fp:
        lines = fp.readlines()
    return lines

import unittest
class TestRevenue(unittest.TestCase):
    data = '''year, company, revenue
2015, eka, 200000
2016, dvi, 100000
2018, tri, 50000
2015, chatur, 10000
2016, eka, 70000
2015, dvi, 19000
2015, tri, 45000
2017, chatur, 22000
2017, eka, 80000
2017, dvi, 88000
2016, tri, 15500
2018, chatur, 32000
2019, eka, 123000
2019, dvi, 167700
2019, tri, 48000
2021, pmg, 10000
2021, pmg, 20000
2019, chatur, 12000'''

    financialReports = FinancialReports(data=data)
    
    def test_revenueByCompany(self):
        revenue = self.financialReports.revenueByCompany()
        pprint(revenue)
        self.assertEqual(revenue['pmg'], 30000.0, 'Revenume by Company for pmg company is incorrect')
        print('ok')


    def test_revenueByYear(self):
        revenue = self.financialReports.revenueByYear()
        pprint(revenue)
        self.assertEqual(revenue[2021], 30000.0, 'Revenume by year for pmg year is incorrect')
        print('ok')

if __name__ == '__main__':
    unittest.main()

def DriverMainFunction():
    data = read_file('xyz.csv')
    reports = FinancialReports(data=data)
    reports.generateReport('Year', 'revenueByYear.csv')
    reports.generateReport('Company', 'revenueByCompany.csv')
	
'''======================== OUTPUT ========================
defaultdict(<function FinancialReports.revenueByCompany.<locals>.<lambda> at 0x7f3825a1cd30>,
            {'chatur': 76000.0,
             'dvi': 374700.0,
             'eka': 473000.0,
             'pmg': 30000.0,
             'tri': 158500.0})
ok
.defaultdict(<function FinancialReports.revenueByYear.<locals>.<lambda> at 0x7f3825a1cd30>,
            {2015: 274000.0,
             2016: 185500.0,
             2017: 190000.0,
             2018: 82000.0,
             2019: 350700.0,
             2021: 30000.0})
ok
.----------------------------------------------------------------------
Ran 2 tests in 0.007s
OK
> 