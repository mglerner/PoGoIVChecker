#!/usr/bin/env python

# TODO
# * Make it so that for shadows, you also see the purified IVs
# * Some PVP IV Deep Dives, like Medicham, use the "top N" pokemon in addition to stats cutoffs. We should do that or a stat product cutoff.
# * Figure out if we're actually calculating things correctly, since we disagree very slightly with pvpivs.com

import pandas as pd, numpy as np
import math, json, re
from IPython.display import display, Markdown, Latex, HTML


MOVES_FILE = 'gamemaster.json'
def get_moves():
    f = open(MOVES_FILE)
    mf = json.load(f)
    fastmoves = {i['moveId']:i for i in mf['moves'] if i['energyGain'] != 0}
    chargedmoves = {i['moveId']:i for i in mf['moves'] if i['energyGain'] == 0}
    return fastmoves, chargedmoves
def get_pokemon():
    f = open(MOVES_FILE)
    mf = json.load(f)
    # This gives you a list of pokemon dictionaries. I actually just want to look things up by name
    pokemon = {mon['speciesName']:mon for mon in mf['pokemon']}
    return pokemon

pokemon = get_pokemon()
# Kind of surprised this isn't in PvPoke
EVOLUTIONS = ( ['Spheal', 'Sealeo','Walrein'],
        ['Bulbasaur', 'Ivysaur', 'Venusaur'],
        ['Mudkip','Marshtomp','Swampert'],
        ['Hoppip','Skiploom','Jumpluff'],
        ['Deoxys (Defense)'],
        ['Seel','Dewgong'],
        ['Sandshrew','Sandslash'],
        ['Cottonee','Whimsicott'],
        ['Registeel'],
        ['Azurill','Marill','Azumarill'],
        ['Dewpider','Araquanid'],
        ['Geodude','Graveler','Golem'],
        ['Cubone','Marowak'],
        ['Zigzagoon (Galarian)','Linoone (Galarian)','Obstagoon'],
        ['Zigzagoon (Galarian)','Linoone (Galarian)'],
        ['Meditite','Medicham'],
        ['Dunsparce'],
        ['Dedenne'],
        ['Stunfisk (Galarian)'],
        ['Lickitung'],#,'Lickilicky'],
        ['Mareanie','Toxapex'],
        ['Croagunk','Toxicroak'],
        ['Phantump','Trevenant'],
        ['Hoothoot','Noctowl'],
        ['Chinchou','Lanturn'],
        ['Chespin','Quilava','Chesnaught'],
        ['Swablu','Altaria'],
        ['Yamask (Galarian)','Runerigus'],
        ['Yamask','Cofagrigus'],
        ['Slowpoke','Slowbro'],
        ['Slowpoke','Slowking'], # No need for this it's the same stats as bro.
        ['Slowpoke (Galarian)','Slowbro (Galarian)'],
        ['Slowpoke (Galarian)','Slowking (Galarian)'],
        ['Tapu Fini'],
        ['Froakie','Frogadier','Greninja'],
        ['Wooloo','Dubwool'],
        ['Wooper','Quagsire'],
        ['Wooper (Paldea)','Clodsire'],
        ['Grubbin','Charjabug'],
        ['Grubbin','Charjabug','Vikavolt'],
        ['Snorunt','Froslass'],
        ['Rowlet','Dartrix','Decidueye'],
        ['Mankey','Primeape','Annihilape'],
        ['Goomy','Sliggoo','Goodra'],
        ['Carbink',],
        )


# I definitely stole this table from https://gamepress.gg/pokemongo/cp-multiplier
def get_cpm(level):
    d = {
        1:	0.094,
        1.5: 0.1351374318,
        2: 0.16639787,
        2.5: 0.192650919,
        3: 0.21573247,
        3.5: 0.2365726613,
        4: 0.25572005,
        4.5: 0.2735303812,
        5: 0.29024988,
        5.5: 0.3060573775,
        6: 0.3210876,
        6.5: 0.3354450362,
        7: 0.34921268,
        7.5: 0.3624577511,
        8: 0.3752356,
        8.5: 0.387592416,
        9: 0.39956728,
        9.5: 0.4111935514,
        10: 0.4225,
        10.5: 0.4329264091,
        11: 0.44310755,
        11.5: 0.4530599591,
        12: 0.4627984,
        12.5: 0.472336093,
        13: 0.48168495,
        13.5: 0.4908558003,
        14: 0.49985844,
        14.5: 0.508701765,
        15: 0.51739395,
        15.5: 0.5259425113,
        16: 0.5343543,
        16.5: 0.5426357375,
        17: 0.5507927,
        17.5: 0.5588305862,
        18: 0.5667545,
        18.5: 0.5745691333,
        19: 0.5822789,
        19.5: 0.5898879072,
        20: 0.5974,
        20.5: 0.6048236651,
        21: 0.6121573,
        21.5: 0.6194041216,
        22: 0.6265671,
        22.5: 0.6336491432,
        23: 0.64065295,
        23.5: 0.6475809666,
        24: 0.65443563,
        24.5: 0.6612192524,
        25: 0.667934,
        25.5: 0.6745818959,
        26: 0.6811649,
        26.5: 0.6876849038,
        27: 0.69414365,
        27.5: 0.70054287,
        28: 0.7068842,
        28.5: 0.7131691091,
        29: 0.7193991,
        29.5: 0.7255756136,
        30: 0.7317,
        30.5: 0.7347410093,
        31: 0.7377695,
        31.5: 0.7407855938,
        32: 0.74378943,
        32.5: 0.7467812109,
        33: 0.74976104,
        33.5: 0.7527290867,
        34: 0.7556855,
        34.5: 0.7586303683,
        35: 0.76156384,
        35.5: 0.7644860647,
        36: 0.76739717,
        36.5: 0.7702972656,
        37: 0.7731865,
        37.5: 0.7760649616,
        38: 0.77893275,
        38.5: 0.7817900548,
        39: 0.784637,
        39.5: 0.7874736075,
        40: 0.7903,
        40.5: 0.792803968,
        41: 0.79530001,
        41.5: 0.797800015,
        42: 0.8003,
        42.5: 0.802799995,
        43: 0.8053,
        43.5: 0.8078,
        44: 0.81029999,
        44.5: 0.812799985,
        45: 0.81529999,
        45.5: 0.81779999,
        46: 0.82029999,
        46.5: 0.82279999,
        47: 0.82529999,
        47.5: 0.82779999,
        48: 0.83029999,
        48.5: 0.83279999,
        49: 0.83529999,
        49.5: 0.83779999,
        50: 0.84029999,
        50.5: 0.84279999,
        51: 0.84529999,        
        }
    return d[level]


OVERALL_RANK = {
    'statprod': {},
    'bulkprod': {},
    }
    
def add_to_rank(mon,max_level=40,max_cp=1500.99):
    if mon not in OVERALL_RANK['statprod']:
        OVERALL_RANK['statprod'][mon] = {}
    if mon not in OVERALL_RANK['bulkprod']:
        OVERALL_RANK['bulkprod'][mon] = {}
    stat = []
    bulk = []
    for atk in range(16):
        for defense in range(16):
            for hp in range(16):
                stats = ivs_to_stats(atk,defense,hp,
                                         my_level=10,# Just make it up since we're just ranking.
                                         mon=mon,max_level=max_level,max_cp=max_cp,
                                         rankby=None)
                level, cp, level_attack, level_defense, level_stamina, stat_prod, bulk_prod, bogus_rank = stats
                stat.append((stat_prod, (atk, defense, hp)))
                bulk.append((bulk_prod, (atk, defense, hp)))
    stat.sort(reverse=True)
    bulk.sort(reverse=True)
    for (i,(stat_prod, (atk, defense, hp))) in enumerate(stat,start=1):
        OVERALL_RANK['statprod'][mon][(atk,defense,hp)] = i
    for (i,(bulk_prod, (atk, defense, hp))) in enumerate(bulk,start=1):
        OVERALL_RANK['bulkprod'][mon][(atk,defense,hp)] = i

    # Now just debugging
    if 1:
        for i in range(1,11):
            print(f"The rank {i} {mon} at max_level {max_level} is {stat[i-1]}")
                            
def ivs_to_stats(my_a, my_d, my_s, my_level,*,mon,
                     max_level=40,max_cp=1500.99,
                     rankby='statprod', # can be None, statprod, or bulkprod. If it's None, we're probably calculating ranks.
                 ):
    """convert ivs to stat. what a mess.

    my_a, my_d, my_s are the stats of the pokemon you're looking at. my_level is its level.

    max_level is the max level you want to consider. 40 for normal, 41 for best buddy, 50 for XL, 51 for XL BB.
    max_cp should be the max cp for your league + 0.99. E.g. 1500.99 for great.

    This function has some errors for mons that go above the max cp right when you evolve them.
    """

    bs = pokemon[mon]['baseStats']
    base_attack, base_defense, base_stamina = bs['atk'],bs['def'],bs['hp']
    attack = base_attack + my_a
    defense = my_d + base_defense
    stamina = my_s + base_stamina
    level = my_level#10
    cp = 10

    if rankby is None:
        rank = None
    else:
        if mon not in OVERALL_RANK[rankby]:
            add_to_rank(mon,max_level=max_level,max_cp=max_cp)
        rank = OVERALL_RANK[rankby][mon][(my_a,my_d,my_s)]
    
    level_attack, level_defense, level_stamina, stat_prod, bulk_prod = 0,0,0,0,0
    stats = (level, cp, level_attack, level_defense, level_stamina, stat_prod, bulk_prod, rank)
    while level <= max_level:
        cpm = get_cpm(level)
        cp = (attack * defense**0.5 * stamina**0.5 * cpm**2) / 10
        level_attack = attack * cpm
        level_defense = defense * cpm
        level_stamina = stamina * cpm
        if cp <= max_cp:
            stat_prod = math.floor(level_attack*level_defense*math.floor(level_stamina))
            bulk_prod = math.floor(level_defense*math.floor(level_stamina))
            #stat_prod = math.floor(level_attack*level_defense*level_stamina)
            stats = level, cp, level_attack, level_defense, level_stamina, stat_prod, bulk_prod, rank
        level = level + 0.5
    level, cp, level_attack, level_defense, level_stamina, stat_prod, bulk_prod, rank  = stats
    #print(f'{level_attack}, {level_defense}, {level_stamina}, {level_attack*level_defense*level_stamina}')
    return stats
    #print(f'level {level} cp {cp:.0f} attack {level_attack:.1f} defense {level_defense:.1f} stamina {level_stamina:.0f}')
    
    
def mons_to_consider(df,mon):
    """Get a list of mons to consider from a df

    We had to split this into two functions because you get weirdo mons
    like Obstagoon where the base forms are Galarian, but the final form
    isn't. We probably could combine it into one function with "or" but
    it's easier this way.
    """
    #evolution_line = [i for i in EVOLUTIONS if mon in i]
    evolution_line = [i for i in EVOLUTIONS if mon == i[-1]]
    if not len(evolution_line) == 1:
        raise Exception(f'Could not find evolution line for {mon}. got {evolution_line}')
    else:
        evolution_line = evolution_line[0]


    all_results = [_mons_to_consider(df,mon) for mon in evolution_line]
    #print(evolution_line)
    #print(all_results[0])
    #print(all_results[1])
    #print(all_results[2])
    result = pd.concat(all_results)
    return result

def _mons_to_consider(df,mon):
    """Helper function for `mons_to_consider` that just does a single mon, not a whole evolution line.
    """
    if '(' in mon:
        if 'Shadow' in mon:
            raise Exception('No code for shadows yet')
        form_pattern = re.compile('(.*) \((.*)\)') # "Deoxys (Defense)"
        form = form_pattern.search(mon).group(2)
        mon = form_pattern.search(mon).group(1)
    else:
        form = None
        form = 'Normal'
    if form == 'Alolan':
        form = 'Alola'
    elif form == 'Galarian':
        # This is to remind us that it's actually listed as galarian for zig and lin
        form = 'Galarian'
    elif form == 'Paldea':
        form = 'Paldea'
    #evolution_line = [i for i in EVOLUTIONS if mon in i]
    #if not len(evolution_line) == 1:
    #    raise Exception(f'Could not find evolution line for {mon}. got {evolution_line}')
    #else:
    #    evolution_line = evolution_line[0]
    #result = df[df.Name.isin(evolution_line)]
    result = df[df.Name == mon]
#    print(f"Looking for {mon} of form {form} I see {result}")
    if form is not None:
        # Sometimes, if there isn't an alola form or whatever, the normal form gets Form set to NaN.
        # If that happens, we won't get any results, so check explicitly for isna and use those.
        _result = result[result.Form == form]
        if not len(_result):
            _result = result[pd.isna(result.Form)]
        result = _result
            
    return result

#'':{'attack':,'defense':,'hp':},
RS_INFO = {
    'Jumpluff':{
        'Great':
        {
            'Top 12 amazing stat product':{'attack':0,'defense':157.31,'hp':0,'onlytop':12},
        'Slight attack, high def':{'attack':97.6,'defense':156.3,'hp':0},
        'Slight attack, balanced bulk':{'attack':97.6,'defense':150,'hp':151},
        }
        },
    'Walrein':{
        'article':'https://gamepress.gg/pokemongo/walrein-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=yJUjtPAPkEM',),
        'extrainfo':"""For the HP, 151 covers the majority of pertinent matchups. However, 154 HP enables the Toxapex 0-0 and 157 can enable the Bastiodon 2-1 and Swampert 2-2 (full bait). These matchups give credence towards forgoing the Azumarill Atk, and instead focusing on Bulk. Do note that only the Rank 1 can achieve the Bastiodon and Swampert matchups without forgoing the Rank 1 Umbreon Defense Breakpoint for the 2-2. 

All of this suggests that the Best Walrein PvP IVs for the Great League are either the Rank 84 (1/11/2) or the Rank 31 (0/13/2). The former covering Azumarill better, the latter covering Umbreon better. The Rank 23 (2/13/8) is great too. If Azumarill or slightly Atk weighted Umbreon aren’t a concern of yours, the Rank 1 (0/12/15) is also good. """,
        'Great':
        {
            'GOD TIER':{'attack':114.46,'defense':114.75,'hp':148},
            'Azu slayer (112.06 atk, 114.75 def, 151 hp)':{'attack':112.06,'defense':114.75,'hp':151},
            'All Attack Breakpoints':{'attack':114.46,'defense':113,'hp':148},

        },
        'Ultra':
        {
            'Mirror slayer HP':{'attack':145.28,'defense':145,'hp':201},
            'Mirror slayer Def':{'attack':145.28,'defense':147,'hp':199},
            'Best of the best':{'attack':147.45,'defense':145.3,'hp':197},
            },
        'Master':
        {
            'Obviously the best':{'attack':15,'defense':15,'hp':15},
            'Still hits the breakpoints':{'attack':15,'defense':14,'hp':13},
            'Read the article to see about these!':{'attack':13,'defense':12,'hp':12},
        },
    },
    'Deoxys (Defense)':{
        'article':'https://gamepress.gg/pokemongo/deoxys-defense-pvp-iv-deep-dive-analysis',
        'videos':('https://www.youtube.com/watch?v=p-UrAQDrvTQ',),
        'extrainfo':'For GL, the SwagMan wants the rank 67>77>22 (15/14/10 > 15/10/12 > 14/12/13) and then bulk 1 > 3 > 9 (10/15/13 > 10/10/15 > 11/13/12) then the mirror slayer rank 17 (13/11/15). For that first range, the 15/13/10 is my best so far. \n The 12/13/15 I have is the UL rank 1. But also my best GL mirror slayer. For UL I decide between that rank 1 and my rank 150 15/13/12 and rank 146 15/11/12 which hit the table breakpoints.',
        'Great':
        {
            'Best you can get are here, but watch the actual video':{'attack':101.95,'defense':221,'hp':98},
            'Lanturn 0-1 1-1 Spark 1-0 2-1 water gun, if lanturn is not super high def': {'attack':101.95,'defense':220.18,'hp':95,},
            'Includes SwagMan table plus more read the article yo':{'attack':100.78,'defense':220.18,'hp':95},
            'Mirror':{'attack':100.78,'defense':0,'hp':98},
            },
        'Ultra':
        {
            'BB umbreon':{'attack':132.81,'defense':284,'hp':122},
            'Registeel and TF (not BB)':{'attack':132.28,'defense':0,'hp':126},
            'Sme rando Umb, TF, Regi': {'attack':131.8,'defense':0,'hp':126},
            'Just atk breakpoint': {'attack':132.28,'defense':0,'hp':0},
            }
        },
    'Venusaur':{
        'article':'https://gamepress.gg/pokemongo/venusaur-pvp-iv-deep-dive',
        'Great':
        {
            'Froslass Slayer + OK Def':{'attack':122.5,'defense':117.88,'hp':122},
            'Froslass Slayer + Big Def':{'attack':122.5,'defense':121.13,'hp':122},
            'Big Bulk':{'attack':0,'defense':121.13,'hp':123},
            'Shadow big bulk':{'attack':0,'defense':120.46,'hp':122},
            },
        'Ultra':
        {
            'Galar Stunfisk Slayer':{'attack':159.2,'defense':157.25,'hp':152},                
            'Huge Defense':{'attack':0,'defense':160.82,'hp':156},                
            'As good as Rank 1 Bulk':{'attack':0,'defense':158.05,'hp':156},
            'Shadow General Blend':{'attack':161.59,'defense':155.28,'hp':153},
        },
        },
    'Dewgong':{
        'article':'https://gamepress.gg/pokemongo/dewgong-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=u_eDH5HNg1M',),
        'extrainfo':'If you have to choose, favor higher def over higher hp. For GBL, may be best to favor atk breakpoint or high stat product.',
        'Great':
        {
            'Max Def Umbreon, Dewgong, most Mew, weather boosted trev atk, very OK bulk':{'attack':102.89,'defense':131.7,'hp':0},
            'Rank 1 umbreon atk, balanced bulk':{'attack':101.79,'defense':136.81,'hp':150},
            'rank 1 umbreon atk, rank 1 dewgong dominating def':{'attack':101.79,'defense':138.28,'hp':150},
            },
        },
    'Sandslash':{
        'article':'https://gamepress.gg/pokemongo/alolan-sandslash-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=o3e84ZurZ0o',),
        'extrainfo':'Breakpoints are less important here, you really want some bulk.',
        'Great':
        {
            'RS says this':{'attack':121,'defense':120,'hp':0},
            },
        },
    'Sandslash (Alolan)':{
        'article':'https://gamepress.gg/pokemongo/alolan-sandslash-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=o3e84ZurZ0o',),
        'extrainfo':'Breakpoints are less important here, you really want some bulk (top 100ish). Ashrew wants to be at least 12/13/13 and probably at least 12/15/15.',
        'Great':
        {
            'High Attack':{'attack':115.31,'defense':128.92,'hp':119},
            'Super High Attack (egg hatch)':{'attack':118.24,'defense':127.59,'hp':118},
            },
        'Ultra':
        {
            '149.14 atk 173.07 def':{'attack':149.14,'defense':173.07,'hp':0},
            '154.26 atk 168 def':{'attack':154.26,'defense':168,'hp':0},
            }
        },
    'Whimsicott':{
        'article':'https://gamepress.gg/pokemongo/whimsicott-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=kJUjufO4YXA',),
        'extrainfo':'Article is quite detailed.',
        'Great':
        {
            'Moderate attack weight':{'attack':121.26,'defense':132.25,'hp':0},
            'Slight attack weight':{'attack':119.47,'defense':132.25,'hp':0},
            'Alolan Ninetails Slayer':{'attack':121.87,'defense':132.25,'hp':0},
            'Lickitung Slayer (no brain, just charmm)':{'attack':122.81,'defense':132.25,'hp':0},
            },
        },
    'Swampert':{
        'article':'',
        'videos':('',),
        'extrainfo':'No good deep dive',
        'Great':
        {
            'Def':{'attack':0,'defense':110,'hp':0},
            'Atk':{'attack':121.6,'defense':108,'hp':0},
            },
        },
    'Registeel':{
        'article':'https://gamepress.gg/pokemongo/registeel-pvp-iv-deep-dive#topic-379686',
        'videos':('https://www.youtube.com/watch?v=C66Ud9me-tg','https://www.youtube.com/watch?v=W_ZOJPz7LV4'),
        'extrainfo':'Oof. Raid IVs.',
        'Great':
        {
            'Raid Only 186.7 Def 127 HP':{'attack':0,'defense':186.7,'hp':127},
            '190.09 Def 129 HP (trade only)':{'attack':0,'defense':190.09,'hp':129},
            '191.97 Def 129 HP (trade only)':{'attack':0,'defense':191.97,'hp':129},
            },
        'Ultra':
        {
            'Raid Only 240.5 Def 165 HP':{'attack':0,'defense':240.5,'hp':165},
            '244.4 Def 167 HP':{'attack':0,'defense':244.4,'hp':167},
            }
        },
    'Azumarill':{
        'article':'https://gamepress.gg/pokemongo/azumarill-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=iYaqdQG0Ic8',),
        'extrainfo':'Old non-XL article: https://gamepress.gg/pokemongo/azumarill-great-league-pvp-iv-deep-dive .. you can make up or lower def/hp at a 1:2 ratio, so 134.7 def is fixed by a94 hp, 190 hp is fixed by 136.7 def.',
        'Great':
        {
            'Medicham 1-1 consistency, 1-2 potential with play rough':{'attack':0,'defense':137.64,'hp':0},
            'Hits the min':{'attack':0,'defense':135.78,'hp':192},
            'General Def/HP Azu':{'attack':0,'defense':132.8,'hp':187},
            'Slight Atk Weight Azu':{'attack':92,'defense':132.8,'hp':187},
            },
            },
    'Araquanid':{
        'article':'',
        'videos':('https://www.youtube.com/watch?v=dQKFwYr9tQY',),
        'extrainfo':'In general, HP > def, Atk > b/c walrus.',
        'Great':
        {
            'Shadow Drapion attack':{'attack':99.02,'defense':0,'hp':0},
            'High end viggy atk':{'attack':99.2,'defense':0,'hp':0},
            'Best best walrus atk':{'attack':99.93,'defense':0,'hp':0},
            'DD D min':{'attack':0,'defense':163.77,'hp':0},
            'DD D max':{'attack':0,'defense':165.21,'hp':0},
            'HP sable min':{'attack':0,'defense':0,'hp':134},
            'HP sable max':{'attack':0,'defense':0,'hp':136},
            'General':{'attack':99.2,'defense':165.2,'hp':134},
            },
            },
    'Golem (Alolan)':{
        'article':'',
        'videos':('',),
        'extrainfo':'',
        'Great':
        {
            'General':{'attack':124.79,'defense':0,'hp':0},
            'Min':{'attack':123.93,'defense':0,'hp':0},
            'Best':{'attack':126,'defense':118,'hp':0},
            },
            },
    'Marowak (Alolan)':{
        'article':'https://gamepress.gg/pokemongo/alolan-marowak-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=jMwFqbkVlpU',),
        'extrainfo':'Right now, this is looking at everything, so you have to check for shadow explicitly. Go for mid range attack if hit the bulk.',
        'Great':
        {
            'Shadow AWak Min attack, very min defense':{'attack':110.5,'defense':141.49,'hp':0},
            'Shadow AWak Min attack high end':{'attack':111.85,'defense':141.49,'hp':0},
            'All':{'attack':0.,'defense':0,'hp':0},
            'Best':{'attack':126,'defense':118,'hp':0},
            },
            },
    'Linoone (Galarian)':{
        'article':'https://twitter.com/SwgTips/status/1558892455017185280',
        'videos':('',),
        'extrainfo':'Still bad right now.',
        'Great':
        {
            'Swamp/cash':{'attack':112.87,'defense':0,'hp':144},
            'Drap/A9 CMP':{'attack':114,'defense':0,'hp':144},
            'Diggers':{'attack':0.,'defense':110.11,'hp':144},
            'SwagAtk FS Awak':{'attack':0.,'defense':111.14,'hp':144},
            'Best':{'attack':114,'defense':111.14,'hp':144},
            },
            },
    'Obstagoon':{
        'article':'https://gamepress.gg/pokemongo/obstagoon-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=XEygOnJDnlY',),
        'extrainfo':'You want three of each league, one with obstruct and one without, and one with high bulk. Also, this does not filter for galarian zig/lin; you have to do that yourself.\n For UL you really want 148+ attack, then 172 HP',
        'Great':
        {
            'Super Premium Atk ':{'attack':115.5,'defense':123.56,'hp':137},
            'Premium Atk (115.5 Atk slightly better, 123.56 Def 137 HP better)':{'attack':115,'defense':123.3,'hp':135},
            'Bulk focus':{'attack':0,'defense':126,'hp':137},
            #'All':{'attack':0.,'defense':0,'hp':0},
            },
        'Ultra':
        {
            'Unicorn':{'attack':148,'defense':166.8,'hp':172},
            'General Atk (146.95 Atk, 163.8 Def, 172 HP)':{'attack':146.95,'defense':163.8,'hp':172},
            'General Atk+ (147.89 Atk, 163.8 Def, 172 HP)':{'attack':147.89,'defense':163.8,'hp':172},
            'Mirror Focus (149.1 Atk, 172 HP)':{'attack':149.1,'defense':172,'hp':172},
            'Bulk Focus (166.8 Def, 174 HP)':{'attack':0,'defense':166.8,'hp':174},
#            'Bare minimum':{'attack':148,'defense':0,'hp':172},
#            'General Atk':{'attack':146.95,'defense':163.8,'hp':172},
#            'General Atk+':{'attack':148,'defense':163.8,'hp':172},
#            'Mirror Focus':{'attack':149.1,'defense':0,'hp':172},
#            'Bulk Focus':{'attack':0,'defense':166.8,'hp':174},
            #'All':{'attack':0.,'defense':0,'hp':0},
            },
            },
    'Medicham':{
        'article':'https://gamepress.gg/pokemongo/medicham-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=-ihUhkBfdok',),
        'extrainfo':'',
        'Great':{
            'The Good (105.38 Atk, 138.6 Def, 140 HP)':{'attack':105.38,'defense':138.6,'hp':140},
            'Premium Cut':{'attack':105.87,'defense':138.64,'hp':140},
            'The few worthwhile best buddies':{'attack':105.38,'defense':140.3,'hp':142},
            'The Mirror Slayers (note: the drop in bulk may cause trouble in other matchups. Simply going for CMP may be better)':{'attack':108,'defense':137.64,'hp':0},
            }
        },
    'Dedenne':{
        'article':'',
        'videos':('https://www.youtube.com/watch?v=gT7Op0zMJJU',),
        'extrainfo':'HP key, then def, then atk.',
        'Great':{
            'Basic':{'attack':123.17,'defense':109,'hp':133},
            'Scrafty':{'attack':123.17,'defense':109.86,'hp':133},
            'Better atk lap/pidg':{'attack':124.59,'defense':109,'hp':133},
            'Best':{'attack':124.59,'defense':109.86,'hp':133},
            'Just HP def':{'attack':0,'defense':109.86,'hp':133},
            }
        },
    'Dunsparce':{
        'article':'https://gamepress.gg/pokemongo/dunsparce-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=ZiZEbDqMur0',),
        'extrainfo':'Cares ONLY about bulk, not about Atk at all',
        'Great':{
            'Basic Bulk':{'attack':0,'defense':110.63,'hp':185},
            'Premium Bulk':{'attack':0,'defense':111.14,'hp':186},
            'Premium Bulk':{'attack':0,'defense':111.14,'hp':186,'sort':'blkprod'},
            }
        },
    'Stunfisk (Galarian)':{
        'article':'https://gamepress.gg/pokemongo/galarian-stunfisk-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=iUja0_EjGnc',),
        'extrainfo':'For UL, realy do want 15/15/14',
        'Great':{
            'High Bulk (124.75 def, 174 hp)':{'attack':99,'defense':124.75,'hp':174},
            'pure mirror slayer (101.79 atk, 127.34 def)':{'attack':101.79,'defense':127.34,'hp':0},
            'bulk mirror slayer (101.79 atk, 124.75/172)':{'attack':101.79,'defense':124.75,'hp':172,},
            'Minimum bulk (124.75 def 172 hp)':{'attack':99,'defense':124.75,'hp':172},
            }
        },
    'Lickitung':{
        'article':'https://gamepress.gg/pokemongo/lickitung-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''General Good is minimum bulk for "good" lickitung.\nAtk focus: Potentiates Registeel and Shadow Walrein Breakpoints without giving up too much bulk, 126.2 Def, 126.58 Def, and 184 HP are notable stat checks, Priority Recommendation 126.2 Def=184 HP>185+ HP=126.58 Def\nBudget Boi: This budget list is for players who’ve already built a Lickitung and are wondering if they should build twice (or for players looking to save ~94 XL Candy), If you meet at least 125.1 Def and 181 HP, building a better Lickitung might not be worth it compared to other projects''',
        'Great':{
            'General Good (125.94 def, 183 hp)':{'attack':96.36,'defense':125.94,'hp':183},
            'Atk Focus (97.7 Atk, 125.94 def, 183 hp)':{'attack':97.7,'defense':125.94,'hp':183},
            'Budget Bois (97 Atk, 125.1 def, 181 hp)':{'attack':97,'defense':125.1,'hp':181},
            }
        },
    'Toxapex':{
        'article':'https://gamepress.gg/pokemongo/toxapex-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=7ZiNZvY8uXs',),
        'extrainfo':'''

        High Bulk:
        * For tie-breakers, generally HP > Def
        * If you fear Swampert, 227.82+ Def is important
        * If you hate Venusaur & Jumpluff, 91+ Atk is important

        Mirror Slayer
        * If you hate Venusaur & Jumpluff, 91+ Atk is important

        Lickitung Slayer
        * Rank 1 and 2 Best Buddy Lickitung require 94.13 Atk

        Which IV is best? See the article. But Rank 1 is great, Ranks 2 and 3 get CMP over things, ranks 4 and 9 do better against swampert, etc.
''',
        'Great':{
            'High Bulk (226.73 Def, 118 HP)':{'attack':0,'defense':226.73,'hp':118},
            'Mirror Slayer/Big HP (219 Def, 121 HP)':{'attack':0,'defense':219,'hp':121},
            'Lickitung Slayer (93 Atk, 118 HP)':{'attack':93,'defense':0,'hp':118},
            }
        },
    'Toxicroak':{
        'article':'https://www.reddit.com/r/TheSilphArena/comments/xs5swn/toxicroak_pvp_iv_highlights_gl_ul/',
        'videos':('',),
        'extrainfo':'''
        Not a real deep dive.

        So for now, if you have the Rank 35, 98, or 121 do a dance, yeehaw.

        Not a deep dive, just a highlight. 136.6 Atk in general is really cool. Has a bunch of BPs, only 4-5 really matter (Lanturn 1-1, Noctowl 1-1, Registeel consistency, Skarmory 1-0 hope, S!Walrein 1-1 and possibly 1-2).
        
        134 HP scores the Azu 0-0 (Azu, who?), S!Walrein 1-1 & 1-2 (with Atk bp). Spark Lantrun 1-1 (w/ Atk BP) requires 133 HP. Given that both Azu and Walrein are kind of dead, I think the HP could be eased down to 133.
        
        The Def is for S!Venu 1-1 and A9 1-1 (w/130 HP). 88.63 is the min, but 89.78+ is safer. If these two matchups are w/e then you could ignore it. Not sure what the min Def is yet though.        
''',
        'Great':{
            'General Good':{'attack':136,'defense':92.51,'hp':131},
            'General Good (discord)':{'attack':136.6,'defense':88.57,'hp':134},
            'Bork':{'attack':136.6,'defense':82,'hp':134},
            }
        },
    'Trevenant':{
        'article':'https://gamepress.gg/pokemongo/trevenant-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=-02-DBdvGJk&t=738s','https://www.youtube.com/watch?v=Y2tMAs-oZKQ&t=573s'),
        'extrainfo':'''
For great, high def and min HP are most valuable

Gotta check the actual article on all of these. Ryan Swag lists individual IVs, and I just took some baselines from those.
''',
        'Great':{
            'Best':{'attack':124,'defense':105.8,'hp':128},
            'Next':{'attack':124,'defense':105.8,'hp':125},
            },
        'Ultra':{
            'Atk':{'attack':168.7,'defense':129,'hp':167},
#            '':{'attack':,'defense':,'hp':},
            }
        },
    'Noctowl':{
        'article':'https://gamepress.gg/pokemongo/noctowl-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=sdagO7Z8p6w&t=85s',),
        'extrainfo':'''
        People use slight atk and azu slayer primarily. not a9 slayer.

        For Atk:

            * Rank 24 >= Rank 4 > Rank 40/41 > All else
            * 104.8 Atk for 127.7 Def (Rank 2 GFisk)
            * You can thrift on Def, just be cautious about sinking below 117.58

        For Azu Slayer

           * Ranks 67 & 68 have notable bulk
           * >105.8 Atk can get Charge Move Priority on Medicham which can be significant
               * 169 HP or 168 HP + >118.75 Def have higher Medicham 2-2 consistency
           * >106 Atk gets the GFisk Breakpoint on the Rank 3 (0/15/11) (the highest reasonably Def weighted GFisk)

        For A9 Slayer

           * Enables the 2-2 vs nearly all Alolan Nineales
               * 138.9 Def weights will require >107 Atk
           * The Top 5 of the group have bulk balanced to the 0-0 mirror & potentially the Venusaur 0-1
           * The 2/0/15 can also 2-1 Tapu Fini
               * The Alolan Ninetales flip can also be achieved with high enough Def, but given the wide Atk Range of Alolan Ninetales + the HP drop, the high HP low Def versions are generally more useful

''',
        'Great':{
            'Slight Atk':{'attack':104.23,'defense':118.27,'hp':171},
            'Azu Slayer':{'attack':105.2,'defense':117.58,'hp':168},
            'A9 Slayer':{'attack':106.36,'defense':0,'hp':172},
            },
        },
    'Chesnaught':{
        'article':'https://gamepress.gg/pokemongo/chesnaught-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
The tables below feature the IV spreads that meet some of the more important stat checks highlighted in the article. It’s important to review the guide itself to make sure you’re getting what you want out of your Chesnaught. For example, you may want a slightly higher Def or HP weight for more consistency.
        
Bulk Focus (122.21 Def, 127 HP)

    * 129 HP can potentially 1-0 Pelipper
    * The Rank 1 can 0-1 some low Atk Galarian Stunfisk with only Frenzy Plant
    * ~119.35 Atk can 0-1 & 1-1 Scrafty more consistently

Froslass Slayer (121.89 Atk, 117.7 Def, 125 HP)

    * Generally Def>Atk=HP

Froslass Slayer, Def focus (121.89 Atk, 122.21 Def, 122 HP)

    * The 6/3/5 is also viable, but pushes it


''',
        'Great':{
            'Bulk focus 122.21 def, 127 hp':{'attack':0,'defense':122.21,'hp':127},
            'frosslass slayer 121.89 atk, 117.7 def, 125 hp':{'attack':121.89,'defense':117.7,'hp':125},
            'frosslass slayer, def focus (121.89 atk, 122.21 def, 122 hp':{'attack':121.89,'defense':122.21,'hp':122},
            },
        },
    'Altaria':{
        'article':'https://gamepress.gg/pokemongo/altaria-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
        

The Trevenant Slayer (102.97 Atk, 149.02 Def, 139 HP)

    * For general safety, sort list by Def
    * See the Great League Altaria section for details

Bulk + Trevenant maybe (101.95 Atk, 151.63, 139 HP)

    * When you don’t want to forgo the bulk life and don’t expect to see high Def Trevenant
    * For tie breakers, 140 HP is generally better and 153.95+ Def is more useful than 141 HP
    * Table is cut at top 15 to reduce “false positives” for this “premium bulk”

Bulk Focus (153.95 Def, 139 HP)

    * Aside from the Rank’s 1, 2, & 7, you should probably just go for the Atk weighted builds

''',
        'Great':{
            'The Trevenant Slayer (102.97 Atk, 149.02 Def, 139 HP)':{'attack':102.97,'defense':149.02,'hp':139},
            'Bulk + Trevenant maybe (101.95 Atk, 151.63, 139 HP)':{'attack':101.95,'defense':151.63,'hp':139},
            'Bulk Focus (153.95 Def, 139 HP)':{'attack':121.89,'defense':122.21,'hp':122},
            },
        },

    'Cofagrigus':{
        'article':'https://gamepress.gg/pokemongo/cofagrigus-pvp-iv-deep-dive#topic-357026',
        'videos':('',),
        'extrainfo':'''
        rank 1 or 2 way better
''',
        'Great':{
            '':{'attack':109,'defense':162,'hp':106},
            'Best':{'attack':111.32,'defense':164.56,'hp':106},
            },
        'Ultra':{
            '':{'attack':145.21,'defense':208,'hp':138},
            },
        },
    'Runerigus':{
        'article':'https://gamepress.gg/pokemongo/cofagrigus-pvp-iv-deep-dive#topic-357026',
        'videos':('',),
        'extrainfo':'''
        rank 1 or 2 way better
''',
        'Great':{
            '':{'attack':109,'defense':162,'hp':106},
            'Best':{'attack':111.32,'defense':164.56,'hp':106},
            },
        'Ultra':{
            '':{'attack':145.21,'defense':208,'hp':138},
            },
        },


### Remember to buddy up the G versions during the event and catch 30 psychics with each.

        
    'Slowbro':{
        'article':'https://gamepress.gg/pokemongo/slowpoke-family-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
Slowbro & Slowking 118.4 Def, 144 HP

    * Higher HP is generally better

Shadow Slowbro & Slowking 113.7 Atk, 117.8 Def, 141 HP

    * 113.7 Atk covers the Rank 1 and 2 Galarian Stunfisk, 114.95 covers the Rank 3
    * In general, HP > Def
''',
        'Great':{
            '118.4 Def, 144 HP':{'attack':0,'defense':118.4,'hp':144},
            },
#        'Ultra':{
#            '':{'attack':102.97,'defense':149.02,'hp':139},
#            },
        },
        
    'Slowbro (Galarian)':{
        'article':'https://gamepress.gg/pokemongo/slowpoke-family-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
Galarian Slowbro Generalist/Mirror 118.48 Atk, 108.83 Def, 144 HP

    * HP > Def > Atk

Galarian Slowbro Bulk Focus 109 Def, 146 HP

    * 147 HP for Shadow Victreebel 0-1 consistency
    * The Rank 2 (0/15/10) may 2-1 high bulk Umbreon
''',
        'Great':{
            'Galarian Slowbro Generalist/Mirror 118.48 Atk, 108.83 Def, 144 HP':{'attack':118.48,'defense':108.83,'hp':144},
            'Galarian Slowbro Bulk Focus 109 Def, 146 HP':{'attack':0,'defense':109,'hp':146},
            'Anything':{'attack':110,'defense':100,'hp':144},
            },
#        'Ultra':{
#            '':{'attack':102.97,'defense':149.02,'hp':139},
#            },
        },
        
    'Slowking (Galarian)':{
        'article':'https://gamepress.gg/pokemongo/slowpoke-family-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
Galarian Slowbro Generalist/Mirror 118.48 Atk, 108.83 Def, 144 HP

    * HP > Def > Atk

Galarian Slowbro Bulk Focus 109 Def, 146 HP

    * 147 HP for Shadow Victreebel 0-1 consistency
    * The Rank 2 (0/15/10) may 2-1 high bulk Umbreon
''',
        'Great':{
            'Galarian Slowking Mirror Slayer 116.7 Atk, 117.5 Def, 138 HP':{'attack':116.7,'defense':117.5,'hp':138},
            },
#        'Ultra':{
#            '':{'attack':102.97,'defense':149.02,'hp':139},
#            },
        },
        
    'Tapu Fini':{
        'article':'https://gamepress.gg/pokemongo/tapu-fini-pvp-iv-deep-dive#topic-445576',
        'videos':('https://www.youtube.com/watch?v=4b_RuJMUFpI',),
        'extrainfo':'''
For GL:

        * Higher Def > Higher HP, unless the HP is 110+
        * You can thrift down to 105 HP if you’re tired of trading for Tapu Fini

For UL

        * 142 HP is notably better and only available through trading
        * 147.59 Atk gets Poliwrath CMP (1-2) and an Aurorus Breakpoint (0-1)
        * 149.39 Atk gets an Alolan Ninetales Breakpoints, enabling the 0-1 and 1-2 vs Powder         

''',
        'Great':{
            'OMG beat medi (153.91 Def, 110 HP)':{'attack':0,'defense':153.91,'hp':110},
            'General Good (153.91 Def, 107 HP)':{'attack':0,'defense':153.91,'hp':107},
            'Thrift 105 HP (153.91 Def, 105 HP)':{'attack':0,'defense':153.91,'hp':107},
            'all':{'attack':0,'defense':0,'hp':0},
            },
        'Ultra':{
            'Better HP (198.9 Def, 142 HP)':{'attack':0,'defense':198.9,'hp':142},
            'Poli and Aurorus Atk (147.49 Atk, 198.9 Def, 139 HP)':{'attack':147.59,'defense':198.9,'hp':139},
            'Also A9 Atk (149.39 Atk, 198.9 Def, 139 HP)':{'attack':149.39,'defense':198.9,'hp':139},
            'General Good (198.9 Def, 139 HP)':{'attack':0,'defense':198.9,'hp':139},
            },
        },

    'Greninja':{
        'article':'https://gamepress.gg/pokemongo/greninja-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=fkWByvRz44M&t=118s',),
        'extrainfo':'''
For GL:

    * 140.51, 141.09, 141.38 are notable Atk BPs for Toxapex, Swampert, and Lanturn respectively See guide for details
        
    * 99.36 Def covers 121.9 Atk Froslass
        
    * 11356+ Bulk Product may cover the Diggersby 0-0
        
    * 110 HP is the absolute bare minimum recommendation if you have limited options

For UL:

    * Higher Def is more likely to handle the SC Giratina 2-2 and Shadow Machamp 1-0 (~131.48)
        
    * Higher Atk weights may get a Breakpoint to 1-1 some Cresselia

Full list of GL atk benefits:

    *     139.04, Pelipper 1-1 consistency (Hydro Cannon BP)
        
    *     139.33, Bastiodon 0-0 consistency (HC BP) & Togedemaru 1-1 (WS BP)
        
    *     139.59, Powder Snow Alolan Ninetales 2-2 (HC BP)
        
    *     140.08, Azumarill 2-1 (WS BP)
        
    *     140.27, Toxicroak 1-0 (WS BP)
        
    *     140.51, Toxapex 1-0 (NS BP)
        
    *     141.09, Swampert 1-1 potential (WS BP)
        
    *     141.38, Water Gun Lanturn 1-1 (NS BP)
        
    *     144.3, Skarmory 1-1 (WS BP)
        
    *     144.6, Shadow Alolan Sandslash 1-1 (WS BP)
        
        
        
''',
        'Great':{
            'GL- Bulk Focus (99.61 Def, 115 HP)':{'attack':0,'defense':99.61,'hp':115},
            'GL- Azu Slayer (140.08 Atk, 99.36 Def, 111 HP)':{'attack':140.08,'defense':99.36,'hp':111},
            'GL - stupid hi atk not filtered for bulk':{'attack':143.3,'defense':0,'hp':0},
            'GL - STUPID hi atk not filtered for bulk':{'attack':144.6,'defense':0,'hp':0},
            'GL - hi atk not filtered for bulk':{'attack':139.04,'defense':0,'hp':0},
            },
        'Ultra':{
            'UL- Bulk Focus (130.62 Def, 149 HP)':{'attack':0,'defense':130.62,'hp':149},
            'This list is also solid (132.53 Def, 147 HP), but 149 HP is safer':{'attack':0,'defense':132.53,'hp':149},
            },
        },

    'Dubwool':{
        'article':'https://gamepress.gg/pokemongo/dubwool-pvp-iv-deep-dive',
        'videos':('https://www.youtube.com/watch?v=xTlYFqEzQdw',),
        'extrainfo':'''

GL - High Bulk (141.6 Def, 128 HP):

    *    Sort list by Bulk Product- 18499+ is generally safe

    *     130 HP is generally preferred

    *     131 HP may 0-0 Water Gun Lanturn

    * 109.3+ Atk may gain Charge Move Breakpoints vs Altaria, Shadow Venusaur, and Registeel

    * 129 HP may prevent Medicham from straight farming you in the 0-0

    
UL - Nearly Hundo

    *     14/15/15 is the preference

    *     In general, 13/13/14 is a solid soft minimum
        
''',
        'Great':{
            'GL - High Bulk (141.6 Def, 128 HP) NEEDS blk prod 18499':{'attack':0,'defense':141.6,'hp':128,'sort':'blkprod'},
            'GL all blkprod sort':{'attack':0,'defense':0,'hp':0,'sort':'blkprod'},
            },
        'Ultra':{
            'UL - Nearly Hundo':{'attack':0,'defense':178.3,'hp':160},
            },
        },
        
    'Quagsire':{
        'article':'https://gamepress.gg/pokemongo/quagsire-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''

Non-shadow notes

  *     113.66 Def > 112.68 Def w/164+ HP > 164+ HP

  *     112 Def covers Rank 1/119.5 Atk Sableye

  *     113.66 Def covers 121.4 Atk Sableye (Swamp/Venu CMP)

  *     113.66 Def covers 108.9/AXN Medicham

  *     112.68 Def covers 86-86.6 Atk Carbink

Shadow high bulk notes


  *     113.66 Def covers 121.4 Atk Sableye & possibly Froslass
        
  *     164 HP enables Vigoroth 1-1
        
  *     Higher Atk gives Shadow Venusaur 0-1, Medicham 2-1, & Noctowl 1-1 potential with Mud Bomb
        
  *         110 Atk vs Rank 1 Medicham, also Cofagrigus CMP potential
        
  *     Honorable mention to the 0/14/8 and 0/15/6 for their higher Def stats mostly making up for the HP drop
        
Carbink slayer notes


  *     112.22 Atk covers Best Buddy Carbink
        
  *     17748+ Bulk Product is safer vs high Atk Carbink
        
  *     Going over 109 Def may maintain the Shadow Venusaur 1-0
        
  *     Going over 110.26 Def may enable the Emolga 1-2 (w/ Mud Bomb)
        
''',
        'Great':{
            'Non-Shadow, High Bulk: 112 Def, 163 HP':{'attack':0,'defense':112,'hp':163},
            'Shadow, High Bulk: 112.68 Def, 163 HP':{'attack':0,'defense':112.68,'hp':163},
            'Shadow, Slight Atk Weight: 110 Atk, 110.26 Def, 163 HP. High def better.':{'attack':110,'defense':110.26,'hp':163},
            'Carbink Slayer: 111.89 Atk, 108 Def, 162 HP':{'attack':111.89,'defense':108,'hp':162},
            },
        },

    'Clodsire':{
        'article':'https://gamepress.gg/pokemongo/clodsire-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
''',
        'Great':{
            'Blk1':{'attack':0,'defense':119.51,'hp':212},
            'Blk2':{'attack':0,'defense':121.23,'hp':210},
            'Atk':{'attack':96.5,'defense':117,'hp':199},
            'all20':{'attack':0,'defense':0,'hp':0,'onlytop':20}
            },
        },
        
    'Charjabug':{
        'article':'',
        'videos':('',),
        'extrainfo':'''
        Here's a slight CMP list that covers the aforementioned losses (atk is cut at Umbreon BP) https://pvpivs.com/?mon=Charjabug&r=11&cp=1500&mA=114.51&mD=136.09&mHP=124&dec=2
''',
        'Great':{
            'Mirror Slayerish':{'attack':116.27,'defense':136.09,'hp':120},
            'Mirror Slayerish slight CMP want rank 194 or better':{'attack':114.51,'defense':136.09,'hp':124},
            'all':{'attack':0,'defense':0,'hp':0},
            },
        'Ultra':{
            '':{'attack':102.97,'defense':149.02,'hp':139},
            },
        },
        
    'Froslass':{
        'article':'https://gamepress.gg/pokemongo/froslass-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
        Premium CMP 121.6 Atk, 113 Def, 131 HP

    Rank 8 is likely the “best”
    HP > Atk > Def for tiebreakers

General Bulk 113 Def, 131 HP

    Same list, but without the Atk weights restricting higher SP
    Ranks 6 & 7 are probably fine, but that HP hit isn’t “high bulk” quality

Higher Atk 123.12 Atk, 113 Def, 127 HP

    This list thins bulk out to the limit while pushing for CMP
    Probably better in Froslass dominant metas rather than Open GL

''',
        'Great':{
            'Premium CMP 121.6 Atk, 113 Def, 131 HP':{'attack':121.6,'defense':113,'hp':131},
            'General Bulk 113 Def, 131 HP':{'attack':0,'defense':113,'hp':131},
            'Higher Atk 123.12 Atk, 113 Def, 127 HP':{'attack':123.12,'defense':113,'hp':127},
            },
        #'Ultra':{
            #'':{'attack':0,'defense':0,'hp':0},
            #},
        },

    'Decidueye':{
        'article':'',
        'videos':('',),
        'extrainfo':'''
        

 * General Good - All Fast Moves (115.29 Def, 118 HP)

    * Note: may bring Def down to 113.7 for 120 HP (extra list)

 * Astonish - General Good (115.52 Def, 118 HP)

    * 127.61 Atk for Trevenant CMP, Gligar 2-1 and Artibax 2-1 potential

        * 127.84 Atk for Lickitung 1-0 potential (FP) and Emolga CMP

    * ">" 116 Def for Shadow Dragonair 0-0, 1-1, and 2-1 potential

        * Note: 0/15/10 may 1-1 Vigoroth

    * 119-120 HP for Cresselia 2-2 consistency (FP BB)

    * 120 HP for Trevenant 2-1 potential (no BB), Lickitung 1-0 potential (FP), and Sableye 2-1 consistency

        * Note: may bring Def down to 113.7 for 120 HP (extra list)

 * Leafage - Slight Atk Weight (127.61 Atk, 115.29 Def, 118 HP)

    * 119 HP Shadow Poliwrath 1-2 potential

        * Tie or win, Shadow Poliwrath IVs depending

    * Highlight: 113.7 Def w/ 121 HP may 2-1 Bronzong and have greater Shadow Poliwrath 1-2 potential

        * 1/9/15 (Rank 9) > 0/10/15 (Rank 8) but both are great

    * Highlight: 116.71+ Def may 1-0 and 2-1 Shadow Dragonair and 2-2 Sir Fetch'd

        * 0/14/11 (Rank 1) for general use, 0/15/10 (Rank 7) has more Def but 1 less HP

''',
        'Great':{
            'General Good - All Fast Moves':{'attack':0,'defense':115.29,'hp':118},
            'General Good - All Fast Moves low def high hp':{'attack':0,'defense':113.7,'hp':120},
            'Astonish':{'attack':0,'defense':115.52,'hp':118},
            'Astonish high atk':{'attack':127.61,'defense':115.52,'hp':118},
            'Astonish high def':{'attack':0,'defense':116,'hp':118},
            'Astonish high hp':{'attack':0,'defense':113.7,'hp':120},
            'Leafage - Slight atk':{'attack':127.61,'defense':115.29,'hp':118},
            'Leafage - Slight atk - s-poli':{'attack':127.61,'defense':115.29,'hp':119},
            'Leafage - Slight atk - zong/poli':{'attack':127.61,'defense':113.7,'hp':118},
            'Leafage - Slight atk - s-dnair, sirfetch':{'attack':127.61,'defense':116.71,'hp':118},
            },
        },

    'Lanturn':{
        'article':'https://gamepress.gg/pokemongo/pvp-iv-deep-dive-lanturn',
        'videos':('',),
        'extrainfo':'''
''',
        'Great':{
            'General Bulk (take the one with highest def)':{'attack':0,'defense':105.5,'hp':196},
            'Premium Bulk/Def focus':{'attack':0,'defense':106.04,'hp':192},
            },
        'Ultra':{
            '':{'attack':0,'defense':0,'hp':0},
            },
        },

    'Annihilape':{
        'article':'https://gamepress.gg/pokemongo/annihilape-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''


* GL-General Good (122.94 Atk, 106.17 Def, 136 HP)

    * 136 HP is safer with >107.1 Def
        
    * Higher Def is more consistent for the Altaria 2-2
        
    * 122.94 Atk is for the Rank 1 Whiscash 2-2 and CMP
        
        * Higher Atk can get BPs on Sableye, Wigglytuff, Zweilous, Cresselia, and more
        
    * 124.4 Atk can full farm Shadow Poliwrath in the 1-0 and may 0-0 Clodsire
        

* GL-Lickitung Slayer (127.23 Atk, 102.26 Def, 132 HP)

    * 127.23 Atk for the Rank 1 non-Best Buddy Lickitung 1-1 (127.09 Def)
        
        * 128.31 Atk covers the Rank 1 Best Buddy Lickitung (128.1 Def)
        
    * 102.26 Def to 2-2 98.26 Atk Lickitung (10/15/13)
        
        * 102.55 Def covers 98.5 Atk Lickitung (10/14/13)
        
    * 103.54 Def for the mirror BP vs 127.23 Atk Annihilape (2-2 no bait, 2-1 farm, 0-0 Ice Punch only)
        
        103.64 Def for 127.51 Atk Annihilape

* UL-General Good (159.7 Atk, 134.5 Def, 178 HP)

    * Higher Atk covers Swampert, Shadow Gliscor, and Talonflame better
        
        * 160.46 for 0/15/12 Swampert, Rank 1 Shadow Gliscor, and non-BB Rank 1 Talonflame CMP
        
    * 134.95 Def covers 138.2 Atk Greedent (6/15/15) for the 0-0
        

* ML Min IVs - 15/15/14 (ideal), 14/14/14 (ok)

    * 15 HP is an empty IV at level 50
        
    * 15 Atk for CMP and Charge Move Breakpoints
        
    * 15 Def can come up for Shadow Ball in the mirror
''',
        'Great':{
            'GL-General Good (122.94 Atk, 106.17 Def, 136 HP)':{'attack':122.94,'defense':106.17,'hp':136},
            'GL-Lickitung Slayer [stop at rank 2829/34] (127.23 Atk, 102.26 Def, 132 HP)':{'attack':127.23,'defense':102.26,'hp':132},
            'GL-Lickitung Slayer bulk [stop at rank 2829/24] (127.23 Atk, 102.26 Def, 132 HP)':{'attack':127.23,'defense':102.55,'hp':132},
            },
        'Ultra':{
            'UL-General Good (159.7 Atk, 134.5 Def, 178 HP)':{'attack':159.7,'defense':134.5,'hp':178},
            },
        },
        
    'Goodra':{
        'article':'',
        'videos':('',),
        'extrainfo':'''
''',
        'Great':{
            'Swag':{'attack':0,'defense':135.72,'hp':117},
            'Swag licki':{'attack':122,'defense':125.2,'hp':115},
            },
        'Ultra':{
            '':{'attack':0,'defense':0,'hp':0},
            },
        },

    'Carbink':{
        'article':'https://gamepress.gg/pokemongo/carbink-pvp-iv-deep-dive',
        'videos':('',),
        'extrainfo':'''
''',
        'Great':{
            'Premium Bulk (247.67 Def, 128 HP) [Best in general]':{'attack':81.38,'defense':247.67,'hp':128},
            'Slight Atk Weight (85.81 Atk, 239.06 Def, 124 HP) [Good for Rock Throw]':{'attack':85.81,'defense':239.06,'hp':124},
            'General Good (246 Def, 124 HP)':{'attack':82.83,'defense':246,'hp':124},
            },
#        'Ultra':{
#
        '':{'attack':0,'defense':0,'hp':0},
#            },
        },
    'Bogus':{
        'article':'',
        'videos':('',),
        'extrainfo':'''
''',
        'Great':{
            '':{'attack':0,'defense':0,'hp':0},
            },
        'Ultra':{
            '':{'attack':0,'defense':0,'hp':0},
            },
        },
        
    }


def display_full_report(df):
    for mon in RS_INFO:
        display_rs_info(df,mon)

def display_rs_info(df,mon):
    """
    """
    if mon not in RS_INFO:
        raise Exception(f"Sorry, I don't know what Ryan Swag says about {mon}.")
        
    df = mons_to_consider(df,mon)
    mon_stats = {
        'Great':get_max_stats(df,mon,max_level=51,max_cp=1500.99),
        'Great cheap':get_max_stats(df,mon,max_level=41,max_cp=1500.99),
        'Ultra':get_max_stats(df,mon,max_level=51,max_cp=2500.99),
        'Ultra cheap':get_max_stats(df,mon,max_level=41,max_cp=2500.99),
        }
    # Maybe rename this
    # TODO: Add ability to sort by atk or blkprod.
    def get_mons(attack,defense,hp,mine,*,level_max=99,sort='statprod'):
        these = mine[mine.attack >= attack]
        these = these[these.defense >= defense]
        these = these[these.stamina >= hp]
        these = these[these.level <= level_max]
        these = these.sort_values(sort,ascending=False)
        return these.sort_values(sort,ascending=False)
        
    display(Markdown(f'# {mon}s you have, according to the Swag Man'))
    if 'article' in RS_INFO[mon]:
        display(Markdown(f'Check out the article [here]({RS_INFO[mon]["article"]})!'))
    if 'videos' in RS_INFO[mon]:
        txt = 'Check out the videos: ' + ' '.join(f'[here]({video})' for video in RS_INFO[mon]['videos']) + '!'
        display(Markdown(txt))
    if 'extrainfo' in RS_INFO[mon]:
        display(Markdown(f'Extra Tips: {RS_INFO[mon]["extrainfo"]}'))
    
    for league in ('Great','Ultra'):
        display(Markdown(f'## {league} League'))
        if league not in RS_INFO[mon]:
            continue
        for k in RS_INFO[mon][league]:
            display(Markdown(f'### {k}'))
            attack, defense, hp = [RS_INFO[mon][league][k][i] for i in ('attack','defense','hp')]
            if 'onlytop' in RS_INFO[mon][league][k]:
                onlytop = RS_INFO[mon][league][k]['onlytop']
                display(HTML(f'<p style="color:red">NOTE! Ryan says you only want the top {onlytop} mons in this category. This code does only checks IVs and stat products, so you want to double-check his actual article before evolving something!</p>'))
            if 'sort' in RS_INFO[mon][league][k]:
                sort = RS_INFO[mon][league][k]['sort']
            else:
                sort='statprod'
            display(get_mons(attack, defense, hp, mon_stats[league],sort=sort))
                    
        
def get_max_stats(df, mon, max_level, max_cp):
    # Great League, allowing XL, allowing best buddy
    rankstr = f'rank{max_level}'
    d = {'CP':[],'max CP':[],'level':[],'attack':[],'defense':[],'stamina':[],'a':[],'d':[],'s':[],'statprod':[],'blkprod':[],rankstr:[]}
    for row in df.iterrows():
        i,s = row
        orig_cp, my_a, my_d, my_s, my_level = s.CP, s['Atk IV'], s['Def IV'], s['Sta IV'], s['Level Min']
        level, cp, attack, defense, stamina, stat_prod, bulk_prod, rank= ivs_to_stats(my_a, my_d, my_s,my_level = my_level,
                                                                            max_level=max_level,max_cp=max_cp,mon=mon,
                                                                                          rankby='statprod')
        #print('orig_cp',orig_cp,'my_a',my_a)
        d['CP'].append(orig_cp)
        d['max CP'].append(int(np.floor(cp)))
        d['level'].append(level)
        d['attack'].append(attack)
        d['defense'].append(defense)
        d['stamina'].append(int(np.floor(stamina)))
        d['a'].append(my_a)
        d['d'].append(my_d)
        d['s'].append(my_s)
        d['statprod'].append(stat_prod)
        d['blkprod'].append(bulk_prod)
        d[rankstr].append(rank)
    mine = pd.DataFrame.from_dict(d)
    return mine
