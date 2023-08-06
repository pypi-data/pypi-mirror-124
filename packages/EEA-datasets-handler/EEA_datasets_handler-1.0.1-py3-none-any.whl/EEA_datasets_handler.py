"""
Module which handles the air pollution datasets provided by `EEA <https://www.eea.europa.eu/data-and-maps/data/aqereporting-8>`_.

There are three groups of functions.
    1. Functions to get the EEA supported values.
    2. Functions to filter only the EEA supported values.
    3. Functions to download and handle the EEA datasets.
"""


import os, os.path
import re
import warnings
from copy import deepcopy

import requests
import pandas as pd

warnings.simplefilter("always") # To show always the warnings




#----------------------------------------------------------------------------------------------------------------------------
#  FUNCTIONS TO GET THE EEA SUPPORTED VALUES.


def get_supported_pollutants():
    """
    Return all the EEA supported pollutants, represented in the numeric notation.

    Returns
    ----------
    list
    """
    return list(get_supported_pollutants_dict().keys())


def get_supported_pollutants_dict():
    """
    Return the dict that maps the supported-pollutants numeric notations and their associated textual notations.

    Returns
    ----------
    dict

    Notes
    ----------
    While each pollutant has a different numeric notation, there are pollutants that have the same textual notation. (I.e.
    duplicate text notation)
    """
    return {1: 'SO2', 3: 'SA', 4: 'SPM', 5: 'PM10', 6: 'BS', 7: 'O3', 8: 'NO2', 9: 'NOX as NO2', 10: 'CO', 11: 'H2S', 12: 'Pb', 13: 'Hg', 14: 'Cd', 15: 'Ni', 16: 'Cr', 17: 'Mn', 18: 'As', 19: 'CS2', 20: 'C6H6', 21: 'C6H5-CH3', 22: 'C6H5-CH=CH2', 23: 'CH2=CH-CN', 24: 'CH2=CH-CH=CH2', 25: 'HCHO', 26: 'CHCl=CCl2', 27: 'C2Cl4', 28: 'CH2Cl2', 29: 'BaP', 30: 'PAH', 31: 'VC', 32: 'THC (NM)', 33: 'T-VOC', 34: 'PAN', 35: 'NH3', 36: 'N-DEP', 37: 'S-DEP', 38: 'NO', 39: 'HCl', 40: 'HF', 41: 'CH4', 42: 'C6H5OH', 45: 'NH4', 46: 'NO3', 47: 'SO4 (H2SO4 aerosols) (SO4--)', 48: 'Se', 49: 'V', 50: 'HNO3', 51: 'HC C2-C6(excl. AROM. & CHLH)', 52: 'HC > C6 (excl. AROM. & CHLH)', 53: 'Aromatics (except C6H6)', 54: 'Chlorinated hydrocarbons', 62: 'Fluor (except HF)', 63: 'Zn', 64: 'Co', 65: 'Fe', 66: 'Back scattering', 67: 'HNO3+NO3', 68: 'NH3+NH4', 69: 'Radioactivity', 71: 'CO2', 73: 'Cu', 78: 'C6H4-(CH3)2', 80: 'p-C6H4(CH3)2', 81: 'm-C6H4-(CH3)2', 82: 'trans-H3C-HC=CH-CH2-CH3', 83: 'cis-H3C-HC=CH-CH2-CH3', 302: 'CFC-11', 303: 'CFC-113', 304: 'CFC-12', 307: 'HCFC-123', 308: 'HCFC-22', 309: '1-methylnaphtalene', 310: '1-methylphenanthrene', 311: 'Methyletylketone (MEK)', 312: 'Crotonaldehyde', 313: '2-methylanthracene', 314: '2-methylbenzaldehyde', 315: '2-methylnaphtalene', 316: '(CH3)2-CH-CH2-CH2-CH3', 317: '2-methylphenanthrene', 318: 'Methacroleine', 319: 'Methylglyoxal', 320: 'Acroleine', 321: 'Methylvinylketone (MVK)', 322: '3-methylbenzaldehyde', 323: '3-methylpentane', 324: '4-methylbenzaldehyde', 326: 'NOy', 330: 'PCB-105', 333: 'PCB-128', 336: 'PCB-149', 339: 'PCB-156', 340: 'PCB-177', 341: 'PCB-18', 344: 'PCB-26', 347: 'PCB-31', 348: 'PCB-44', 351: 'Acenaphthene', 352: 'Acenaphtylene', 356: 'Aldrin', 364: 'Anthanthrene', 372: 'Benzaldehyde', 373: 'Benzo(a)fluoranthene', 374: 'C8H8O', 380: 'Benzo(b+j+k)fluoranthenes', 381: 'Benzo(e)pyrene', 390: 'Biphenyl', 391: 'Black Carbon', 393: 'Butanales', 394: 'H3C-CH2-CH2-CH3', 395: 'Butenes', 396: 'Methacroleine + Butanal', 401: 'Carbon-tetrachloride', 406: 'Chrysene', 412: 'k', 415: 'Coronene', 416: 'Cyclo-hexane', 417: 'Cyklopenta(cd)pyrene', 418: 'Dibenzo(ac+ah)anthracenes', 419: 'Dibenzo(ah)anthracene', 420: 'Dibenzofuran', 421: 'Dibenzothiophene', 425: 'N2O', 426: 'Endrin', 427: 'Acetaldehyde', 428: 'C2H6', 429: 'Glyoxal', 430: 'H2C=CH2', 431: 'C6H5-C2H5', 432: 'HC=CH', 433: 'C9H12', 434: 'C9H12', 435: 'Fluorene', 438: 'Halon 1211', 439: 'Halon 1301', 440: 'Heptachlor', 441: 'C7H16', 442: 'n-Hexanal', 443: 'C6H14', 447: 'H3C-CH(CH3)2', 448: 'i-Heptane', 449: '(CH3)3-C-CH2-CH-(CH3)2', 450: 'H3C-CH2-CH(CH3)2', 451: 'CH2=CH-C(CH3)=CH2', 453: 'C6H4Cl2', 454: 'C9H20', 455: 'C2Cl4', 456: 'Tetrachloromethane (air)', 457: 'Chlorobenzene (air)', 458: '1,1,2-trichloroethane (air)', 459: '1,1-dichloroethane (air)', 460: '1,2-dichloroethylene (air)', 461: '1,2-dichloroethane (air)', 462: '1,1,1-trichloroethane (air)', 463: 'Methyl-chloroform', 464: 'm,p-C6H4(CH3)2', 465: 'Naphtalene', 466: 'Neo-hexane', 467: 'Neo-pentane', 475: 'C8H18', 482: 'o-C6H4-(CH3)2', 485: 'Valeraldehyde', 486: 'H3C-(CH2)3-CH3', 487: 'Pentenes', 488: 'Perylene', 491: 'Acetophenone', 501: 'C4H8O', 502: 'Propanal', 503: 'H3C-CH2-CH3', 504: 'Acetone', 505: 'CH2=CH-CH3', 506: 'CH2=CH-CH3 + H3C-CH2-CH2-CH3', 507: 'H3C-(CH2)3-CH3 + H3C-CH2-CH(CH3)2', 508: 'Retene', 509: 'Acetone + Acrolein', 517: 'sum-PCB', 520: 'SO2 + SO4--', 601: '3-methylphenantrene', 602: '9-methylphenantrene', 604: 'Al', 605: 'Al', 606: 'Anthracene', 607: 'Anthracene', 608: 'Anthracene', 609: 'Benzo(a)anthracene', 610: 'Benzo(a)anthracene', 611: 'Benzo(a)anthracene', 613: 'Benzo(a)fluorene', 616: 'Benzo(b)fluoranthene', 617: 'Benzo(b)fluoranthene', 618: 'Benzo(b)fluoranthene', 619: 'Benzo(b)fluorene', 620: 'Benzo(ghi)fluoranthene', 621: 'Benzo(ghi)fluoranthene', 622: 'Benzo(ghi)perylene', 623: 'Benzo(ghi)perylene', 624: 'Benzo(ghi)perylene', 625: 'Benzo(k)fluoranthene', 626: 'Benzo(k)fluoranthene', 627: 'Benzo(k)fluoranthene', 629: 'Ca++', 630: 'Ca++', 631: 'Cl-', 632: 'Cl-', 633: 'Dibenz(ac+ah)anthracenes', 634: 'Dibenz(ac+ah)anthracenes', 635: 'Dibenz(ah)anthracene', 636: 'Dibenzo(ae)pyrene', 637: 'Dibenzo(ah)pyrene', 638: 'Dibenzo(ai)pyrene', 639: 'Dibenzo(ai)pyrene', 640: 'Dieldrin', 641: 'Dieldrin', 643: 'Fluoranthene', 644: 'Fluoranthene', 645: 'Fluoranthene', 648: 'H+', 649: 'HCB', 650: 'HCB', 652: 'Heptachlor Epoxide', 653: 'Hg-reactive', 654: 'Indeno-(1,2,3-cd)pyrene', 655: 'Indeno-(1,2,3-cd)pyrene', 656: 'Indeno-(1,2,3-cd)pyrene', 657: 'K+', 658: 'K+', 659: 'Mg++', 660: 'Mg++', 661: 'Mo', 664: 'NH4+', 666: 'NO3-', 667: 'Kj-N', 668: 'Na+', 669: 'Na+', 670: 'PCB-101', 671: 'PCB-101', 672: 'PCB-101', 673: 'PCB-114', 674: 'PCB-118', 675: 'PCB-118', 676: 'PCB-118', 677: 'PCB-138', 678: 'PCB-138', 679: 'PCB-141', 680: 'PCB-153', 681: 'PCB-153', 682: 'PCB-153', 683: 'PCB-157', 684: 'PCB-167', 685: 'PCB-170', 686: 'PCB-180', 687: 'PCB-180', 688: 'PCB-180', 689: 'PCB-183', 690: 'PCB-187', 691: 'PCB-189', 692: 'PCB-194', 693: 'PCB-206', 694: 'PCB-209', 695: 'PCB-28', 696: 'PCB-28', 697: 'PCB-28', 698: 'PCB-33', 699: 'PCB-37', 700: 'PCB-47', 701: 'PCB-52', 702: 'PCB-52', 703: 'PCB-52', 704: 'PCB-60', 705: 'PCB-66', 706: 'PCB-74', 707: 'PCB-99', 708: 'PCB_122', 709: 'PCB_123', 710: 'PCB_128', 711: 'PCB_138', 712: 'Phenanthrene', 713: 'Phenanthrene', 714: 'Phenanthrene', 715: 'Pyrene', 716: 'Pyrene', 717: 'Pyrene', 719: 'SO4--', 720: 'SO4-- corr', 723: 'TI', 728: 'Vanadium', 729: 'alpha-HCH', 730: 'alpha-HCH', 731: 'alpha-HCH', 732: 'beta-HCH', 733: 'beta-HCH', 734: 'cis-CD', 735: 'cis-CD', 736: 'cis-NO', 737: 'gamma-HCH', 738: 'gamma-HCH', 739: 'gamma-HCH', 741: "o,p'-DDD", 742: "o,p'-DDE", 743: "o,p'-DDT", 744: "o,p'-DDD", 745: "o,p'-DDE", 746: "o,p'-DDT", 747: "p,p'-DDD", 748: "p,p'-DDE", 749: "p,p'-DDT", 750: "p,p'-DDD", 751: "p,p'-DDE", 752: "p,p'-DDT", 753: 'precip_amount', 754: 'precip_amount_off', 755: 'trans-CD', 756: 'trans-CD', 757: 'trans-NO', 758: 'trans_NO', 759: 'Benzo(j)fluoranthene', 760: 'Benzo(j)fluoranthene', 761: 'Benzo(j)fluorene', 762: 'Benzo(j)fluoranthene', 763: 'Dibenzo(ah)anthracene', 771: 'EC', 772: 'OC', 773: 'alpha-Endosulfan', 774: 'beta-Endosulfan', 775: 'Endosulfan sulfate', 776: 'DCMU', 777: 'Atrazine', 778: 'Isoproturon', 779: 'Heptachlor', 780: 'Aldrin', 1012: 'Pb in PM2.5', 1013: 'Hg in PM2.5', 1014: 'Cd in PM2.5', 1015: 'Ni in PM2.5', 1016: 'Cr in PM2.5', 1017: 'Mn in PM2.5', 1018: 'As in PM2.5', 1029: 'BaP in PM2.5', 1045: 'NH4+ in PM2.5', 1046: 'NO3- in PM2.5', 1047: 'SO42- in PM2.5', 1048: 'Se in PM2.5', 1049: 'V in PM2.5', 1063: 'Zn in PM2.5', 1064: 'Co in PM2.5', 1065: 'Fe in PM2.5', 1073: 'Cu in PM2.5', 1129: 'BaP in PM2.5', 1419: 'Dibenzo(ah)anthracene in PM2.5', 1610: 'Benzo(a)anthracene in PM2.5', 1617: 'Benzo(b)fluoranthene in PM2.5', 1626: 'Benzo(k)fluoranthene in PM2.5', 1629: 'Ca2+ in PM2.5', 1631: 'Cl- in PM2.5', 1655: 'Indeno-(1,2,3-cd)pyrene in PM2', 1657: 'K+ in PM2.5', 1659: 'Mg2+ in PM2.5', 1668: 'Na+  in PM2.5', 1759: 'Benzo(j)fluoranthene in PM2.5', 1771: 'EC in PM2.5', 1772: 'OC in PM2.5', 2012: 'Pb', 2013: 'Hg', 2014: 'Cd', 2015: 'Ni', 2016: 'Cr', 2017: 'Mn', 2018: 'As', 2063: 'Zn', 2064: 'Co', 2065: 'Fe', 2073: 'Cu', 2076: 'pH', 2380: 'Benzo(b,j,k)fluoranthene', 2770: 'PO43-', 2771: 'TP', 2861: 'PFBA', 2862: 'PFPeA', 2863: 'PFHxA', 2864: 'PFHpA', 2865: 'PFOA', 2866: 'PFNA', 2867: 'PFDA', 2868: 'PFUnDA', 2871: 'PFBS', 2872: 'PFHxS', 2873: 'PFOSA', 2874: '6:2-FTS', 2875: 'PFOS', 2876: 'PFDS', 3012: 'Pb in TSP', 3013: 'Hg in TSP', 3014: 'Cd in TSP', 3015: 'Ni in TSP', 3016: 'Cr in TSP', 3017: 'Mn in TSP', 3018: 'As in TSP', 3063: 'Zn in TSP', 3073: 'Cu in TSP', 3631: 'Cl- in TSP', 3668: 'Na+  in TSP', 4013: 'Hg0', 4330: 'PCB-105', 4336: 'PCB-149', 4339: 'PCB-156', 4341: 'PCB-18', 4347: 'PCB-31', 4406: 'Chrysene', 4407: 'Chrysene + Triphenylene', 4813: 'Hg0 + Hg-reactive', 4821: 'TCDD', 4822: 'CDD1N', 4823: 'CDD4X', 4824: 'CDD6X', 4825: 'CDD9X', 4826: 'CDD6P', 4827: 'CDDO', 4841: 'CDF2T', 4842: 'CDFDN', 4843: 'CDF2N', 4844: 'CDFDX', 4845: 'CDF6X', 4846: 'CDF9X', 4847: 'CDF4X', 4848: 'CDF6P', 4849: 'CDF9P', 4850: 'CDFO', 4851: 'CDFX1', 4852: 'CDFP2', 4861: 'PFBA', 4862: 'PFPeA', 4863: 'PFHxA', 4864: 'PFHpA', 4865: 'PFOA', 4866: 'PFNA', 4867: 'PFDA', 4868: 'PFUnDA', 4871: 'PFBS', 4872: 'PFHxS', 4873: 'PFOSA', 4874: '6:2-FTS', 4875: 'PFOS', 4876: 'PFDS', 4901: 'BDE47', 4902: 'BDE85', 4903: 'BDE99', 4904: 'BDE100', 4905: 'BDE153', 4906: 'BDE154', 4907: 'BDE209', 4908: 'SCCP', 4909: 'MCCP', 4910: 'HBCD', 4911: 'HBB', 4912: 'PBT', 4913: 'PBEB', 4914: 'α-DBE-DBCH', 4915: 'β-DBE-DBCH', 4916: 'BEH-TEBP', 4917: 'BTBPT', 4918: 'EH-TBB', 4919: 'Syn-DP', 4920: 'Anti-DP', 4921: 'DBDPE', 4922: 'TBP', 5012: 'Pb in PM10', 5013: 'Hg in PM10', 5014: 'Cd in PM10', 5015: 'Ni in PM10', 5016: 'Cr in PM10', 5017: 'Mn in PM10', 5018: 'As in PM10', 5029: 'BaP in PM10', 5045: 'NH4+ in PM10', 5046: 'NO3- in PM10', 5047: 'SO42-  in PM10', 5048: 'Se in PM10', 5049: 'V in PM10', 5060: 'Sn in PM10', 5063: 'Zn in PM10', 5064: 'Co in PM10', 5065: 'Fe in PM10', 5073: 'Cu in PM10', 5129: 'BaP in PM10', 5301: '1-Methyl anthracene in PM10', 5364: 'Anthanthrene in PM10', 5380: 'Benzo(b,j,k)fluorantheneInPM1', 5381: 'Benzo(e)pyrene in PM10', 5406: 'Chrysene in PM10', 5415: 'Coronene in PM10', 5417: 'Cyclopenta(c,d)pyrene in PM10', 5418: 'Dibenzo(ac+ah)anthracene in PM10', 5419: 'Dibenzo(ah)anthracene in PM10', 5480: 'Benzo(b,j)fluorantheneinPM10', 5488: 'Perylene in PM10', 5521: '4.5-Methylene phenanthrene in PM10', 5522: '5-Methyl Chrysene in PM10', 5523: '9-Methyl anthracene in PM10', 5524: 'Benzo(b)naphtho(2,1-d)thiophene in PM10', 5525: 'Benzo(c)phenanthrene in PM10', 5526: 'Cholanthrene in PM10', 5527: 'Dibenzo(ac)anthracene in PM10', 5528: 'Dibenzo(al)pyrene in PM10', 5580: 'Benzo(b+j)fluoranthene in PM10', 5606: 'Anthracene in PM10 (aerosol)', 5609: 'Benzo(a)anthracene in PM10', 5610: 'Benzo(a)anthracene in PM10', 5616: 'Benzo(b)fluoranthene in PM10', 5617: 'Benzo(b)fluoranthene in PM10', 5622: '5-Methyl Chrysene in PM10', 5623: 'Benzo(ghi)perylene in PM10', 5624: 'Benzo(b)naphtho(2,1-d)thiophene in PM10', 5625: 'Benzo(k)fluoranthene in PM10', 5626: 'Benzo(k)fluoranthene in PM10', 5627: 'Dibenzo(ac)anthracene in PM10', 5628: 'Dibenzo(al)pyrene in PM10', 5629: 'Ca2+ in PM10', 5631: 'Cl- in PM10', 5633: 'Dibenzo(ah+ac)anthracene in PM10', 5636: 'Dibenzo(ae)pyrene in PM10', 5637: 'Dibenzo(ah)pyrene in PM10', 5639: 'Dibenzo(ai)pyrene in PM10', 5643: 'Fluoranthene in PM10 (aerosol)', 5654: 'Indeno-(1,2,3-cd)pyrene in PM', 5655: 'Indeno-(1,2,3-cd)pyrene in PM', 5657: 'K+ in PM10', 5659: 'Mg2+ in PM10', 5668: 'Na+  in PM10', 5712: 'Phenanthrene in PM10 (aerosol)', 5715: 'Pyrene in PM10 (aerosol)', 5725: 'Benzo(c)phenanthrene in PM10', 5733: 'Dibenzo(ah+ac)anthracene in PM10', 5759: 'Benzo(j)fluoranthene in PM10', 5762: 'Benzo(j)fluoranthene in PM10', 5763: 'Dibenzo(ah)anthracene in PM10', 5771: 'EC in PM10', 5772: 'OC in PM10', 6001: 'PM2.5', 6002: 'PM1', 6005: 'H2C=CH-CH2-CH3', 6006: 'trans-H3C-CH=CH-CH3', 6007: 'cis-H3C-CH=CH-CH3', 6008: 'H2C=CH-CH2-CH2-CH3', 6009: 'H3C-HC=CH-CH2-CH3', 6011: '1,2,4-C6H3(CH3)3', 6012: '1,2,3-C6H3(CH3)3', 6013: '1,3,5-C6H3(CH3)3', 6015: 'BaP', 6016: 'C6H12', 6017: 'C6H12O2', 6380: 'Benzo(b,j,k)fluorantheneInPM1', 6400: 'VPM10', 6401: 'NVPM10', 6410: 'VPM2.5', 6411: 'NVPM2.5', 6420: 'VPM1', 6421: 'NVPM1', 7012: 'Pb', 7013: 'Hg', 7014: 'Cd', 7015: 'Ni', 7016: 'Cr', 7018: 'As', 7029: 'BaP', 7063: 'Zn', 7073: 'Cu', 7301: '1-Methyl anthracene', 7309: '1-Methyl Naphthalene', 7310: '1-Methyl phenanthrene', 7313: '2-Methyl anthracene', 7315: '2-Methyl Naphthalene', 7317: '2-Methyl phenanthrene', 7351: 'Acenaphthene', 7352: 'Acenaphthylene', 7364: 'Anthanthrene', 7380: 'Benzo(b,j,k)fluoranthene', 7381: 'Benzo(e)pyrene', 7390: 'Biphenyl', 7406: 'Chrysene', 7407: 'Chrysene + Triphenylene', 7415: 'Coronene', 7417: 'Cyclopenta(c,d)pyrene', 7418: 'Dibenzo(ah+ac)anthracene', 7419: 'Dibenzo(ah)anthracene', 7435: 'Fluorene', 7465: 'Naphthalene', 7480: 'Benzo(b+j)fluoranthene', 7488: 'Perylene', 7521: '4.5-Methylene phenanthrene', 7522: '5-Methyl Chrysene', 7523: '9-Methyl anthracene', 7524: 'Benzo(b)naphtho(2,1-d)thiophene', 7525: 'Benzo(c)phenanthrene', 7526: 'Cholanthrene', 7527: 'Dibenzo(ac)anthracene', 7528: 'Dibenzo(al)pyrene', 7636: 'Dibenzo(ae)pyrene', 7637: 'Dibenzo(ah)pyrene', 7639: 'Dibenzo(ai)pyrene', 7640: 'Dieldrin', 7734: 'cis-CD', 7750: "p,p'-DDD", 7751: "p,p'-DDE", 7752: "p,p'-DDT", 7755: 'trans-CD', 7757: 'trans-NO', 7773: 'alpha-Endosulfan', 7774: 'beta-Endosulfan', 7775: 'Endosulfan sulfate', 7776: 'DCMU', 7777: 'Atrazine', 7778: 'Isoproturon', 7779: 'Heptachlor', 7780: 'Aldrin', 7781: 'HCB', 7821: 'TCDD', 7822: 'CDD1N', 7823: 'CDD4X', 7824: 'CDD6X', 7825: 'CDD9X', 7826: 'CDD6P', 7827: 'CDDO', 7841: 'CDF2T', 7842: 'CDFDN', 7843: 'CDF2N', 7844: 'CDFDX', 7845: 'CDF6X', 7846: 'CDF9X', 7847: 'CDF4X', 7848: 'CDF6P', 7849: 'CDF9P', 7850: 'CDFO', 7851: 'CDFX1', 7852: 'CDFP2', 7901: 'BDE47', 7902: 'BDE85', 7903: 'BDE99', 7904: 'BDE100', 7905: 'BDE153', 7906: 'BDE154', 7907: 'BDE209', 7908: 'SCCP', 7909: 'MCCP', 7910: 'HBCD'}


def get_supported_pollutants_inverse_dict():
    """
    Return the dict that maps the supported pollutants textual notations and their associated numeric notations.

    Returns
    ----------
    dict

    Notes
    ----------
    The returned dictionary doesn't contain all the supported pollutants: the pollutants for which exist at least another
    pollutant with the same textual-notation are not considered . (I.e. duplicate textual notation).
    """
    return {'SO2': 1, 'CO': 10, 'Pb in PM2.5': 1012, 'Hg in PM2.5': 1013, 'Cd in PM2.5': 1014, 'Ni in PM2.5': 1015, 'Cr in PM2.5': 1016, 'Mn in PM2.5': 1017, 'As in PM2.5': 1018, 'NH4+ in PM2.5': 1045, 'NO3- in PM2.5': 1046, 'SO42- in PM2.5': 1047, 'Se in PM2.5': 1048, 'V in PM2.5': 1049, 'Zn in PM2.5': 1063, 'Co in PM2.5': 1064, 'Fe in PM2.5': 1065, 'Cu in PM2.5': 1073, 'H2S': 11, 'Dibenzo(ah)anthracene in PM2.5': 1419, 'Benzo(a)anthracene in PM2.5': 1610, 'Benzo(b)fluoranthene in PM2.5': 1617, 'Benzo(k)fluoranthene in PM2.5': 1626, 'Ca2+ in PM2.5': 1629, 'Cl- in PM2.5': 1631, 'Indeno-(1,2,3-cd)pyrene in PM2': 1655, 'K+ in PM2.5': 1657, 'Mg2+ in PM2.5': 1659, 'Na+  in PM2.5': 1668, 'Benzo(j)fluoranthene in PM2.5': 1759, 'EC in PM2.5': 1771, 'OC in PM2.5': 1772, 'CS2': 19, 'C6H6': 20, 'pH': 2076, 'C6H5-CH3': 21, 'C6H5-CH=CH2': 22, 'CH2=CH-CN': 23, 'CH2=CH-CH=CH2': 24, 'HCHO': 25, 'CHCl=CCl2': 26, 'PO43-': 2770, 'TP': 2771, 'CH2Cl2': 28, 'SA': 3, 'PAH': 30, 'Pb in TSP': 3012, 'Hg in TSP': 3013, 'Cd in TSP': 3014, 'Ni in TSP': 3015, 'Cr in TSP': 3016, 'Mn in TSP': 3017, 'As in TSP': 3018, 'CFC-11': 302, 'CFC-113': 303, 'CFC-12': 304, 'Zn in TSP': 3063, 'HCFC-123': 307, 'Cu in TSP': 3073, 'HCFC-22': 308, '1-methylnaphtalene': 309, 'VC': 31, '1-methylphenanthrene': 310, 'Methyletylketone (MEK)': 311, 'Crotonaldehyde': 312, '2-methylanthracene': 313, '2-methylbenzaldehyde': 314, '2-methylnaphtalene': 315, '(CH3)2-CH-CH2-CH2-CH3': 316, '2-methylphenanthrene': 317, 'Methacroleine': 318, 'Methylglyoxal': 319, 'THC (NM)': 32, 'Acroleine': 320, 'Methylvinylketone (MVK)': 321, '3-methylbenzaldehyde': 322, '3-methylpentane': 323, '4-methylbenzaldehyde': 324, 'NOy': 326, 'T-VOC': 33, 'PCB-128': 333, 'PAN': 34, 'PCB-177': 340, 'PCB-26': 344, 'PCB-44': 348, 'NH3': 35, 'Acenaphtylene': 352, 'N-DEP': 36, 'Cl- in TSP': 3631, 'Na+  in TSP': 3668, 'S-DEP': 37, 'Benzaldehyde': 372, 'Benzo(a)fluoranthene': 373, 'C8H8O': 374, 'NO': 38, 'Benzo(b+j+k)fluoranthenes': 380, 'HCl': 39, 'Black Carbon': 391, 'Butanales': 393, 'H3C-CH2-CH2-CH3': 394, 'Butenes': 395, 'Methacroleine + Butanal': 396, 'SPM': 4, 'HF': 40, 'Carbon-tetrachloride': 401, 'Hg0': 4013, 'CH4': 41, 'k': 412, 'Cyclo-hexane': 416, 'Cyklopenta(cd)pyrene': 417, 'Dibenzo(ac+ah)anthracenes': 418, 'C6H5OH': 42, 'Dibenzofuran': 420, 'Dibenzothiophene': 421, 'N2O': 425, 'Endrin': 426, 'Acetaldehyde': 427, 'C2H6': 428, 'Glyoxal': 429, 'H2C=CH2': 430, 'C6H5-C2H5': 431, 'HC=CH': 432, 'Halon 1211': 438, 'Halon 1301': 439, 'C7H16': 441, 'n-Hexanal': 442, 'C6H14': 443, 'H3C-CH(CH3)2': 447, 'i-Heptane': 448, '(CH3)3-C-CH2-CH-(CH3)2': 449, 'NH4': 45, 'H3C-CH2-CH(CH3)2': 450, 'CH2=CH-C(CH3)=CH2': 451, 'C6H4Cl2': 453, 'C9H20': 454, 'Tetrachloromethane (air)': 456, 'Chlorobenzene (air)': 457, '1,1,2-trichloroethane (air)': 458, '1,1-dichloroethane (air)': 459, 'NO3': 46, '1,2-dichloroethylene (air)': 460, '1,2-dichloroethane (air)': 461, '1,1,1-trichloroethane (air)': 462, 'Methyl-chloroform': 463, 'm,p-C6H4(CH3)2': 464, 'Naphtalene': 465, 'Neo-hexane': 466, 'Neo-pentane': 467, 'SO4 (H2SO4 aerosols) (SO4--)': 47, 'C8H18': 475, 'Se': 48, 'Hg0 + Hg-reactive': 4813, 'o-C6H4-(CH3)2': 482, 'Valeraldehyde': 485, 'H3C-(CH2)3-CH3': 486, 'Pentenes': 487, 'V': 49, 'Acetophenone': 491, 'HBB': 4911, 'PBT': 4912, 'PBEB': 4913, 'α-DBE-DBCH': 4914, 'β-DBE-DBCH': 4915, 'BEH-TEBP': 4916, 'BTBPT': 4917, 'EH-TBB': 4918, 'Syn-DP': 4919, 'Anti-DP': 4920, 'DBDPE': 4921, 'TBP': 4922, 'PM10': 5, 'HNO3': 50, 'C4H8O': 501, 'Pb in PM10': 5012, 'Hg in PM10': 5013, 'Cd in PM10': 5014, 'Ni in PM10': 5015, 'Cr in PM10': 5016, 'Mn in PM10': 5017, 'As in PM10': 5018, 'Propanal': 502, 'H3C-CH2-CH3': 503, 'Acetone': 504, 'NH4+ in PM10': 5045, 'NO3- in PM10': 5046, 'SO42-  in PM10': 5047, 'Se in PM10': 5048, 'V in PM10': 5049, 'CH2=CH-CH3': 505, 'CH2=CH-CH3 + H3C-CH2-CH2-CH3': 506, 'Sn in PM10': 5060, 'Zn in PM10': 5063, 'Co in PM10': 5064, 'Fe in PM10': 5065, 'H3C-(CH2)3-CH3 + H3C-CH2-CH(CH3)2': 507, 'Cu in PM10': 5073, 'Retene': 508, 'Acetone + Acrolein': 509, 'HC C2-C6(excl. AROM. & CHLH)': 51, 'sum-PCB': 517, 'HC > C6 (excl. AROM. & CHLH)': 52, 'SO2 + SO4--': 520, 'Aromatics (except C6H6)': 53, '1-Methyl anthracene in PM10': 5301, 'Anthanthrene in PM10': 5364, 'Benzo(e)pyrene in PM10': 5381, 'Chlorinated hydrocarbons': 54, 'Chrysene in PM10': 5406, 'Coronene in PM10': 5415, 'Cyclopenta(c,d)pyrene in PM10': 5417, 'Dibenzo(ac+ah)anthracene in PM10': 5418, 'Benzo(b,j)fluorantheneinPM10': 5480, 'Perylene in PM10': 5488, '4.5-Methylene phenanthrene in PM10': 5521, '9-Methyl anthracene in PM10': 5523, 'Cholanthrene in PM10': 5526, 'Benzo(b+j)fluoranthene in PM10': 5580, 'Anthracene in PM10 (aerosol)': 5606, 'Benzo(ghi)perylene in PM10': 5623, 'Ca2+ in PM10': 5629, 'Cl- in PM10': 5631, 'Dibenzo(ae)pyrene in PM10': 5636, 'Dibenzo(ah)pyrene in PM10': 5637, 'Dibenzo(ai)pyrene in PM10': 5639, 'Fluoranthene in PM10 (aerosol)': 5643, 'K+ in PM10': 5657, 'Mg2+ in PM10': 5659, 'Na+  in PM10': 5668, 'Phenanthrene in PM10 (aerosol)': 5712, 'Pyrene in PM10 (aerosol)': 5715, 'EC in PM10': 5771, 'OC in PM10': 5772, 'BS': 6, 'PM2.5': 6001, 'PM1': 6002, 'H2C=CH-CH2-CH3': 6005, 'trans-H3C-CH=CH-CH3': 6006, 'cis-H3C-CH=CH-CH3': 6007, 'H2C=CH-CH2-CH2-CH3': 6008, 'H3C-HC=CH-CH2-CH3': 6009, '3-methylphenantrene': 601, '1,2,4-C6H3(CH3)3': 6011, '1,2,3-C6H3(CH3)3': 6012, '1,3,5-C6H3(CH3)3': 6013, 'C6H12': 6016, 'C6H12O2': 6017, '9-methylphenantrene': 602, 'Benzo(a)fluorene': 613, 'Benzo(b)fluorene': 619, 'Fluor (except HF)': 62, 'Dibenz(ah)anthracene': 635, 'VPM10': 6400, 'NVPM10': 6401, 'VPM2.5': 6410, 'NVPM2.5': 6411, 'VPM1': 6420, 'NVPM1': 6421, 'H+': 648, 'Heptachlor Epoxide': 652, 'Hg-reactive': 653, 'Back scattering': 66, 'Mo': 661, 'NH4+': 664, 'NO3-': 666, 'Kj-N': 667, 'HNO3+NO3': 67, 'PCB-114': 673, 'PCB-141': 679, 'NH3+NH4': 68, 'PCB-157': 683, 'PCB-167': 684, 'PCB-170': 685, 'PCB-183': 689, 'Radioactivity': 69, 'PCB-187': 690, 'PCB-189': 691, 'PCB-194': 692, 'PCB-206': 693, 'PCB-209': 694, 'PCB-33': 698, 'PCB-37': 699, 'O3': 7, 'PCB-47': 700, 'PCB-60': 704, 'PCB-66': 705, 'PCB-74': 706, 'PCB-99': 707, 'PCB_122': 708, 'PCB_123': 709, 'CO2': 71, 'PCB_128': 710, 'PCB_138': 711, 'SO4--': 719, 'SO4-- corr': 720, 'TI': 723, 'Vanadium': 728, '1-Methyl anthracene': 7301, '1-Methyl Naphthalene': 7309, '1-Methyl phenanthrene': 7310, '2-Methyl anthracene': 7313, '2-Methyl Naphthalene': 7315, '2-Methyl phenanthrene': 7317, 'Acenaphthylene': 7352, 'cis-NO': 736, 'Cyclopenta(c,d)pyrene': 7417, 'Dibenzo(ah+ac)anthracene': 7418, 'Naphthalene': 7465, 'Benzo(b+j)fluoranthene': 7480, '4.5-Methylene phenanthrene': 7521, '5-Methyl Chrysene': 7522, '9-Methyl anthracene': 7523, 'Benzo(b)naphtho(2,1-d)thiophene': 7524, 'Benzo(c)phenanthrene': 7525, 'Cholanthrene': 7526, 'Dibenzo(ac)anthracene': 7527, 'Dibenzo(al)pyrene': 7528, 'precip_amount': 753, 'precip_amount_off': 754, 'trans_NO': 758, 'Benzo(j)fluorene': 761, 'EC': 771, 'OC': 772, 'C6H4-(CH3)2': 78, 'NO2': 8, 'p-C6H4(CH3)2': 80, 'm-C6H4-(CH3)2': 81, 'trans-H3C-HC=CH-CH2-CH3': 82, 'cis-H3C-HC=CH-CH2-CH3': 83, 'NOX as NO2': 9}


# TODO : indagare meglio quali sono gli effettivi anni supportati
def get_supported_years():
    """
    Return all the EEA supported years.

    Returns
    ----------
    list
    """
    return list(range(2013,2022))


def get_supported_countries():
    """
    Return all the EEA supported countries, represented in the code notation.

    Returns
    ----------
    list
    """
    return list(get_supported_countries_cities_dict().keys())


def get_supported_cities():
    """
    Return all the EEA supported cities.

    Returns
    ----------
    list
    """
    supported_countries_cities_dict = {country:cities
                                       for (country,cities) in get_supported_countries_cities_dict().items()
                                       if cities}
    return [ city for (country,cities) in supported_countries_cities_dict.items() for city in cities ]


def get_supported_countries_dict():
    """
    Return the dict that maps the supported-countries code notations and their associated extended notations.

    Returns
    ----------
    dict

    Notes
    ----------
    Each country has both a different code notation and a different extended notation.
    """
    return {'AD': 'Andorra', 'AL': 'Albania', 'AT': 'Austria', 'BA': 'Bosnia and Herzegovina', 'BE': 'Belgium', 'BG': 'Bulgaria', 'CH': 'Switzerland', 'CY': 'Cypern', 'CZ': 'Czech Republic', 'DE': 'Germany', 'DK': 'Denmark', 'EE': 'Estonia', 'ES': 'Spain', 'FI': 'Finland', 'FR': 'France', 'GB': 'United Kingdom', 'GI': 'Gibraltar', 'GR': 'Greece', 'HR': 'Croatia', 'HU': 'Hungary', 'IE': 'Ireland', 'IS': 'Island', 'IT': 'Italy', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LV': 'Latvia', 'ME': 'Montenegro', 'MK': 'former Yogoslav Republic of Macedonia, the', 'MT': 'Malta', 'NL': 'Netherlands', 'NO': 'Norway', 'PL': 'Poland', 'PT': 'Portugal', 'RO': 'Romania', 'RS': 'Serbia', 'SE': 'Sweden', 'SI': 'Slovenia', 'SK': 'Slovakia', 'TR': 'Turkey', 'XK': 'Kosovo'}


def get_supported_countries_inverse_dict():
    """
    Return the dict that maps the supported-countries extended notations and their associated code notations.

    Returns
    ----------
    dict
    """
    return { country:id for (id,country) in get_supported_countries_dict().items() }


def get_supported_countries_cities_dict():
    """
    Return the dict that maps the supported-countries code notations and their associated list of cities.

    Returns
    ----------
    dict
        Dictionary which has as keys the supported countries and as values the associated list of cities.

    Notes
    ----------
    There are countries without supported cities: these countries have simply associated an empty list.
    """
    # TODO : prendere ciò da fonti più auteroveli del mero file Javascript
    supported_countries_cities_dict = {'AT': ['Graz', 'Innsbruck', 'Klagenfurt', 'Linz', 'Salzburg', 'Wien'], 'BE': ['Antwerpen', 'Brugge', 'Bruxelles / Brussel', 'Charleroi', 'Gent', 'Kortrijk', 'Leuven', 'Liège', 'Mons', 'Namur'], 'BG': ['Blagoevgrad', 'Burgas', 'Dobrich', 'Haskovo', 'Pazardzhik', 'Pernik', 'Pleven', 'Plovdiv', 'Ruse', 'Shumen', 'Sliven', 'Sofia', 'Stara Zagora', 'Varna', 'Veliko Tarnovo', 'Vidin', 'Vratsa'], 'CH': ['Basel', 'Bern', 'Genève', 'Lausanne', 'Lugano', 'Luzern', 'St. Gallen', 'Winterthur', 'Zürich'], 'CY': ['Lefkosia', 'Lemesos'], 'CZ': ['Brno', 'Ceské Budejovice', 'Chomutov-Jirkov', 'Havírov', 'Hradec Králové', 'Jihlava', 'Karlovy Vary', 'Karviná', 'Kladno', 'Liberec', 'Most', 'Olomouc', 'Ostrava', 'Pardubice', 'Plzen', 'Praha', 'Ústí nad Labem', 'Zlín'], 'DE': ['Aachen', 'Aschaffenburg', 'Augsburg', 'Bamberg', 'Bayreuth', 'Berlin', 'Bielefeld', 'Bochum', 'Bonn', 'Bottrop', 'Brandenburg an der Havel', 'Braunschweig', 'Bremen', 'Bremerhaven', 'Celle', 'Chemnitz', 'Cottbus', 'Darmstadt', 'Dessau-Roßlau', 'Dortmund', 'Dresden', 'Duisburg', 'Düsseldorf', 'Erfurt', 'Erlangen', 'Essen', 'Esslingen am Neckar', 'Flensburg', 'Frankenthal (Pfalz)', 'Frankfurt (Oder)', 'Frankfurt am Main', 'Freiburg im Breisgau', 'Friedrichshafen', 'Fulda', 'Fürth', 'Gelsenkirchen', 'Gera', 'Gießen', 'Görlitz', 'Göttingen', 'Hagen', 'Halle an der Saale', 'Hamburg', 'Hamm', 'Hanau', 'Hannover', 'Heidelberg', 'Heilbronn', 'Herne', 'Hildesheim', 'Ingolstadt', 'Iserlohn', 'Jena', 'Kaiserslautern', 'Karlsruhe', 'Kassel', 'Kempten (Allgäu)', 'Kiel', 'Koblenz', 'Köln', 'Konstanz', 'Krefeld', 'Landshut', 'Leipzig', 'Leverkusen', 'Lübeck', 'Ludwigsburg', 'Ludwigshafen am Rhein', 'Lüneburg', 'Magdeburg', 'Mainz', 'Mannheim', 'Marburg', 'Moers', 'Mönchengladbach', 'Mülheim a.d.Ruhr', 'München', 'Münster', 'Neubrandenburg', 'Neumünster', 'Neuss', 'Neu-Ulm', 'Nürnberg', 'Oberhausen', 'Offenbach am Main', 'Offenburg', 'Oldenburg (Oldenburg)', 'Osnabrück', 'Paderborn', 'Passau', 'Pforzheim', 'Plauen', 'Potsdam', 'Recklinghausen', 'Regensburg', 'Remscheid', 'Reutlingen', 'Rostock', 'Saarbrücken', 'Salzgitter', 'Schweinfurt', 'Schwerin', 'Siegen', 'Solingen', 'Speyer', 'Stralsund', 'Stuttgart', 'Trier', 'Tübingen', 'Ulm', 'Villingen-Schwenningen', 'Weimar', 'Wetzlar', 'Wiesbaden', 'Witten', 'Wolfsburg', 'Wuppertal', 'Würzburg', 'Zwickau'], 'DK': ['Aalborg', 'Århus', 'København', 'Odense'], 'EE': ['Narva', 'Tallinn', 'Tartu'], 'ES': ['A Coruña', 'Albacete', 'Alcalá de Henares', 'Alcobendas', 'Alcorcón', 'Algeciras', 'Alicante/Alacant', 'Almería', 'Arrecife', 'Avilés', 'Badajoz', 'Barcelona', 'Benidorm', 'Bilbao', 'Burgos', 'Cáceres', 'Cádiz', 'Cartagena', 'Castellón de la Plana/Castelló de la Plana', 'Ciudad Real', 'Córdoba', 'Coslada', 'Dos Hermanas', 'Elche/Elx', 'Elda', 'Ferrol', 'Gandia', 'Getafe', 'Gijón', 'Girona', 'Granada', 'Granollers', 'Guadalajara', 'Jaén', 'Jerez de la Frontera', 'Las Palmas', 'Leganés', 'León', 'Línea de la Concepción, La', 'Lleida', 'Logroño', 'Lugo', 'Madrid', 'Majadahonda', 'Málaga', 'Manresa', 'Marbella', 'Mataró', 'Mollet del Vallès', 'Móstoles', 'Murcia', 'Ourense', 'Oviedo', 'Palencia', 'Palma de Mallorca', 'Pamplona/Iruña', 'Ponferrada', 'Pontevedra', 'Reus', 'Salamanca', 'San Fernando', 'San Sebastián/Donostia', 'Santa Cruz de Tenerife', 'Santander', 'Santiago de Compostela', 'Sevilla', 'Talavera de la Reina', 'Tarragona', 'Telde', 'Terrassa', 'Toledo', 'Torrejón de Ardoz', 'Torrevieja', 'Valencia', 'Valladolid', 'Vigo', 'Viladecans', 'Vilanova i la Geltrú', 'Vitoria/Gasteiz', 'Zamora', 'Zaragoza'], 'FI': ['Helsinki / Helsingfors', 'Jyväskylä', 'Kuopio', 'Lahti / Lahtis', 'Oulu / Uleåborg', 'Tampere / Tammerfors', 'Turku / Åbo'], 'FR': ['Aix-en-Provence', 'Ajaccio', 'Albi', 'Amiens', 'Angers', 'Angoulème', 'Annecy', 'Annemasse', 'Argenteuil - Bezons', 'Arras', 'Aubagne', 'Avignon', 'Bayonne', 'Beauvais', 'Belfort', 'Besançon', 'Bordeaux', 'Boulogne-sur-mer', 'Bourges', 'Brest', 'Brive-la-Gaillarde', 'CA de Sophia-Antipolis', "CA Europ' Essonne", 'CA Sénart - Val de Seine', 'Caen', 'Calais', 'Cergy-Pontoise', 'Châlons-en-Champagne', 'Chalon-sur-Saône', 'Chambery', 'Charleville-Mézières', 'Chartres', 'Châteauroux', 'Cherbourg', 'Clermont-Ferrand', 'Colmar', 'Compiègne', 'Creil', 'Dijon', 'Douai', 'Dunkerque', 'Evreux', 'Evry', 'Fort-de-France', 'Fréjus', 'Grenoble', 'Hénin - Carvin', 'La Rochelle', 'Le Havre', 'Le Mans', 'Lens - Liévin', 'Lille', 'Limoges', 'Lorient', 'Lyon', 'Mantes en Yvelines', 'Marne la Vallée', 'Marseille', 'Martigues', 'Melun', 'Metz', 'Montbelliard', 'Montpellier', 'Mulhouse', 'Nancy', 'Nantes', 'Nice', 'Nimes', 'Niort', 'Orléans', 'Paris', 'Pau', 'Perpignan', 'Poitiers', 'Quimper', 'Reims', 'Rennes', 'Roanne', 'Rouen', 'Saint Denis', 'Saint-Brieuc', 'Saint-Etienne', 'Saint-Nazaire', 'Saint-Quentin', 'Strasbourg', 'Tarbes', 'Toulon', 'Toulouse', 'Tours', 'Troyes', 'Valence', 'Valenciennes', 'Vannes', 'Versailles'], 'GB': ['Aberdeen', 'Barnsley', 'Bath and North East Somerset', 'Bedford', 'Belfast', 'Blackburn with Darwen', 'Blackpool', 'Bournemouth', 'Bradford', 'Brighton and Hove', 'Bristol', 'Burnley', 'Cambridge', 'Cannock Chase', 'Cardiff', 'Carlisle', 'Cheshire West and Chester', 'Chesterfield', 'Coventry', 'Crawley', 'Darlington', 'Derby', 'Derry', 'Doncaster', 'Dundee City', 'East Staffordshire', 'Eastbourne', 'Edinburgh', 'Exeter', 'Falkirk', 'Glasgow', 'Gloucester', 'Greater Manchester', 'Greater Nottingham', 'Halton', 'Hartlepool', 'Hyndburn', 'Kingston-upon-Hull', 'Kirklees', 'Leeds', 'Leicester', 'Lincoln', 'Lisburn', 'Liverpool', 'London', 'Luton', 'Maidstone', 'Mansfield', 'Medway', 'Middlesbrough', 'Milton Keynes', 'Newport', 'North East Lincolnshire', 'North Lanarkshire', 'Northampton', 'Norwich', 'Oxford', 'Plymouth', 'Portsmouth', 'Preston', 'Reading', 'Rotherham', 'Sheffield', 'Slough', 'Southampton', 'Southend-on-Sea', 'St Albans', 'Stevenage', 'Stockton-on-Tees', 'Stoke-on-trent', 'Sunderland', 'Swansea', 'Swindon', 'Telford and Wrekin', 'Thurrock', 'Tyneside conurbation', 'Wakefield', 'Warrington', 'Warwick', 'West Midlands urban area', 'Wirral', 'Worthing', 'Wrexham', 'York'], 'GR': ['Athina', 'Larisa', 'Pátra', 'Thessaloniki', 'Volos'], 'HR': ['Osijek', 'Rijeka', 'Slavonski Brod', 'Split', 'Zagreb'], 'HU': ['Budapest', 'Debrecen', 'Gyõr', 'Kecskemét', 'Miskolc', 'Nyíregyháza', 'Pécs', 'Szeged', 'Szombathely'], 'IE': ['Cork', 'Dublin', 'Galway', 'Limerick', 'Waterford'], 'IS': ['Reykjavík'], 'IT': ['Ancona', 'Asti', 'Avellino', 'Bari', 'Barletta', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano', 'Brescia', 'Busto Arsizio', 'Cagliari', 'Campobasso', 'Carrara', 'Caserta', 'Catania', 'Catanzaro', 'Como', 'Cosenza', 'Cremona', 'Ferrara', 'Firenze', 'Foggia', 'Forlì', 'Genova', 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Massa', 'Messina', 'Milano', 'Modena', 'Napoli', 'Novara', 'Padova', 'Palermo', 'Parma', 'Pavia', 'Perugia', 'Pesaro', 'Pescara', 'Piacenza', 'Pisa', 'Pordenone', 'Potenza', 'Prato', 'Ravenna', 'Reggio di Calabria', "Reggio nell'Emilia", 'Rimini', 'Roma', 'Salerno', 'Sanremo', 'Sassari', 'Savona', 'Siracusa', 'Taranto', 'Terni', 'Torino', 'Trento', 'Treviso', 'Trieste', 'Udine', 'Varese', 'Venezia', 'Verona', 'Viareggio', 'Vicenza', 'Vigevano'], 'LT': ['Kaunas', 'Klaipeda', 'Panevežys', 'Šiauliai', 'Vilnius'], 'LU': ['Luxembourg'], 'LV': ['Liepaja', 'Riga'], 'MT': ['Valletta'], 'NL': ['Amsterdam', 'Apeldoorn', 'Breda', 'Dordrecht', 'Eindhoven', 'Enschede', 'Groningen', 'Haarlem', 'Heerlen', 'Hilversum', 'Leiden', 'Nijmegen', 'Rotterdam', "'s-Gravenhage", 'Utrecht'], 'NO': ['Bergen', 'Kristiansand', 'Oslo', 'Stavanger', 'Tromsø', 'Trondheim'], 'PL': ['Bialystok', 'Bielsko-Biala', 'Bydgoszcz', 'Chelm', 'Czestochowa', 'Elblag', 'Elk', 'Gdansk', 'Gdynia', 'Glogów', 'Gniezno', 'Górnoslaski Zwiazek Metropolitalny', 'Gorzów Wielkopolski', 'Grudziadz', 'Inowroclaw', 'Jastrzebie-Zdrój', 'Jelenia Góra', 'Kalisz', 'Kielce', 'Konin', 'Koszalin', 'Kraków', 'Legnica', 'Leszno', 'Lódz', 'Lomza', 'Lubin', 'Lublin', 'Nowy Sacz', 'Olsztyn', 'Opole', 'Ostrów Wielkopolski', 'Pabianice', 'Pila', 'Piotrków Trybunalski', 'Plock', 'Poznan', 'Przemysl', 'Radom', 'Rybnik', 'Rzeszów', 'Siedlce', 'Slupsk', 'Stalowa Wola', 'Stargard Szczecinski', 'Suwalki', 'Swidnica', 'Szczecin', 'Tarnów', 'Tczew', 'Tomaszów Mazowiecki', 'Torun', 'Walbrzych', 'Warszawa', 'Wloclawek', 'Wroclaw', 'Zamosc', 'Zgierz', 'Zielona Góra', 'Zory'], 'PT': ['Aveiro', 'Braga', 'Coimbra', 'Faro', 'Funchal', 'Guimarães', 'Lisboa', 'Paredes', 'Porto', 'Setúbal', 'Sintra', 'Vila Franca de Xira'], 'RO': ['Alba Iulia', 'Arad', 'Bacau', 'Baia Mare', 'Bistrita', 'Botosani', 'Braila', 'Brasov', 'Bucuresti', 'Buzau', 'Calarasi', 'Cluj-Napoca', 'Constanta', 'Craiova', 'Galati', 'Giurgiu', 'Iasi', 'Oradea', 'Piatra Neamt', 'Pitesti', 'Ploiesti', 'Râmnicu Vâlcea', 'Satu Mare', 'Sibiu', 'Suceava', 'Târgu Mures', 'Timisoara', 'Tulcea'], 'SE': ['Borås', 'Göteborg', 'Helsingborg', 'Jönköping', 'Linköping', 'Lund', 'Malmö', 'Norrköping', 'Örebro', 'Stockholm', 'Umeå', 'Uppsala', 'Västerås'], 'SI': ['Ljubljana', 'Maribor'], 'SK': ['Banská Bystrica', 'Bratislava', 'Košice', 'Nitra', 'Prešov', 'Trencín', 'Trnava', 'Žilina'], 'AD': [], 'AL': [], 'BA': [], 'GI': [], 'ME': [], 'MK': [], 'RS': [], 'TR': [], 'XK': []}

    return supported_countries_cities_dict




#----------------------------------------------------------------------------------------------------------------------------
# FUNCTIONS TO FILTER ONLY THE EEA SUPPORTED VALUES.


def keep_pollutants_supported(pollutants):
    """
    Keep, from the given pollutants, only the ones supported by EEA.

    Parameters
    ----------
    pollutants: list
        List of pollutants. Each pollutant can be either expressed in the numeric or textual notation.

    Returns
    ----------
    list
        A new list with only the supported pollutants. Each pollutant is expressed in the numeric notation.

    Warns
    ----------
    UserWarning
        When not supported pollutants are given.

    Notes
    ----------
    - `pollutants` can be the string "all": in this case the returned list contains all the supported pollutants.
    - In `pollutants`, if a pollutant is expressed with a textual notation that is not unique (i.e. another EEA pollutant has
      the same textual notation) that pollutant is not considered supported.
    """
    all_supported_pollutants = get_supported_pollutants()

    if pollutants=="all":
        return all_supported_pollutants

    # Transform the pollutants textual notations in numeric notations
    pollutants_inverse_dict = get_supported_pollutants_inverse_dict()
    pollutants = [ pollutants_inverse_dict[poll] if poll in pollutants_inverse_dict else poll for poll in pollutants  ]

    pollutants = list(dict.fromkeys(pollutants)) # Remove the duplicates, keeping the order

    # Pollutants not supported by EEA
    pollutants_dif = [ pollutant for pollutant in pollutants if not pollutant in all_supported_pollutants]

    if len(pollutants_dif)>0:
        warnings.warn("The pollutants "+str(pollutants_dif)+" are not supported by EEA")
        return [ pollutant for pollutant in pollutants if not pollutant in pollutants_dif ] # Only the supported pollutants

    return pollutants


def keep_years_supported(years):
    """
    Keep, from the given years, only the ones supported by EEA.

    Parameters
    ----------
    years: list
        List of years.

    Returns
    ----------
    list
        A new list with only the supported years.

    Warns
    ----------
    UserWarning
        When not supported years are given.
    """
    years = list(dict.fromkeys(years)) # Remove the duplicates, keeping the order
    all_supported_years = get_supported_years()
    years_dif = [ year for year in years if not year in all_supported_years] # Years not supported by EEA

    if len(years_dif)>0:
        warnings.warn("The years "+str(years_dif)+" are not supported by EEA")
        return [ year for year in years if not year in years_dif] # Only the supported years

    return years


def keep_countries_cities_supported(countries_cities_dict):
    """
    Keep, from the dictionary given in input, only the countries and cities supported by EEA.

    Parameters
    ----------
    countries_cities_dict: dict
        Map between countries and list of cities. Each country can be either expressed in the code notation or in the
        extended notation.

    Returns
    ----------
    dict
        A new dictionary with only the supported countries and cities. Each country is expressed in the code notation.


    Warns
    ----------
    UserWarning
        - When not supported countries are given.
        - When not supported cities are given for a certain (supported) country.

    Notes
    ----------
    In `countries_cities_dict` a country can have associated the string "all": the returned dictionary will contain all the
    supported cities for that country.
    The whole `countries_cities_dict` can be the string "all": the returned dictionary will contain all the supported
    countries and associated cities.
    """
    # Dictionary of all the supported countries and the associated list of cities
    supported_countries_cities_dict = get_supported_countries_cities_dict()

    if countries_cities_dict=="all":
        return supported_countries_cities_dict

    countries_cities_dict = deepcopy(countries_cities_dict) # Copy the dictionary

    # Transform the country extended notations in code notations
    # (To do that is removed that dictionary entry and is put a new one)
    supported_countries_inverse_dict = get_supported_countries_inverse_dict()
    extended_notation_countries = [country
                                   for country in countries_cities_dict.keys()
                                   if country in supported_countries_inverse_dict]
    if len(extended_notation_countries)>0:
        for country in extended_notation_countries:
            countries_cities_dict[supported_countries_inverse_dict[country]] = countries_cities_dict.pop(country)

    # Remove the non-supported countries
    not_supported_countries = [country
                               for country in countries_cities_dict.keys()
                               if not country in supported_countries_cities_dict]
    if len(not_supported_countries)>0:
        warnings.warn("The countries "+str(list(not_supported_countries))+" are not supported by EEA")
        for country in not_supported_countries:
            del countries_cities_dict[country]

    # Iterate through all the countries
    for country in countries_cities_dict:
        if countries_cities_dict[country]=="all":
            countries_cities_dict[country]=supported_countries_cities_dict[country]
            continue

        cities = countries_cities_dict[country] # Specified cities for that country
        cities = list(dict.fromkeys(cities)) # Remove the cities duplicates, keeping the order

        supported_cities = supported_countries_cities_dict[country] # Supported cities for that country

        if not supported_cities: # Country without supported cities
            if len(cities)>0:
                warnings.warn("The cities "+str(cities)+" are not supported by EEA for the country "+country)
            countries_cities_dict[country] = [] # Set empty list
            continue

        not_supported_cities = [ city for city in cities if not city in supported_cities ] # Not supported cities

        if len(not_supported_cities)>0: # At least one not-supported city
            warnings.warn("The cities "+str(not_supported_cities)+" are not supported by EEA for the country "+country)
            # Overwrite the dictionary entry
            countries_cities_dict[country] = [ city for city in cities if not city in not_supported_cities]

    return countries_cities_dict




#----------------------------------------------------------------------------------------------------------------------------
# FUNCTIONS TO DOWNLOAD AND HANDLE THE EEA DATASETS


def download_datasets(dest_path, countries_cities_dict, pollutants, years):
    """
    Download the selected EEA air pollution datasets in the specified local path.

    The EEA datasets are csv files.

    Parameters
    ----------
    dest_path : str
    countries_cities_dict : dict
        Map between countries and list of cities. Each country can be either expressed in the code notation or in the
        extended notation.
    pollutants : list
        List of pollutants. Each pollutant can be either expressed in the numeric notation or in the textual notation.
    years : list
        List of years.

    Warns
    ----------
    UserWarning
        - When not supported countries/cities/pollutants/years are given.
        - When, for a specified country, no dataset has been downloaded.
        - When some problem occurs during an HTTP request. (I.e. a problem during the downloading of certain datasets).

    Notes
    ---------
    In `countries_cities_dict` a country can be associated with  the string "all": in this case all the supported cities of
    that country are taken into account.
    In addition, the whole `countries_cities_dict` can be the string "all": in this case all the supported countries and
    associated cities are considered.
    Also `pollutants` can be "all", which means that all the supported pollutants are taken into account.
    """

    pollutants = keep_pollutants_supported(pollutants)
    years = keep_years_supported(years)
    countries_cities_dict = keep_countries_cities_supported(countries_cities_dict)

    supported_countries_cities_dict = get_supported_countries_cities_dict()

    # Iterate through all the countries
    for country in countries_cities_dict.keys():
        downloaded = False # Flag which indicates if at least one dataset has been downloaded for that country

        if not supported_countries_cities_dict[country]:
            # Country without supported cities -> download all the datasets of that country (related to these pollutants and
            # years)
            downloaded = _download_single_dataset(dest_path,country,None,pollutants,years)
        else:
            # Iterate through all the cities, and download all the datasets of that city
            for city in countries_cities_dict[country]:
                downloaded = downloaded | _download_single_dataset(dest_path,country,city,pollutants,years)

        if not downloaded: # No datasets have been downloaded for that country
            warnings.warn(("Data have not been found for the country "+country+
                           " for the pollutants "+str(pollutants)+
                           " for the years "+str(years)))


def _download_single_dataset(dest_path, country, city, pollutants, years):
    """
    Download the EEA air pollution datasets of the selected country/city in the specified local path.

    The EEA datasets are csv files.
    This function is meant to be private in the module.

    Parameters
    ----------
    dest_path : str
    country: str
        A specific country, expressed in the code notation.
    city: str
        A specific city of that country.
    pollutants : list
        List of pollutants, expressed in the numeric notation.
    years : list
        List of years.

    Returns
    ----------
    bool
        True if at least one dataset is download for that country/city, False otherwise.

    Warns
    ----------
    UserWarning
        When some problem occurs during an HTTP request. (I.e. a problem during the downloading of certain datasets).

    Notes
    ---------
    - No check is done on the input parameters `country`/`city`/`pollutants`/`years`: the caller of the function
      must ensure to pass in input only supported values.
    - `city` can be None. In this case all the datasets of that country are downloaded.
      This option is meant to be used only for the countries that haven't associated supported cities (e.g. AD): the caller
      of the function must ensure that.
    """
    # Base EEA URL, used to download the datasets
    base_url = "https://fme.discomap.eea.europa.eu/fmedatastreaming/AirQualityDownload/AQData_Extract.fmw?"

    base_path = dest_path + "\\EEA" # Base local path (i.e. EEA folder)
    country_path = base_path + "\\" + country # Country folder
    if city: # City folder
        city_supp = re.sub('[\/:*?"<>|_"]', '', city) # Remove the not lecit characters
        city_path = country_path + "\\" + city_supp

    first = True # Flag which indicates if the first dataset has not been donwloaded yet

    # Iterate through all the pollutants and years
    for pollutant in pollutants:
        for year in years:
            year = str(year)
            pollutant = str(pollutant)

            if city: # URL for that specific city of that country
                url = base_url + "CountryCode=" + country + "&CityName=" + city + "&Pollutant=" + pollutant +\
                "&Year_from=" + year + "&Year_to=" + year + \
                "&Station=&Samplingpoint=&Source=All&Output=TEXT&UpdateDate=&TimeCoverage=Year"
            else: # URL for that specific country (without any city)
                url = base_url + "CountryCode=" + country + "&CityName=&Pollutant=" + pollutant +\
                "&Year_from=" + year + "&Year_to=" + year + \
                "&Station=&Samplingpoint=&Source=All&Output=TEXT&UpdateDate=&TimeCoverage=Year"

            # HTTP request for the links of the datasets related to that country/city, pollutants and years
            try:
                r =requests.get(url)
            except:
                warnings.warn(("Something bad happened while downloading data for the country "+country+
                               (" for the city "+city if city else "")+
                               " for the pollutants "+str(pollutants)+
                               " for the years "+str(years)))
                continue

            text = r.text # String containing all the datasets links
            text = re.sub(r'^.*?https', 'https', text) # Remove initial garbage

            links = text.split() # List of links to download

            # Iterate through all the links
            for link in links:
                try:
                    r_data =requests.get(link) # Download the dataset
                except:
                    warnings.warn(("Something bad happened while downloading data for the country "+country+
                                   (" for the city "+city if city else "")+
                                   " for the pollutants "+str(pollutants)+
                                   " for the years "+str(years)))
                    continue

                # If there are not been created yet, create the folders
                # (The folders are created in a lazy manner)
                if first:
                    if not os.path.isdir(base_path):
                        os.mkdir(base_path)
                    if not os.path.isdir(country_path):
                        os.mkdir(country_path)
                    if city and (not os.path.isdir(city_path)):
                        os.mkdir(city_path)
                    first = False # Now at least one dataset has been downloaded

                # Generate the file name
                id_code = link.split("/")[-1].split("_")[2] # station id
                if city: # File name with the city
                    city_supp = re.sub('[\/:*?"<>|_"]', '', city)
                    file_path = city_path + "\\" + country+"_"+city_supp+"_"+pollutant+"_"+year+"_"+id_code + ".csv"
                else:    # File name without the city
                    file_path = country_path + "\\" + country+"_"+pollutant+"_"+year+"_"+id_code + ".csv"

                # Save the csv file (If it alredy exits, overwrite it)
                file = open(file_path,"wb")
                file.write(r_data.content)
                file.close()


    return not first


def retrieve_datasets(source_path, countries_cities_dict, pollutants, years):
    """
    Retrieve the selected EEA air pollution datasets from the local storage.

    The EEA datasets are csv files.

    Parameters
    ----------
    source_path : str
        Local path in which the selected datasets are searched.
    countries_cities_dict : dict
        Map between countries and list of cities. Each country can be either expressed in the code notation or in the
        extended notation.
    pollutants : list
        List of pollutants. Each pollutant can be either expressed in the numeric notation or in the textual notation.
    years : list
        List of years.

    Returns
    ----------
    list
        List of the retrieved datasets. Each dataset is represented as a string (i.e. his local path).

    Warns
    ----------
    UserWarning
        - When not supported countries/pollutants/years are given.
        - When, for a specified country, no dataset has been found.

    Notes
    ---------
    In `countries_cities_dict` a country can be associated with the string "all": in this case all the supported cities of
    that country are taken into account.
    In addition, the whole `countries_cities_dict` can be the string "all": in this case all the supported countries and
    associated cities are considered.
    Also `pollutants` can be "all", which means that all the supported pollutants are taken into account.
    """


    def retrieve_files(source_path, keywords):
        """
        Retrieve all the local files whose path names match the specified keywords.

        Parameters
        ----------
        source_path: str
            Local path in which the files are searched.
        keywords: list
            List of tuples, in which each tuple contains an indefinite number of strings.
            These strings can be seen as the keywords.

        Returns
        ----------
        list
            List of the retrieved files. Each file is represented as a string (i.e. his local path).

        Notes
        ----------
        A file is selected if at least one of the tuples in 'keyword' have all his strings that are contained in the local
        path name of the file.
        It's like that the strings inside the same tuple are in logical AND, instead different tuples are in logical OR.
        """
        # List of the files local paths to return in output
        all_files = list()

        # List of files and subdirectories. The names are relative paths.
        list_of_file = os.listdir(source_path)

        # Iterate through all the entries
        for entry in list_of_file:
            # Create full path
            full_path = os.path.join(source_path, entry)
            # If the entry is a subdirectory, apply the function recursively
            if os.path.isdir(full_path):
                all_files = all_files + retrieve_files(full_path,keywords)
            elif entry.endswith('.csv') and any([all([ keyword in entry for keyword in keywords_tuple])\
                                                     for keywords_tuple in keywords]): # Match
                all_files.append(full_path)

        return all_files


    # List of the files local paths to return in output
    all_files = []

    pollutants = keep_pollutants_supported(pollutants)
    years = keep_years_supported(years)
    countries_cities_dict = keep_countries_cities_supported(countries_cities_dict)

    # Dictionary of all the supported countries and the associated list of cities
    supported_countries_cities_dict = get_supported_countries_cities_dict()

    # List containing the countries/cities (strings) to search.
    # For the countries without supported cities is simply put the code country (e.g. "AD").
    # Otherwise, is put the string "country_city" for each specified city for that country. (e.g. "IT_Milano")
    countries_cities = []
    for country in countries_cities_dict: # Iterate through all the specified countries
        if not supported_countries_cities_dict[country]: # Country without supported cities: put only the code country
            countries_cities.append(country)
        else:
            # Put all the cities of that country ("country_city" for each specified city).
            # It can alse be an empty list.
            countries_cities += [country+"_"+re.sub('[\/:*?"<>|_"]', '', city) for city in countries_cities_dict[country]]

    if len(countries_cities)==0 or len(pollutants)==0 or len(years)==0: # Nothing to search
        return []

    keywords = [] # List of tuples of strings, which are the keywords.

    for country_city in countries_cities:
        for pollutant in pollutants:
            for year in years:
                # Two strings in each tuple: country/city and pollutant+year
                keywords.append((country_city+"_","_"+str(pollutant)+"_"+str(year)+"_"))

    all_files = retrieve_files(source_path, keywords) # Take all the files that match the keywords

    # Make the warnings
    for country in countries_cities_dict:
        if all([country+"_" not in file for file in all_files]):
            warnings.warn(("Data have not been found for the country "+country+
                           " for the pollutants "+str(pollutants)+
                           " for the years "+str(years)))

    return all_files


def remove_datasets(source_path, countries_cities_dict, pollutants, years):
    """
    Delete the selected EEA air pollution datasets from the local storage.
    (The EEA datasets are csv files).

    Parameters
    ----------
    source_path : str
        Local path from which the selected datasets are removed.
    countries_cities_dict : dict
        Map between countries and list of cities. Each country can be either expressed in the code notation or in the
        extended notation.
    pollutants : list
        List of pollutants. Each pollutant can be either expressed in the numeric notation or in the textual notation.
    years : list
        List of years.

    Warns
    ----------
    UserWarning
        - When not supported countries/pollutants/years are given.
        - When, for a specified country, no dataset has been found.

    Notes
    ---------
    In `countries_cities_dict` a country can be associated with the string "all": in this case all the supported cities of
    that country are taken into account.
    In addition, the whole `countries_cities_dict` can be the string "all": in this case all the supported countries and
    associated cities are considered.
    Also `pollutants` can be "all", which means that all the supported pollutants are taken into account.
    """

    list_of_files = retrieve_datasets(source_path,countries_cities_dict,pollutants,years)

    for file in list_of_files:
        os.remove(file)


def load_datasets(source_path, countries_cities_dict, pollutants, years):
    """
    Load the selected EEA air pollution datasets, retrieved from the local storage, into a single pandas DataFrame.
    (The EEA datasets are csv files).

    The returned DataFrame is a raw DataFrame. This means two things.
        1. The DataFrame simply contains air pollution concentration measurements, which are not properly grouped by their
           days.
        2. The values in the DataFrame have not been cleaned.

    Parameters
    ----------
    source_path : str
        Local path in which the selected datasets are searched.
    countries_cities_dict : dict
        Map between countries and list of cities. Each country can be either expressed in the code notation or in the
        extended notation.
    pollutants : list
        List of pollutants. Each pollutant can be either expressed in the numeric notation or in the textual notation.
    years : list
        List of years.

    Returns
    ----------
    pd.DataFrame
        DataFrame containing all the selected datasets.

    Warns
    ----------
    UserWarning
        - When not supported countries/pollutants/years are given.
        - When, for a specified country, no dataset has been found.
        - When no dataset at all has been found.

    Notes
    ---------
    In `countries_cities_dict` a country can be associated with the string "all": in this case all the supported cities of
    that country are taken into account.
    In addition, the whole `countries_cities_dict` can be the string "all": in this case all the supported countries and
    associated cities are considered.
    Also `pollutants` can be "all", which means that all the supported pollutants are taken into account.
    """

    list_of_files = retrieve_datasets(source_path,countries_cities_dict,pollutants,years)

    if len(list_of_files)==0:
        warnings.warn("No data have been found")

    dataframe_list = []
    for file in list_of_files:
        dataframe_list.append(pd.read_csv(file))

    return pd.concat(dataframe_list,ignore_index=True)


def preprocessing(df, fill=True, fill_n_days=10, fill_aggr="mean"):
    """
    Prepare and clean the given raw EEA DataFrame, grouping the air pollution concentration measurements by day.

    Return three DataFrames. All of these DataFrames are indexed by dayes and all of them have only one column.
    But:
        - the first DataFrame contains, for each day, the daily mean concentration;
        - the second contains, for each day, the daily min concentration;
        - the third contains, for each day, the daily max concentration.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to clean. It's a raw EEA DataFrame, loaded using the load_datasets function.
    fill : bool
        If True, the missing days (i.e. the days in `df` without any measurement) are filled. Otherwise, they remain with a
        missing value.
        (In all the three returned DataFrame)
    fill_n_days : int or str
        The number of preceding  days, contained in `df`, used to fill a missing day.
        `fill_n_days` can be either an integer or the string "all": in the latter case all the preceding  days in `df` are
        used to fill the missing days.
    fill_aggr : str
        The statistic aggregation used to fill a missing day.
        It can be either "mean" or "min" or "max".

    Returns
    ----------
    pd.DataFrame
        The prepared and cleaned DataFrame, containing the daily mean concentrations.
    pd.DataFrame
        The prepared and cleaned DataFrame, containing the daily min concentrations.
    pd.DataFrame
        The prepared and cleaned DataFrame, containing the daily max concentrations.

    Warns
    ----------
    UserWarning
        When missing days are contained in `df`.

    Notes
    ---------
    - If `fill` is True, the missing days are filled computing the aggregation `fill_aggr` on the `fill_n_days` days in `df`
      preceding the missing day.
      (In all the three returned DataFrame)
      Moreover, the missing days for which no preceding day has been found in `df` are deleted from the returned DataFrames.
      These days are surely the first days in `df`.
    - The returned DataFrames are indexed by days. In particular, are used the pandas built-in types: the index type is
      pd.DatetimeIndex.
    """

    def find_missing_days(days):
        """
        Return, given a vector of days, his missing days.

        More specifically, the missing days are the ones which are not present in the contigous sequence of days in `days`.

        Parameters
        ----------
        days: pd.DatetimeIndex
            Vector of dates.

        Returns
        ----------
        pd.DatetimeIndex
            Vector of missing days.
        """
        day_min = min(days)
        day_max = max(days)

        return pd.date_range(start=day_min,end=day_max).difference(days)


    df = df.copy()

    # Remove invalid values
    df = df[df["Validity"]>0] # Validity 1 and 3
    df = df[~df["Concentration"].isna()]
    df = df[df["Concentration"]>=0]

    df["Datetime"] = df["DatetimeBegin"].map(lambda data : data.split()[0]) # Group the measurements by date
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.groupby("Datetime")["Concentration"].agg(["mean","min","max"]) # Create three columns : "mean","min","max"

    missing_days = find_missing_days(df.index) # Missing days : they are "holes" in the contiguous sequence of days

    if len(missing_days)>0:
        warnings.warn("Missing days: "+str(list(missing_days.strftime('%Y-%m-%d'))))

    if fill: # Fill the missing days
        # Days to remove in the final DataFrames, because they are missing days and no preceding days have been found in `df`
        days_to_remove = []

        for miss_day in missing_days: # Iterate through all the missing days
            nearest_days = [d for d in df.index if d<miss_day] # All the days in `df` preceding that missing day
            if fill_n_days!="all":
                nearest_days = nearest_days[::-1][:fill_n_days] # keep only the specified number of preceding days
            if len(nearest_days)==0: # Missing day without preceding days: it's a day to remove
                days_to_remove.append(miss_day)

            # Fill the missing day
            if fill_aggr=="mean":
                df.loc[miss_day] = df.loc[nearest_days].mean()
            elif fill_aggr=="min":
                df.loc[miss_day] = df.loc[nearest_days].min()
            elif fill_aggr=="max":
                df.loc[miss_day] = df.loc[nearest_days].max()

        df = df.drop(days_to_remove) # Remove the days

    else: # Not fill the missing days
        for miss_day in missing_days:
            df.loc[miss_day] = float("Nan")

    df = df.sort_index()

    return pd.DataFrame(df["mean"]),pd.DataFrame(df["min"]),pd.DataFrame(df["max"]) # Return three dataframes
