#!/bin/usr/python

# GADMPostProc.data

# Alpa-3 code to English short name mapping
## Based on https://www.iso.org/obp/ui/#search/code/
## Accessed on May, the 20th of 2023
code2country = {
        'AUS': 'Australia',
        'BGD': 'Bangladesh',
        'BRN': 'Brunei Darussalam',
        'BTN': 'Bhutan',
        'CHN': 'China',
        'COK': 'Cook Islands (the)',
        'CXR': 'Christmas Island',
        'HKG': 'Hong Kong',
        'IDN': 'Indonesia',
        'IND': 'India',
        'KHM': 'Cambodia',
        'LAO': "Lao People's Democratic Republic (the)",
        'LKA': 'Sri Lanka',
        'MMR': 'Myanmar',
        'MYS': 'Malaysia',
        'NPL': 'Nepal',
        'PHL': 'Philippines (the)',
        'PLW': 'Palau',
        'PNG': 'Papua New Guinea',
        'SGP': 'Singapore',
        'SLB': 'Solomon Islands',
        'THA': 'Thailand',
        'TLS': 'Timor-Leste',
        'TWN': 'Taiwan (Province of China)',
        'VNM': 'Viet Nam',
        }
'''
Aruba ABW
Afghanistan AFG
Angola AGO
Anguilla AIA
Åland Islands ALA
Albania ALB
Andorra AND
United Arab Emirates (the) ARE
Argentina ARG
Armenia ARM
American Samoa ASM
Antarctica ATA
French Southern Territories (the) ATF
Antigua and Barbuda ATG
Australia AUS
Austria AUT
Azerbaijan AZE
Burundi BDI
Belgium BEL
Benin BEN
Bonaire, Sint Eustatius and Saba BES
Burkina Faso BFA
Bangladesh BGD
Bulgaria BGR
Bahrain BHR
Bahamas (the) BHS
Bosnia and Herzegovina BIH
Saint Barthélemy BLM
Belarus BLR
Belize BLZ
Bermuda BMU
Bolivia (Plurinational State of) BOL
Brazil BRA
Barbados BRB
Brunei Darussalam BRN
Bhutan BTN
Bouvet Island BVT
Botswana BWA
Central African Republic (the) CAF
Canada CAN
Cocos (Keeling) Islands (the) CCK
Switzerland CHE
Chile CHL
China CHN
Côte d'Ivoire CIV
Cameroon CMR
Congo (the Democratic Republic of the) COD
Congo (the) COG
Cook Islands (the) COK
Colombia COL
Comoros (the) COM
Cabo Verde CPV
Costa Rica CRI
Cuba CUB
Curaçao CUW
Christmas Island CXR
Cayman Islands (the) CYM
Cyprus CYP
Czechia CZE
Germany DEU
Djibouti DJI
Dominica DMA
Denmark DNK
Dominican Republic (the) DOM
Algeria DZA
Ecuador ECU
Egypt EGY
Eritrea ERI
Western Sahara ESH
Spain ESP
Estonia EST
Ethiopia ETH
Finland FIN
Fiji FJI
Falkland Islands (the) [Malvinas] FLK
France FRA
Faroe Islands (the) FRO
Micronesia (Federated States of) FSM
Gabon GAB
United Kingdom of Great Britain and Northern Ireland (the) GBR
Georgia GEO
Guernsey GGY
Ghana GHA
Gibraltar GIB
Guinea GIN
Guadeloupe GLP
Gambia (the) GMB
Guinea-Bissau GNB
Equatorial Guinea GNQ
Greece GRC
Grenada GRD
Greenland GRL
Guatemala GTM
French Guiana GUF
Guam GUM
Guyana GUY
Hong Kong HKG
Heard Island and McDonald Islands HMD
Honduras HND
Croatia HRV
Haiti HTI
Hungary HUN
Indonesia IDN
Isle of Man IMN
India IND
British Indian Ocean Territory (the) IOT
Ireland IRL
Iran (Islamic Republic of) IRN
Iraq IRQ
Iceland ISL
Israel ISR
Italy ITA
Jamaica JAM
Jersey JEY
Jordan JOR
Japan JPN
Kazakhstan KAZ
KenyaKenya (le)KEKEN404KyrgyzstanKirghizistan (le)KGKGZ417CambodiaCambodge (le)KHKHM116KiribatiKiribatiKIKIR296Saint Kitts and NevisSaint-Kitts-et-NevisKNKNA659Korea (the Republic of)Corée (la République de)KRKOR410KuwaitKoweït (le)KWKWT414Lao People's Democratic Republic (the)Lao (la République démocratique populaire)LALAO418LebanonLiban (le)LBLBN422LiberiaLibéria (le)LRLBR430LibyaLibye (la)LYLBY434Saint LuciaSainte-LucieLCLCA662LiechtensteinLiechtenstein (le)LILIE438Sri LankaSri LankaLKLKA144LesothoLesotho (le)LSLSO426LithuaniaLituanie (la)LTLTU440LuxembourgLuxembourg (le)LULUX442LatviaLettonie (la)LVLVA428MacaoMacaoMOMAC446Saint Martin (French part)Saint-Martin (partie française)MFMAF663MoroccoMaroc (le)MAMAR504MonacoMonacoMCMCO492Moldova (the Republic of)Moldova (la République de)MDMDA498MadagascarMadagascarMGMDG450MaldivesMaldives (les)MVMDV462MexicoMexique (le)MXMEX484Marshall Islands (the)Marshall (les Îles)MHMHL584North MacedoniaMacédoine du Nord (la)MKMKD807MaliMali (le)MLMLI466MaltaMalteMTMLT470MyanmarMyanmar (le)MMMMR104MontenegroMonténégro (le)MEMNE499MongoliaMongolie (la)MNMNG496Northern Mariana Islands (the)Mariannes du Nord (les Îles)MPMNP580MozambiqueMozambique (le)MZMOZ508MauritaniaMauritanie (la)MRMRT478MontserratMontserratMSMSR500MartiniqueMartinique (la)MQMTQ474MauritiusMauriceMUMUS480MalawiMalawi (le)MWMWI454MalaysiaMalaisie (la)MYMYS458MayotteMayotteYTMYT175NamibiaNamibie (la)NANAM516New CaledoniaNouvelle-Calédonie (la)NCNCL540Niger (the)Niger (le)NENER562Norfolk IslandNorfolk (l'Île)NFNFK574NigeriaNigéria (le)NGNGA566NicaraguaNicaragua (le)NINIC558NiueNiueNUNIU570Netherlands (Kingdom of the)Pays-Bas (Royaume des)NLNLD528NorwayNorvège (la)NONOR578NepalNépal (le)NPNPL524NauruNauruNRNRU520New ZealandNouvelle-Zélande (la)NZNZL554OmanOmanOMOMN512PakistanPakistan (le)PKPAK586PanamaPanama (le)PAPAN591PitcairnPitcairnPNPCN612PeruPérou (le)PEPER604Philippines (the)Philippines (les)PHPHL608PalauPalaos (les)PWPLW585Papua New GuineaPapouasie-Nouvelle-Guinée (la)PGPNG598PolandPologne (la)PLPOL616Puerto RicoPorto RicoPRPRI630Korea (the Democratic People's Republic of)Corée (la République populaire démocratique de)KPPRK408PortugalPortugal (le)PTPRT620ParaguayParaguay (le)PYPRY600Palestine, State ofPalestine, État dePSPSE275French PolynesiaPolynésie française (la)PFPYF258QatarQatar (le)QAQAT634RéunionRéunion (La)REREU638RomaniaRoumanie (la)ROROU642Russian Federation (the)Russie (la Fédération de)RURUS643RwandaRwanda (le)RWRWA646Saudi ArabiaArabie saoudite (l')SASAU682Sudan (the)Soudan (le)SDSDN729SenegalSénégal (le)SNSEN686SingaporeSingapourSGSGP702South Georgia and the South Sandwich IslandsGéorgie du Sud-et-les Îles Sandwich du Sud (la)GSSGS239Saint Helena, Ascension and Tristan da CunhaSainte-Hélène, Ascension et Tristan da CunhaSHSHN654Svalbard and Jan MayenSvalbard et l'Île Jan Mayen (le)SJSJM744Solomon IslandsSalomon (les Îles)SBSLB090Sierra LeoneSierra Leone (la)SLSLE694El SalvadorEl SalvadorSVSLV222San MarinoSaint-MarinSMSMR674SomaliaSomalie (la)SOSOM706Saint Pierre and MiquelonSaint-Pierre-et-MiquelonPMSPM666SerbiaSerbie (la)RSSRB688South SudanSoudan du Sud (le)SSSSD728Sao Tome and PrincipeSao Tomé-et-PrincipeSTSTP678SurinameSuriname (le)SRSUR740SlovakiaSlovaquie (la)SKSVK703SloveniaSlovénie (la)SISVN705SwedenSuède (la)SESWE752EswatiniEswatini (l')SZSWZ748Sint Maarten (Dutch part)Saint-Martin (partie néerlandaise)SXSXM534SeychellesSeychelles (les)SCSYC690Syrian Arab Republic (the)République arabe syrienne (la)SYSYR760Turks and Caicos Islands (the)Turks-et-Caïcos (les Îles)TCTCA796ChadTchad (le)TDTCD148TogoTogo (le)TGTGO768ThailandThaïlande (la)THTHA764TajikistanTadjikistan (le)TJTJK762TokelauTokelau (les)TKTKL772TurkmenistanTurkménistan (le)TMTKM795Timor-LesteTimor-Leste (le)TLTLS626TongaTonga (les)TOTON776Trinidad and TobagoTrinité-et-Tobago (la)TTTTO780TunisiaTunisie (la)TNTUN788TürkiyeTürkiye (la)TRTUR792TuvaluTuvalu (les)TVTUV798Taiwan (Province of China)Taïwan (Province de Chine)TWTWN158Tanzania, the United Republic ofTanzanie (la République-Unie de)TZTZA834UgandaOuganda (l')UGUGA800UkraineUkraine (l')UAUKR804United States Minor Outlying Islands (the)Îles mineures éloignées des États-Unis (les)UMUMI581UruguayUruguay (l')UYURY858United States of America (the)États-Unis d'Amérique (les)USUSA840UzbekistanOuzbékistan (l')UZUZB860Holy See (the)Saint-Siège (le)VAVAT336Saint Vincent and the GrenadinesSaint-Vincent-et-les GrenadinesVCVCT670Venezuela (Bolivarian Republic of)Venezuela (République bolivarienne du)VEVEN862Virgin Islands (British)Vierges britanniques (les Îles)VGVGB092Virgin Islands (U.S.)Vierges des États-Unis (les Îles)VIVIR850Viet NamViet Nam (le)VNVNM704VanuatuVanuatu (le)VUVUT548Wallis and FutunaWallis-et-FutunaWFWLF876SamoaSamoa (le)WSWSM882YemenYémen (le)YEYEM887South AfricaAfrique du Sud (l')ZAZAF710ZambiaZambie (la)ZMZMB
Zimbabwe ZWE
'''
# Provide the maximum precision available
maxPrecision = {
        'AUS': 2, 
        'BGD': 4, 
        'BRN': 2, 
        'BTN': 2, 
        'CHN': 3, 
        'COK': 0, 
        'CXR': 0, 
        'HKG': 1, 
        'IDN': 4, 
        'IND': 3, 
        'KHM': 4, 
        'LAO': 2, 
        'LKA': 2, 
        'MMR': 3, 
        'MYS': 2, 
        'NPL': 4, 
        'PHL': 3, 
        'PLW': 1, 
        'PNG': 2, 
        'SGP': 1, 
        'SLB': 2, 
        'THA': 3, 
        'TLS': 3, 
        'TWN': 2, 
        'VNM': 3, 
        }

# Shapefiles' name format
shp_file = 'gadm36_%s_shp/gadm36_%s_%i.shp' # %(code, code, precision)
