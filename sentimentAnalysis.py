import re
import math

SENTIMENT_DICT = {
    'abandon': 'negative', 'abandoned': 'negative', 'abandonment': 'negative', 'abase': 'negative',
    'abasement': 'negative', 'abash': 'negative', 'abate': 'negative', 'abdicate': 'negative',
    'aberration': 'negative', 'abhor': 'negative', 'abhorred': 'negative', 'abhorrence':
    'negative', 'abhorrent': 'negative', 'abhorrently': 'negative', 'abhors': 'negative',
    'abidance': 'positive', 'abide': 'positive', 'abilities': 'positive', 'ability': 'positive',
    'abject': 'negative', 'abjectly': 'negative', 'abjure': 'negative', 'able': 'positive',
    'abnormal': 'negative', 'abolish': 'negative', 'abominable': 'negative', 'abominably':
    'negative', 'abominate': 'negative', 'abomination': 'negative', 'abound': 'positive', 'above':
    'positive', 'above-average': 'positive', 'abrade': 'negative', 'abrasive': 'negative',
    'abrupt': 'negative', 'abscond': 'negative', 'absence': 'negative', 'absent-minded':
    'negative', 'absentee': 'negative', 'absolute': 'neutral', 'absolutely': 'neutral', 'absolve':
    'positive', 'absorbed': 'neutral', 'absurd': 'negative', 'absurdity': 'negative', 'absurdly':
    'negative', 'absurdness': 'negative', 'abundance': 'positive', 'abundant': 'positive', 'abuse':
    'negative', 'abuses': 'negative', 'abusive': 'negative', 'abysmal': 'negative', 'abysmally':
    'negative', 'abyss': 'negative', 'accede': 'positive', 'accentuate': 'neutral', 'accept':
    'positive', 'acceptable': 'positive', 'acceptance': 'positive', 'accessible': 'positive',
    'accidental': 'negative', 'acclaim': 'positive', 'acclaimed': 'positive', 'acclamation':
    'positive', 'accolade': 'positive', 'accolades': 'positive', 'accommodative': 'positive',
    'accomplish': 'positive', 'accomplishment': 'positive', 'accomplishments': 'positive',
    'accord': 'positive', 'accordance': 'positive', 'accordantly': 'positive', 'accost':
    'negative', 'accountable': 'negative', 'accurate': 'positive', 'accurately': 'positive',
    'accursed': 'negative', 'accusation': 'negative', 'accusations': 'negative', 'accuse':
    'negative', 'accuses': 'negative', 'accusing': 'negative', 'accusingly': 'negative',
    'acerbate': 'negative', 'acerbic': 'negative', 'acerbically': 'negative', 'ache': 'negative',
    'achievable': 'positive', 'achieve': 'positive', 'achievement': 'positive', 'achievements':
    'positive', 'acknowledge': 'positive', 'acknowledgement': 'positive', 'acquit': 'positive',
    'acrid': 'negative', 'acridly': 'negative', 'acridness': 'negative', 'acrimonious': 'negative',
    'acrimoniously': 'negative', 'acrimony': 'negative', 'active': 'positive', 'activist':
    'neutral', 'actual': 'neutral', 'actuality': 'neutral', 'actually': 'neutral', 'acumen':
    'positive', 'adamant': 'negative', 'adamantly': 'negative', 'adaptability': 'positive',
    'adaptable': 'positive', 'adaptive': 'positive', 'addict': 'negative', 'addiction': 'negative',
    'adept': 'positive', 'adeptly': 'positive', 'adequate': 'positive', 'adherence': 'positive',
    'adherent': 'positive', 'adhesion': 'positive', 'admirable': 'positive', 'admirably':
    'positive', 'admiration': 'positive', 'admire': 'positive', 'admirer': 'positive', 'admiring':
    'positive', 'admiringly': 'positive', 'admission': 'positive', 'admit': 'positive',
    'admittedly': 'positive', 'admonish': 'negative', 'admonisher': 'negative', 'admonishingly':
    'negative', 'admonishment': 'negative', 'admonition': 'negative', 'adolescents': 'neutral',
    'adorable': 'positive', 'adore': 'positive', 'adored': 'positive', 'adorer': 'positive',
    'adoring': 'positive', 'adoringly': 'positive', 'adrift': 'negative', 'adroit': 'positive',
    'adroitly': 'positive', 'adulate': 'positive', 'adulation': 'positive', 'adulatory':
    'positive', 'adulterate': 'negative', 'adulterated': 'negative', 'adulteration': 'negative',
    'advanced': 'positive', 'advantage': 'positive', 'advantageous': 'positive', 'advantages':
    'positive', 'adventure': 'positive', 'adventuresome': 'positive', 'adventurism': 'positive',
    'adventurous': 'positive', 'adversarial': 'negative', 'adversary': 'negative', 'adverse':
    'negative', 'adversity': 'negative', 'advice': 'positive', 'advisable': 'positive', 'advocacy':
    'positive', 'advocate': 'positive', 'affability': 'positive', 'affable': 'positive', 'affably':
    'positive', 'affect': 'neutral', 'affectation': 'negative', 'affected': 'neutral', 'affection':
    'positive', 'affectionate': 'positive', 'affinity': 'positive', 'affirm': 'positive',
    'affirmation': 'positive', 'affirmative': 'positive', 'afflict': 'negative', 'affliction':
    'negative', 'afflictive': 'negative', 'affluence': 'positive', 'affluent': 'positive',
    'afford': 'positive', 'affordable': 'positive', 'affront': 'negative', 'afloat': 'positive',
    'afraid': 'negative', 'against': 'negative', 'aggravate': 'negative', 'aggravating':
    'negative', 'aggravation': 'negative', 'aggression': 'negative', 'aggressive': 'negative',
    'aggressiveness': 'negative', 'aggressor': 'negative', 'aggrieve': 'negative', 'aggrieved':
    'negative', 'aghast': 'negative', 'agile': 'positive', 'agilely': 'positive', 'agility':
    'positive', 'agitate': 'negative', 'agitated': 'negative', 'agitation': 'negative', 'agitator':
    'negative', 'agonies': 'negative', 'agonize': 'negative', 'agonizing': 'negative',
    'agonizingly': 'negative', 'agony': 'negative', 'agree': 'positive', 'agreeability':
    'positive', 'agreeable': 'positive', 'agreeableness': 'positive', 'agreeably': 'positive',
    'agreement': 'positive', 'aha': 'neutral', 'ail': 'negative', 'ailment': 'negative', 'aimless':
    'negative', 'air': 'neutral', 'airs': 'negative', 'alarm': 'negative', 'alarmed': 'negative',
    'alarming': 'negative', 'alarmingly': 'negative', 'alas': 'negative', 'alert': 'neutral',
    'alienate': 'negative', 'alienated': 'negative', 'alienation': 'negative', 'all-time':
    'neutral', 'allay': 'positive', 'allegation': 'negative', 'allegations': 'negative', 'allege':
    'negative', 'allegorize': 'neutral', 'allergic': 'negative', 'alleviate': 'positive',
    'alliance': 'neutral', 'alliances': 'neutral', 'allow': 'positive', 'allowable': 'positive',
    'allure': 'positive', 'alluring': 'positive', 'alluringly': 'positive', 'allusion': 'neutral',
    'allusions': 'neutral', 'ally': 'positive', 'almighty': 'positive', 'aloof': 'negative',
    'altercation': 'negative', 'although': 'negative', 'altogether': 'neutral', 'altruist':
    'positive', 'altruistic': 'positive', 'altruistically': 'positive', 'amaze': 'positive',
    'amazed': 'positive', 'amazement': 'positive', 'amazing': 'positive', 'amazingly': 'positive',
    'ambiguity': 'negative', 'ambiguous': 'negative', 'ambitious': 'positive', 'ambitiously':
    'positive', 'ambivalence': 'negative', 'ambivalent': 'negative', 'ambush': 'negative',
    'ameliorate': 'positive', 'amenable': 'positive', 'amenity': 'positive', 'amiability':
    'positive', 'amiabily': 'positive', 'amiable': 'positive', 'amicability': 'positive',
    'amicable': 'positive', 'amicably': 'positive', 'amiss': 'negative', 'amity': 'positive',
    'amnesty': 'positive', 'amour': 'positive', 'ample': 'positive', 'amplify': 'neutral', 'amply':
    'positive', 'amputate': 'negative', 'amuse': 'positive', 'amusement': 'positive', 'amusing':
    'positive', 'amusingly': 'positive', 'analytical': 'neutral', 'anarchism': 'negative',
    'anarchist': 'negative', 'anarchistic': 'negative', 'anarchy': 'negative', 'anemic':
    'negative', 'angel': 'positive', 'angelic': 'positive', 'anger': 'negative', 'angrily':
    'negative', 'angriness': 'negative', 'angry': 'negative', 'anguish': 'negative', 'animated':
    'positive', 'animosity': 'negative', 'annihilate': 'negative', 'annihilation': 'negative',
    'annoy': 'negative', 'annoyance': 'negative', 'annoyed': 'negative', 'annoying': 'negative',
    'annoyingly': 'negative', 'anomalous': 'negative', 'anomaly': 'negative', 'antagonism':
    'negative', 'antagonist': 'negative', 'antagonistic': 'negative', 'antagonize': 'negative',
    'anti-': 'negative', 'anti-American': 'negative', 'anti-Israeli': 'negative', 'anti-Semites':
    'negative', 'anti-US': 'negative', 'anti-occupation': 'negative', 'anti-proliferation':
    'negative', 'anti-social': 'negative', 'anti-white': 'negative', 'antipathy': 'negative',
    'antiquated': 'negative', 'antithetical': 'negative', 'anxieties': 'negative', 'anxiety':
    'negative', 'anxious': 'negative', 'anxiously': 'negative', 'anxiousness': 'negative',
    'anyhow': 'neutral', 'anyway': 'neutral', 'anyways': 'neutral', 'apathetic': 'negative',
    'apathetically': 'negative', 'apathy': 'negative', 'ape': 'negative', 'apocalypse': 'negative',
    'apocalyptic': 'negative', 'apologist': 'negative', 'apologists': 'negative', 'apostle':
    'positive', 'apotheosis': 'positive', 'appal': 'negative', 'appall': 'negative', 'appalled':
    'negative', 'appalling': 'negative', 'appallingly': 'negative', 'apparent': 'neutral',
    'apparently': 'neutral', 'appeal': 'positive', 'appealing': 'positive', 'appear': 'neutral',
    'appearance': 'neutral', 'appease': 'positive', 'applaud': 'positive', 'appreciable':
    'positive', 'appreciate': 'positive', 'appreciation': 'positive', 'appreciative': 'positive',
    'appreciatively': 'positive', 'appreciativeness': 'positive', 'apprehend': 'neutral',
    'apprehension': 'negative', 'apprehensions': 'negative', 'apprehensive': 'negative',
    'apprehensively': 'negative', 'appropriate': 'positive', 'approval': 'positive', 'approve':
    'positive', 'apt': 'positive', 'aptitude': 'positive', 'aptly': 'positive', 'arbitrary':
    'negative', 'arcane': 'negative', 'archaic': 'negative', 'ardent': 'positive', 'ardently':
    'positive', 'ardor': 'positive', 'arduous': 'negative', 'arduously': 'negative', 'argue':
    'negative', 'argument': 'negative', 'argumentative': 'negative', 'arguments': 'negative',
    'aristocratic': 'positive', 'arousal': 'positive', 'arouse': 'positive', 'arousing':
    'positive', 'arresting': 'positive', 'arrogance': 'negative', 'arrogant': 'negative',
    'arrogantly': 'negative', 'articulate': 'positive', 'artificial': 'negative', 'ascendant':
    'positive', 'ascertainable': 'positive', 'ashamed': 'negative', 'asinine': 'negative',
    'asininely': 'negative', 'asinininity': 'negative', 'askance': 'negative', 'asperse':
    'negative', 'aspersion': 'negative', 'aspersions': 'negative', 'aspiration': 'positive',
    'aspirations': 'positive', 'aspire': 'positive', 'assail': 'negative', 'assassin': 'negative',
    'assassinate': 'negative', 'assault': 'negative', 'assent': 'positive', 'assertions':
    'positive', 'assertive': 'positive', 'assess': 'neutral', 'assessment': 'neutral',
    'assessments': 'neutral', 'asset': 'positive', 'assiduous': 'positive', 'assiduously':
    'positive', 'assuage': 'positive', 'assumption': 'neutral', 'assurance': 'positive',
    'assurances': 'positive', 'assure': 'positive', 'assuredly': 'positive', 'astonish':
    'positive', 'astonished': 'positive', 'astonishing': 'positive', 'astonishingly': 'positive',
    'astonishment': 'positive', 'astound': 'positive', 'astounded': 'positive', 'astounding':
    'positive', 'astoundingly': 'positive', 'astray': 'negative', 'astronomic': 'neutral',
    'astronomical': 'neutral', 'astronomically': 'neutral', 'astute': 'positive', 'astutely':
    'positive', 'asunder': 'negative', 'asylum': 'positive', 'atrocious': 'negative', 'atrocities':
    'negative', 'atrocity': 'negative', 'atrophy': 'negative', 'attack': 'negative', 'attain':
    'positive', 'attainable': 'positive', 'attentive': 'positive', 'attest': 'positive',
    'attitude': 'neutral', 'attitudes': 'neutral', 'attraction': 'positive', 'attractive':
    'positive', 'attractively': 'positive', 'attune': 'positive', 'audacious': 'negative',
    'audaciously': 'negative', 'audaciousness': 'negative', 'audacity': 'negative', 'auspicious':
    'positive', 'austere': 'negative', 'authentic': 'positive', 'authoritarian': 'negative',
    'authoritative': 'positive', 'autocrat': 'negative', 'autocratic': 'negative', 'autonomous':
    'positive', 'avalanche': 'negative', 'avarice': 'negative', 'avaricious': 'negative',
    'avariciously': 'negative', 'avenge': 'negative', 'aver': 'positive', 'averse': 'negative',
    'aversion': 'negative', 'avid': 'positive', 'avidly': 'positive', 'avoid': 'negative',
    'avoidance': 'negative', 'award': 'positive', 'aware': 'neutral', 'awareness': 'neutral',
    'awe': 'positive', 'awed': 'positive', 'awesome': 'positive', 'awesomely': 'positive',
    'awesomeness': 'positive', 'awestruck': 'positive', 'awful': 'negative', 'awfully': 'negative',
    'awfulness': 'negative', 'awkward': 'negative', 'awkwardness': 'negative', 'ax': 'negative',
    'babble': 'negative', 'baby': 'neutral', 'back': 'positive', 'backbite': 'negative',
    'backbiting': 'negative', 'backbone': 'positive', 'backward': 'negative', 'backwardness':
    'negative', 'bad': 'negative', 'badly': 'negative', 'baffle': 'negative', 'baffled':
    'negative', 'bafflement': 'negative', 'baffling': 'negative', 'bait': 'negative', 'balanced':
    'positive', 'balk': 'negative', 'banal': 'negative', 'banalize': 'negative', 'bane':
    'negative', 'banish': 'negative', 'banishment': 'negative', 'bankrupt': 'negative', 'bar':
    'negative', 'barbarian': 'negative', 'barbaric': 'negative', 'barbarically': 'negative',
    'barbarity': 'negative', 'barbarous': 'negative', 'barbarously': 'negative', 'barely':
    'negative', 'bargain': 'positive', 'barren': 'negative', 'baseless': 'negative', 'bashful':
    'negative', 'basic': 'positive', 'basically': 'neutral', 'bask': 'positive', 'bastard':
    'negative', 'batons': 'neutral', 'battered': 'negative', 'battering': 'negative', 'battle':
    'negative', 'battle-lines': 'negative', 'battlefield': 'negative', 'battleground': 'negative',
    'batty': 'negative', 'beacon': 'positive', 'bearish': 'negative', 'beast': 'negative',
    'beastly': 'negative', 'beatify': 'positive', 'beauteous': 'positive', 'beautiful': 'positive',
    'beautifully': 'positive', 'beautify': 'positive', 'beauty': 'positive', 'bedlam': 'negative',
    'bedlamite': 'negative', 'befit': 'positive', 'befitting': 'positive', 'befoul': 'negative',
    'befriend': 'positive', 'beg': 'negative', 'beggar': 'negative', 'beggarly': 'negative',
    'begging': 'negative', 'beguile': 'negative', 'belabor': 'negative', 'belated': 'negative',
    'beleaguer': 'negative', 'belie': 'negative', 'belief': 'neutral', 'beliefs': 'neutral',
    'believable': 'positive', 'believe': 'neutral', 'belittle': 'negative', 'belittled':
    'negative', 'belittling': 'negative', 'bellicose': 'negative', 'belligerence': 'negative',
    'belligerent': 'negative', 'belligerently': 'negative', 'beloved': 'positive', 'bemoan':
    'negative', 'bemoaning': 'negative', 'bemused': 'negative', 'benefactor': 'positive',
    'beneficent': 'positive', 'beneficial': 'positive', 'beneficially': 'positive', 'beneficiary':
    'positive', 'benefit': 'positive', 'benefits': 'positive', 'benevolence': 'positive',
    'benevolent': 'positive', 'benign': 'positive', 'bent': 'negative', 'berate': 'negative',
    'bereave': 'negative', 'bereavement': 'negative', 'bereft': 'negative', 'berserk': 'negative',
    'beseech': 'negative', 'beset': 'negative', 'besides': 'neutral', 'besiege': 'negative',
    'besmirch': 'negative', 'best': 'positive', 'best-known': 'positive', 'best-performing':
    'positive', 'best-selling': 'positive', 'bestial': 'negative', 'betray': 'negative',
    'betrayal': 'negative', 'betrayals': 'negative', 'betrayer': 'negative', 'better': 'positive',
    'better-known': 'positive', 'better-than-expected': 'positive', 'bewail': 'negative', 'beware':
    'negative', 'bewilder': 'negative', 'bewildered': 'negative', 'bewildering': 'negative',
    'bewilderingly': 'negative', 'bewilderment': 'negative', 'bewitch': 'negative', 'bias':
    'negative', 'biased': 'negative', 'biases': 'negative', 'bicker': 'negative', 'bickering':
    'negative', 'bid-rigging': 'negative', 'big': 'neutral', 'bitch': 'negative', 'bitchy':
    'negative', 'biting': 'negative', 'bitingly': 'negative', 'bitter': 'negative', 'bitterly':
    'negative', 'bitterness': 'negative', 'bizarre': 'negative', 'blab': 'negative', 'blabber':
    'negative', 'black': 'negative', 'blackmail': 'negative', 'blah': 'negative', 'blame':
    'negative', 'blameless': 'positive', 'blameworthy': 'negative', 'bland': 'negative',
    'blandish': 'negative', 'blaspheme': 'negative', 'blasphemous': 'negative', 'blasphemy':
    'negative', 'blast': 'negative', 'blasted': 'negative', 'blatant': 'negative', 'blatantly':
    'negative', 'blather': 'negative', 'bleak': 'negative', 'bleakly': 'negative', 'bleakness':
    'negative', 'bleed': 'negative', 'blemish': 'negative', 'bless': 'positive', 'blessing':
    'positive', 'blind': 'negative', 'blinding': 'negative', 'blindingly': 'negative', 'blindness':
    'negative', 'blindside': 'negative', 'bliss': 'positive', 'blissful': 'positive', 'blissfully':
    'positive', 'blister': 'negative', 'blistering': 'negative', 'blithe': 'positive', 'bloated':
    'negative', 'block': 'negative', 'blockhead': 'negative', 'blood': 'neutral', 'bloodshed':
    'negative', 'bloodthirsty': 'negative', 'bloody': 'negative', 'bloom': 'positive', 'blossom':
    'positive', 'blow': 'negative', 'blunder': 'negative', 'blundering': 'negative', 'blunders':
    'negative', 'blunt': 'negative', 'blur': 'negative', 'blurt': 'negative', 'boast': 'positive',
    'boastful': 'negative', 'boggle': 'negative', 'bogus': 'negative', 'boil': 'negative',
    'boiling': 'negative', 'boisterous': 'negative', 'bold': 'positive', 'boldly': 'positive',
    'boldness': 'positive', 'bolster': 'positive', 'bomb': 'negative', 'bombard': 'negative',
    'bombardment': 'negative', 'bombastic': 'negative', 'bondage': 'negative', 'bonkers':
    'negative', 'bonny': 'positive', 'bonus': 'positive', 'boom': 'positive', 'booming':
    'positive', 'boost': 'positive', 'bore': 'negative', 'boredom': 'negative', 'boring':
    'negative', 'botch': 'negative', 'bother': 'negative', 'bothersome': 'negative', 'boundless':
    'positive', 'bountiful': 'positive', 'bowdlerize': 'negative', 'boycott': 'negative', 'brag':
    'both', 'braggart': 'negative', 'bragger': 'negative', 'brains': 'positive', 'brainwash':
    'negative', 'brainy': 'positive', 'brash': 'negative', 'brashly': 'negative', 'brashness':
    'negative', 'brat': 'negative', 'bravado': 'negative', 'brave': 'positive', 'bravery':
    'positive', 'brazen': 'negative', 'brazenly': 'negative', 'brazenness': 'negative', 'breach':
    'negative', 'break': 'negative', 'break-point': 'negative', 'breakdown': 'negative',
    'breakthrough': 'positive', 'breakthroughs': 'positive', 'breathlessness': 'positive',
    'breathtaking': 'positive', 'breathtakingly': 'positive', 'bright': 'positive', 'brighten':
    'positive', 'brightness': 'positive', 'brilliance': 'positive', 'brilliant': 'positive',
    'brilliantly': 'positive', 'brimstone': 'negative', 'brisk': 'positive', 'bristle': 'negative',
    'brittle': 'negative', 'broad': 'positive', 'broad-based': 'neutral', 'broke': 'negative',
    'broken-hearted': 'negative', 'brood': 'negative', 'brook': 'positive', 'brotherly':
    'positive', 'browbeat': 'negative', 'bruise': 'negative', 'brusque': 'negative', 'brutal':
    'negative', 'brutalising': 'negative', 'brutalities': 'negative', 'brutality': 'negative',
    'brutalize': 'negative', 'brutalizing': 'negative', 'brutally': 'negative', 'brute':
    'negative', 'brutish': 'negative', 'buckle': 'negative', 'bug': 'negative', 'bulky':
    'negative', 'bull': 'positive', 'bullies': 'negative', 'bullish': 'positive', 'bully':
    'negative', 'bullyingly': 'negative', 'bum': 'negative', 'bumpy': 'negative', 'bungle':
    'negative', 'bungler': 'negative', 'bunk': 'negative', 'buoyant': 'positive', 'burden':
    'negative', 'burdensome': 'negative', 'burdensomely': 'negative', 'burn': 'negative', 'busy':
    'negative', 'busybody': 'negative', 'butcher': 'negative', 'butchery': 'negative', 'byzantine':
    'negative', 'cackle': 'negative', 'cajole': 'negative', 'calamities': 'negative', 'calamitous':
    'negative', 'calamitously': 'negative', 'calamity': 'negative', 'callous': 'negative', 'calm':
    'positive', 'calming': 'positive', 'calmness': 'positive', 'calumniate': 'negative',
    'calumniation': 'negative', 'calumnies': 'negative', 'calumnious': 'negative', 'calumniously':
    'negative', 'calumny': 'negative', 'cancer': 'negative', 'cancerous': 'negative', 'candid':
    'positive', 'candor': 'positive', 'cannibal': 'negative', 'cannibalize': 'negative',
    'capability': 'positive', 'capable': 'positive', 'capably': 'positive', 'capitalize':
    'positive', 'capitulate': 'negative', 'capricious': 'negative', 'capriciously': 'negative',
    'capriciousness': 'negative', 'capsize': 'negative', 'captivate': 'positive', 'captivating':
    'positive', 'captivation': 'positive', 'captive': 'negative', 'care': 'positive', 'carefree':
    'positive', 'careful': 'positive', 'careless': 'negative', 'carelessness': 'negative',
    'caricature': 'negative', 'carnage': 'negative', 'carp': 'negative', 'cartoon': 'negative',
    'cartoonish': 'negative', 'cash-strapped': 'negative', 'castigate': 'negative', 'casualty':
    'negative', 'cataclysm': 'negative', 'cataclysmal': 'negative', 'cataclysmic': 'negative',
    'cataclysmically': 'negative', 'catalyst': 'positive', 'catastrophe': 'negative',
    'catastrophes': 'negative', 'catastrophic': 'negative', 'catastrophically': 'negative',
    'catchy': 'positive', 'caustic': 'negative', 'caustically': 'negative', 'cautionary':
    'negative', 'cautious': 'negative', 'cave': 'negative', 'ceaseless': 'neutral', 'celebrate':
    'positive', 'celebrated': 'positive', 'celebration': 'positive', 'celebratory': 'positive',
    'celebrity': 'positive', 'censure': 'negative', 'central': 'neutral', 'certain': 'neutral',
    'certainly': 'neutral', 'certified': 'neutral', 'chafe': 'negative', 'chaff': 'negative',
    'chagrin': 'negative', 'challenge': 'negative', 'challenging': 'negative', 'champ': 'positive',
    'champion': 'positive', 'chant': 'neutral', 'chaos': 'negative', 'chaotic': 'negative',
    'charisma': 'negative', 'charismatic': 'positive', 'charitable': 'positive', 'charity':
    'positive', 'charm': 'positive', 'charming': 'positive', 'charmingly': 'positive', 'chaste':
    'positive', 'chasten': 'negative', 'chastise': 'negative', 'chastisement': 'negative',
    'chatter': 'negative', 'chatterbox': 'negative', 'cheap': 'negative', 'cheapen': 'negative',
    'cheat': 'negative', 'cheater': 'negative', 'cheer': 'positive', 'cheerful': 'positive',
    'cheerless': 'negative', 'cheery': 'positive', 'cherish': 'positive', 'cherished': 'positive',
    'cherub': 'positive', 'chic': 'positive', 'chide': 'negative', 'childish': 'negative', 'chill':
    'negative', 'chilly': 'negative', 'chit': 'negative', 'chivalrous': 'positive', 'chivalry':
    'positive', 'choke': 'negative', 'choppy': 'negative', 'chore': 'negative', 'chronic':
    'negative', 'chum': 'positive', 'civil': 'positive', 'civility': 'positive', 'civilization':
    'positive', 'civilize': 'positive', 'claim': 'neutral', 'clamor': 'negative', 'clamorous':
    'negative', 'clandestine': 'neutral', 'clarity': 'positive', 'clash': 'negative', 'classic':
    'positive', 'clean': 'positive', 'cleanliness': 'positive', 'cleanse': 'positive', 'clear':
    'positive', 'clear-cut': 'positive', 'clearer': 'positive', 'clearly': 'positive', 'clever':
    'positive', 'cliche': 'negative', 'cliched': 'negative', 'clique': 'negative', 'clog':
    'negative', 'close': 'negative', 'closeness': 'positive', 'cloud': 'negative', 'clout':
    'positive', 'clumsy': 'negative', 'co-operation': 'positive', 'coarse': 'negative', 'coax':
    'positive', 'cocky': 'negative', 'coddle': 'positive', 'coerce': 'negative', 'coercion':
    'negative', 'coercive': 'negative', 'cogent': 'positive', 'cogitate': 'neutral', 'cognizance':
    'neutral', 'cognizant': 'neutral', 'cohere': 'positive', 'coherence': 'positive', 'coherent':
    'positive', 'cohesion': 'positive', 'cohesive': 'positive', 'cold': 'negative', 'coldly':
    'negative', 'collapse': 'negative', 'collide': 'negative', 'collude': 'negative', 'collusion':
    'negative', 'colorful': 'positive', 'colossal': 'positive', 'combative': 'negative',
    'comeback': 'positive', 'comedy': 'negative', 'comely': 'positive', 'comfort': 'positive',
    'comfortable': 'positive', 'comfortably': 'positive', 'comforting': 'positive', 'comical':
    'negative', 'commend': 'positive', 'commendable': 'positive', 'commendably': 'positive',
    'commensurate': 'positive', 'comment': 'neutral', 'commentator': 'neutral', 'commiserate':
    'negative', 'commitment': 'positive', 'commodious': 'positive', 'commonplace': 'negative',
    'commonsense': 'positive', 'commonsensible': 'positive', 'commonsensibly': 'positive',
    'commonsensical': 'positive', 'commotion': 'negative', 'compact': 'positive', 'compassion':
    'positive', 'compassionate': 'positive', 'compatible': 'positive', 'compel': 'negative',
    'compelling': 'positive', 'compensate': 'positive', 'competence': 'positive', 'competency':
    'positive', 'competent': 'positive', 'competitive': 'positive', 'competitiveness': 'positive',
    'complacent': 'negative', 'complain': 'negative', 'complaining': 'negative', 'complaint':
    'negative', 'complaints': 'negative', 'complement': 'positive', 'complete': 'neutral',
    'completely': 'neutral', 'complex': 'negative', 'compliant': 'positive', 'complicate':
    'negative', 'complicated': 'negative', 'complication': 'negative', 'complicit': 'negative',
    'compliment': 'positive', 'complimentary': 'positive', 'comprehend': 'neutral',
    'comprehensive': 'positive', 'compromise': 'positive', 'compromises': 'positive', 'compulsion':
    'negative', 'compulsive': 'negative', 'compulsory': 'negative', 'comrades': 'positive',
    'concede': 'negative', 'conceit': 'negative', 'conceited': 'negative', 'conceivable':
    'positive', 'concern': 'negative', 'concerned': 'negative', 'concerning': 'neutral',
    'concerns': 'negative', 'concerted': 'neutral', 'concession': 'negative', 'concessions':
    'negative', 'conciliate': 'positive', 'conciliatory': 'positive', 'conclusive': 'positive',
    'concrete': 'positive', 'concur': 'positive', 'condemn': 'negative', 'condemnable': 'negative',
    'condemnation': 'negative', 'condescend': 'negative', 'condescending': 'negative',
    'condescendingly': 'negative', 'condescension': 'negative', 'condolence': 'negative',
    'condolences': 'negative', 'condone': 'positive', 'conducive': 'positive', 'confer':
    'positive', 'confess': 'negative', 'confession': 'negative', 'confessions': 'negative',
    'confide': 'neutral', 'confidence': 'positive', 'confident': 'positive', 'conflict':
    'negative', 'confound': 'negative', 'confounded': 'negative', 'confounding': 'negative',
    'confront': 'negative', 'confrontation': 'negative', 'confrontational': 'negative', 'confuse':
    'negative', 'confused': 'negative', 'confusing': 'negative', 'confusion': 'negative',
    'confute': 'positive', 'congenial': 'positive', 'congested': 'negative', 'congestion':
    'negative', 'congratulate': 'positive', 'congratulations': 'positive', 'congratulatory':
    'positive', 'conjecture': 'neutral', 'conquer': 'positive', 'conscience': 'neutral',
    'conscientious': 'positive', 'consciousness': 'neutral', 'consensus': 'positive', 'consent':
    'positive', 'consequently': 'neutral', 'consider': 'neutral', 'considerable': 'neutral',
    'considerably': 'neutral', 'considerate': 'positive', 'consideration': 'neutral', 'consistent':
    'positive', 'console': 'positive', 'conspicuous': 'negative', 'conspicuously': 'negative',
    'conspiracies': 'negative', 'conspiracy': 'negative', 'conspirator': 'negative',
    'conspiratorial': 'negative', 'conspire': 'negative', 'constancy': 'positive', 'consternation':
    'negative', 'constitutions': 'neutral', 'constrain': 'negative', 'constraint': 'negative',
    'constructive': 'positive', 'consume': 'negative', 'consummate': 'positive', 'contagious':
    'negative', 'contaminate': 'negative', 'contamination': 'negative', 'contemplate': 'neutral',
    'contempt': 'negative', 'contemptible': 'negative', 'contemptuous': 'negative',
    'contemptuously': 'negative', 'contend': 'negative', 'content': 'positive', 'contention':
    'negative', 'contentious': 'negative', 'contentment': 'positive', 'continuity': 'positive',
    'continuous': 'neutral', 'contort': 'negative', 'contortions': 'negative', 'contradict':
    'negative', 'contradiction': 'negative', 'contradictory': 'negative', 'contrariness':
    'negative', 'contrary': 'negative', 'contravene': 'negative', 'contribution': 'positive',
    'contrive': 'negative', 'contrived': 'negative', 'controversial': 'negative', 'controversy':
    'negative', 'convenient': 'positive', 'conveniently': 'positive', 'conviction': 'positive',
    'convince': 'positive', 'convincing': 'positive', 'convincingly': 'positive', 'convoluted':
    'negative', 'cooperate': 'positive', 'cooperation': 'positive', 'cooperative': 'positive',
    'cooperatively': 'positive', 'coping': 'negative', 'cordial': 'positive', 'cornerstone':
    'positive', 'correct': 'positive', 'corrective': 'neutral', 'correctly': 'positive', 'corrode':
    'negative', 'corrosion': 'negative', 'corrosive': 'negative', 'corrupt': 'negative',
    'corruption': 'negative', 'cost-effective': 'positive', 'cost-saving': 'positive', 'costly':
    'negative', 'could': 'neutral', 'counterproductive': 'negative', 'coupists': 'negative',
    'courage': 'positive', 'courageous': 'positive', 'courageously': 'positive', 'courageousness':
    'positive', 'court': 'positive', 'courteous': 'positive', 'courtesy': 'positive', 'courtly':
    'positive', 'covenant': 'positive', 'covert': 'neutral', 'covet': 'both', 'coveting': 'both',
    'covetingly': 'both', 'covetous': 'negative', 'covetously': 'both', 'cow': 'negative',
    'coward': 'negative', 'cowardly': 'negative', 'cozy': 'positive', 'crackdown': 'negative',
    'crafty': 'negative', 'cramped': 'negative', 'cranky': 'negative', 'crass': 'negative',
    'crave': 'positive', 'craven': 'negative', 'cravenly': 'negative', 'craving': 'positive',
    'craze': 'negative', 'crazily': 'negative', 'craziness': 'negative', 'crazy': 'negative',
    'creative': 'positive', 'credence': 'positive', 'credible': 'positive', 'credulous':
    'negative', 'crime': 'negative', 'criminal': 'negative', 'cringe': 'negative', 'cripple':
    'negative', 'crippling': 'negative', 'crisis': 'negative', 'crisp': 'positive', 'critic':
    'negative', 'critical': 'negative', 'criticism': 'negative', 'criticisms': 'negative',
    'criticize': 'negative', 'critics': 'negative', 'crook': 'negative', 'crooked': 'negative',
    'cross': 'negative', 'crowded': 'negative', 'crude': 'negative', 'cruel': 'negative',
    'cruelties': 'negative', 'cruelty': 'negative', 'crumble': 'negative', 'crumple': 'negative',
    'crusade': 'positive', 'crusader': 'positive', 'crush': 'negative', 'crushing': 'negative',
    'cry': 'negative', 'culpable': 'negative', 'cumbersome': 'negative', 'cuplrit': 'negative',
    'cure-all': 'positive', 'curious': 'positive', 'curiously': 'positive', 'curse': 'negative',
    'cursed': 'negative', 'curses': 'negative', 'cursory': 'negative', 'curt': 'negative', 'cuss':
    'negative', 'cut': 'negative', 'cute': 'positive', 'cutthroat': 'negative', 'cynical':
    'negative', 'cynicism': 'negative', 'damage': 'negative', 'damaging': 'negative', 'damn':
    'negative', 'damnable': 'negative', 'damnably': 'negative', 'damnation': 'negative', 'damned':
    'negative', 'damning': 'negative', 'dance': 'positive', 'danger': 'negative', 'dangerous':
    'negative', 'dangerousness': 'negative', 'dangle': 'negative', 'dare': 'positive', 'daring':
    'positive', 'daringly': 'positive', 'dark': 'negative', 'darken': 'negative', 'darkness':
    'negative', 'darling': 'positive', 'darn': 'negative', 'dash': 'negative', 'dashing':
    'positive', 'dastard': 'negative', 'dastardly': 'negative', 'daunt': 'negative', 'daunting':
    'negative', 'dauntingly': 'negative', 'dauntless': 'positive', 'dawdle': 'negative', 'dawn':
    'positive', 'daydream': 'positive', 'daydreamer': 'positive', 'daze': 'negative', 'dazed':
    'negative', 'dazzle': 'positive', 'dazzled': 'positive', 'dazzling': 'positive', 'dead':
    'negative', 'deadbeat': 'negative', 'deadlock': 'negative', 'deadly': 'negative', 'deadweight':
    'negative', 'deaf': 'negative', 'deal': 'positive', 'dear': 'positive', 'dearth': 'negative',
    'death': 'negative', 'debacle': 'negative', 'debase': 'negative', 'debasement': 'negative',
    'debaser': 'negative', 'debatable': 'negative', 'debate': 'negative', 'debauch': 'negative',
    'debaucher': 'negative', 'debauchery': 'negative', 'debilitate': 'negative', 'debilitating':
    'negative', 'debility': 'negative', 'decadence': 'negative', 'decadent': 'negative', 'decay':
    'negative', 'decayed': 'negative', 'deceit': 'negative', 'deceitful': 'negative',
    'deceitfully': 'negative', 'deceitfulness': 'negative', 'deceive': 'negative', 'deceiver':
    'negative', 'deceivers': 'negative', 'deceiving': 'negative', 'decency': 'positive', 'decent':
    'positive', 'deception': 'negative', 'deceptive': 'negative', 'deceptively': 'negative',
    'decide': 'neutral', 'decisive': 'positive', 'decisiveness': 'positive', 'declaim': 'negative',
    'decline': 'negative', 'declining': 'negative', 'decrease': 'negative', 'decreasing':
    'negative', 'decrement': 'negative', 'decrepit': 'negative', 'decrepitude': 'negative',
    'decry': 'negative', 'dedicated': 'positive', 'deduce': 'neutral', 'deep': 'neutral',
    'deepening': 'negative', 'deeply': 'neutral', 'defamation': 'negative', 'defamations':
    'negative', 'defamatory': 'negative', 'defame': 'negative', 'defeat': 'negative', 'defect':
    'negative', 'defective': 'negative', 'defend': 'positive', 'defender': 'positive', 'defense':
    'positive', 'defensive': 'negative', 'deference': 'positive', 'defiance': 'negative',
    'defiant': 'negative', 'defiantly': 'negative', 'deficiency': 'negative', 'deficient':
    'negative', 'defile': 'negative', 'defiler': 'negative', 'definite': 'positive', 'definitely':
    'positive', 'definitive': 'positive', 'definitively': 'positive', 'deflationary': 'positive',
    'deform': 'negative', 'deformed': 'negative', 'defrauding': 'negative', 'deft': 'positive',
    'defunct': 'negative', 'defy': 'negative', 'degenerate': 'negative', 'degenerately':
    'negative', 'degeneration': 'negative', 'degradation': 'negative', 'degrade': 'negative',
    'degrading': 'negative', 'degradingly': 'negative', 'dehumanization': 'negative', 'dehumanize':
    'negative', 'deign': 'negative', 'deject': 'negative', 'dejected': 'negative', 'dejectedly':
    'negative', 'dejection': 'negative', 'delectable': 'positive', 'delicacy': 'positive',
    'delicate': 'positive', 'delicious': 'positive', 'delight': 'positive', 'delighted':
    'positive', 'delightful': 'positive', 'delightfully': 'positive', 'delightfulness': 'positive',
    'delinquency': 'negative', 'delinquent': 'negative', 'delirious': 'negative', 'delirium':
    'negative', 'delude': 'negative', 'deluded': 'negative', 'deluge': 'negative', 'delusion':
    'negative', 'delusional': 'negative', 'delusions': 'negative', 'demand': 'both', 'demands':
    'both', 'demean': 'negative', 'demeaning': 'negative', 'demise': 'negative', 'democratic':
    'positive', 'demolish': 'negative', 'demolisher': 'negative', 'demon': 'negative', 'demonic':
    'negative', 'demonize': 'negative', 'demoralize': 'negative', 'demoralizing': 'negative',
    'demoralizingly': 'negative', 'demystify': 'positive', 'denial': 'negative', 'denigrate':
    'negative', 'denounce': 'negative', 'denunciate': 'negative', 'denunciation': 'negative',
    'denunciations': 'negative', 'deny': 'negative', 'dependable': 'positive', 'dependent':
    'neutral', 'deplete': 'negative', 'deplorable': 'negative', 'deplorably': 'negative',
    'deplore': 'negative', 'deploring': 'negative', 'deploringly': 'negative', 'deprave':
    'negative', 'depraved': 'negative', 'depravedly': 'negative', 'deprecate': 'negative',
    'depress': 'negative', 'depressed': 'negative', 'depressing': 'negative', 'depressingly':
    'negative', 'depression': 'negative', 'deprive': 'negative', 'deprived': 'negative', 'deride':
    'negative', 'derision': 'negative', 'derisive': 'negative', 'derisively': 'negative',
    'derisiveness': 'negative', 'derogatory': 'negative', 'desecrate': 'negative', 'desert':
    'negative', 'desertion': 'negative', 'deserve': 'positive', 'deserved': 'positive',
    'deservedly': 'positive', 'deserving': 'positive', 'desiccate': 'negative', 'desiccated':
    'negative', 'desirable': 'positive', 'desire': 'positive', 'desirous': 'positive', 'desolate':
    'negative', 'desolately': 'negative', 'desolation': 'negative', 'despair': 'negative',
    'despairing': 'negative', 'despairingly': 'negative', 'desperate': 'negative', 'desperately':
    'negative', 'desperation': 'negative', 'despicable': 'negative', 'despicably': 'negative',
    'despise': 'negative', 'despised': 'negative', 'despite': 'negative', 'despoil': 'negative',
    'despoiler': 'negative', 'despondence': 'negative', 'despondency': 'negative', 'despondent':
    'negative', 'despondently': 'negative', 'despot': 'negative', 'despotic': 'negative',
    'despotism': 'negative', 'destabilisation': 'negative', 'destine': 'positive', 'destined':
    'positive', 'destinies': 'positive', 'destiny': 'positive', 'destitute': 'negative',
    'destitution': 'negative', 'destroy': 'negative', 'destroyer': 'negative', 'destruction':
    'negative', 'destructive': 'negative', 'desultory': 'negative', 'deter': 'negative',
    'deteriorate': 'negative', 'deteriorating': 'negative', 'deterioration': 'negative',
    'determination': 'positive', 'deterrent': 'negative', 'detest': 'negative', 'detestable':
    'negative', 'detestably': 'negative', 'detract': 'negative', 'detraction': 'negative',
    'detriment': 'negative', 'detrimental': 'negative', 'devastate': 'negative', 'devastated':
    'negative', 'devastating': 'negative', 'devastatingly': 'negative', 'devastation': 'negative',
    'deviate': 'negative', 'deviation': 'negative', 'devil': 'negative', 'devilish': 'negative',
    'devilishly': 'negative', 'devilment': 'negative', 'devilry': 'negative', 'devious':
    'negative', 'deviously': 'negative', 'deviousness': 'negative', 'devoid': 'negative', 'devote':
    'positive', 'devoted': 'positive', 'devotee': 'positive', 'devotion': 'positive', 'devout':
    'positive', 'dexterity': 'positive', 'dexterous': 'positive', 'dexterously': 'positive',
    'dextrous': 'positive', 'diabolic': 'negative', 'diabolical': 'negative', 'diabolically':
    'negative', 'diametrically': 'negative', 'diatribe': 'negative', 'diatribes': 'negative',
    'dictator': 'negative', 'dictatorial': 'negative', 'differ': 'negative', 'difference':
    'neutral', 'difficult': 'negative', 'difficulties': 'negative', 'difficulty': 'negative',
    'diffidence': 'negative', 'dig': 'negative', 'dignified': 'positive', 'dignify': 'positive',
    'dignity': 'positive', 'digress': 'negative', 'dilapidated': 'negative', 'dilemma': 'negative',
    'diligence': 'positive', 'diligent': 'positive', 'diligently': 'positive', 'dilly-dally':
    'negative', 'dim': 'negative', 'diminish': 'negative', 'diminishing': 'negative', 'din':
    'negative', 'dinky': 'negative', 'diplomacy': 'neutral', 'diplomatic': 'positive', 'dire':
    'negative', 'direct': 'neutral', 'direly': 'negative', 'direness': 'negative', 'dirt':
    'negative', 'dirty': 'negative', 'disable': 'negative', 'disabled': 'negative', 'disaccord':
    'negative', 'disadvantage': 'negative', 'disadvantaged': 'negative', 'disadvantageous':
    'negative', 'disaffect': 'negative', 'disaffected': 'negative', 'disaffirm': 'negative',
    'disagree': 'negative', 'disagreeable': 'negative', 'disagreeably': 'negative', 'disagreement':
    'negative', 'disallow': 'negative', 'disappoint': 'negative', 'disappointed': 'negative',
    'disappointing': 'negative', 'disappointingly': 'negative', 'disappointment': 'negative',
    'disapprobation': 'negative', 'disapproval': 'negative', 'disapprove': 'negative',
    'disapproving': 'negative', 'disarm': 'negative', 'disarray': 'negative', 'disaster':
    'negative', 'disastrous': 'negative', 'disastrously': 'negative', 'disavow': 'negative',
    'disavowal': 'negative', 'disbelief': 'negative', 'disbelieve': 'negative', 'disbeliever':
    'negative', 'discern': 'neutral', 'discerning': 'positive', 'disclaim': 'negative',
    'discombobulate': 'negative', 'discomfit': 'negative', 'discomfititure': 'negative',
    'discomfort': 'negative', 'discompose': 'negative', 'disconcert': 'negative', 'disconcerted':
    'negative', 'disconcerting': 'negative', 'disconcertingly': 'negative', 'disconsolate':
    'negative', 'disconsolately': 'negative', 'disconsolation': 'negative', 'discontent':
    'negative', 'discontented': 'negative', 'discontentedly': 'negative', 'discontinuity':
    'negative', 'discord': 'negative', 'discordance': 'negative', 'discordant': 'negative',
    'discountenance': 'negative', 'discourage': 'negative', 'discouragement': 'negative',
    'discouraging': 'negative', 'discouragingly': 'negative', 'discourteous': 'negative',
    'discourteously': 'negative', 'discredit': 'negative', 'discreet': 'positive', 'discrepant':
    'negative', 'discretion': 'positive', 'discriminate': 'negative', 'discriminating': 'positive',
    'discriminatingly': 'positive', 'discrimination': 'negative', 'discriminatory': 'negative',
    'disdain': 'negative', 'disdainful': 'negative', 'disdainfully': 'negative', 'disease':
    'negative', 'diseased': 'negative', 'disfavor': 'negative', 'disgrace': 'negative',
    'disgraced': 'negative', 'disgraceful': 'negative', 'disgracefully': 'negative', 'disgruntle':
    'negative', 'disgruntled': 'negative', 'disgust': 'negative', 'disgusted': 'negative',
    'disgustedly': 'negative', 'disgustful': 'negative', 'disgustfully': 'negative', 'disgusting':
    'negative', 'disgustingly': 'negative', 'dishearten': 'negative', 'disheartening': 'negative',
    'dishearteningly': 'negative', 'dishonest': 'negative', 'dishonestly': 'negative',
    'dishonesty': 'negative', 'dishonor': 'negative', 'dishonorable': 'negative', 'dishonorablely':
    'negative', 'disillusion': 'negative', 'disillusioned': 'negative', 'disinclination':
    'negative', 'disinclined': 'negative', 'disingenuous': 'negative', 'disingenuously':
    'negative', 'disintegrate': 'negative', 'disintegration': 'negative', 'disinterest':
    'negative', 'disinterested': 'negative', 'dislike': 'negative', 'dislocated': 'negative',
    'disloyal': 'negative', 'disloyalty': 'negative', 'dismal': 'negative', 'dismally': 'negative',
    'dismalness': 'negative', 'dismay': 'negative', 'dismayed': 'negative', 'dismaying':
    'negative', 'dismayingly': 'negative', 'dismissive': 'negative', 'dismissively': 'negative',
    'disobedience': 'negative', 'disobedient': 'negative', 'disobey': 'negative', 'disorder':
    'negative', 'disordered': 'negative', 'disorderly': 'negative', 'disorganized': 'negative',
    'disorient': 'negative', 'disoriented': 'negative', 'disown': 'negative', 'disparage':
    'negative', 'disparaging': 'negative', 'disparagingly': 'negative', 'dispensable': 'negative',
    'dispirit': 'negative', 'dispirited': 'negative', 'dispiritedly': 'negative', 'dispiriting':
    'negative', 'displace': 'negative', 'displaced': 'negative', 'displease': 'negative',
    'displeasing': 'negative', 'displeasure': 'negative', 'disposition': 'neutral',
    'disproportionate': 'negative', 'disprove': 'negative', 'disputable': 'negative', 'dispute':
    'negative', 'disputed': 'negative', 'disquiet': 'negative', 'disquieting': 'negative',
    'disquietingly': 'negative', 'disquietude': 'negative', 'disregard': 'negative',
    'disregardful': 'negative', 'disreputable': 'negative', 'disrepute': 'negative', 'disrespect':
    'negative', 'disrespectable': 'negative', 'disrespectablity': 'negative', 'disrespectful':
    'negative', 'disrespectfully': 'negative', 'disrespectfulness': 'negative', 'disrespecting':
    'negative', 'disrupt': 'negative', 'disruption': 'negative', 'disruptive': 'negative',
    'dissatisfaction': 'negative', 'dissatisfactory': 'negative', 'dissatisfied': 'negative',
    'dissatisfy': 'negative', 'dissatisfying': 'negative', 'dissemble': 'negative', 'dissembler':
    'negative', 'dissension': 'negative', 'dissent': 'negative', 'dissenter': 'negative',
    'dissention': 'negative', 'disservice': 'negative', 'dissidence': 'negative', 'dissident':
    'negative', 'dissidents': 'negative', 'dissocial': 'negative', 'dissolute': 'negative',
    'dissolution': 'negative', 'dissonance': 'negative', 'dissonant': 'negative', 'dissonantly':
    'negative', 'dissuade': 'negative', 'dissuasive': 'negative', 'distaste': 'negative',
    'distasteful': 'negative', 'distastefully': 'negative', 'distinct': 'positive', 'distinction':
    'positive', 'distinctive': 'positive', 'distinctly': 'neutral', 'distinguish': 'positive',
    'distinguished': 'positive', 'distort': 'negative', 'distortion': 'negative', 'distract':
    'negative', 'distracting': 'negative', 'distraction': 'negative', 'distraught': 'negative',
    'distraughtly': 'negative', 'distraughtness': 'negative', 'distress': 'negative', 'distressed':
    'negative', 'distressing': 'negative', 'distressingly': 'negative', 'distrust': 'negative',
    'distrustful': 'negative', 'distrusting': 'negative', 'disturb': 'negative', 'disturbed':
    'negative', 'disturbed-let': 'negative', 'disturbing': 'negative', 'disturbingly': 'negative',
    'disunity': 'negative', 'disvalue': 'negative', 'divergent': 'negative', 'diversified':
    'positive', 'divide': 'negative', 'divided': 'negative', 'divine': 'positive', 'divinely':
    'positive', 'division': 'negative', 'divisive': 'negative', 'divisively': 'negative',
    'divisiveness': 'negative', 'divorce': 'negative', 'divorced': 'negative', 'dizzing':
    'negative', 'dizzingly': 'negative', 'dizzy': 'negative', 'doddering': 'negative', 'dodge':
    'positive', 'dodgey': 'negative', 'dogged': 'negative', 'doggedly': 'negative', 'dogmatic':
    'negative', 'doldrums': 'negative', 'dominance': 'negative', 'dominant': 'neutral', 'dominate':
    'negative', 'domination': 'negative', 'domineer': 'negative', 'domineering': 'negative',
    'doom': 'negative', 'doomsday': 'negative', 'dope': 'negative', 'dote': 'positive', 'dotingly':
    'positive', 'doubt': 'negative', 'doubtful': 'negative', 'doubtfully': 'negative', 'doubtless':
    'positive', 'doubts': 'negative', 'down': 'negative', 'downbeat': 'negative', 'downcast':
    'negative', 'downer': 'negative', 'downfall': 'negative', 'downfallen': 'negative',
    'downgrade': 'negative', 'downhearted': 'negative', 'downheartedly': 'negative', 'downright':
    'neutral', 'downside': 'negative', 'drab': 'negative', 'draconian': 'negative', 'draconic':
    'negative', 'dragon': 'negative', 'dragons': 'negative', 'dragoon': 'negative', 'drain':
    'negative', 'drama': 'negative', 'dramatic': 'neutral', 'dramatically': 'neutral', 'drastic':
    'negative', 'drastically': 'negative', 'dread': 'negative', 'dreadful': 'negative',
    'dreadfully': 'negative', 'dreadfulness': 'negative', 'dream': 'positive', 'dreamland':
    'positive', 'dreams': 'positive', 'dreamy': 'positive', 'dreary': 'negative', 'drive':
    'positive', 'driven': 'positive', 'drones': 'negative', 'droop': 'negative', 'drought':
    'negative', 'drowning': 'negative', 'drunk': 'negative', 'drunkard': 'negative', 'drunken':
    'negative', 'dubious': 'negative', 'dubiously': 'negative', 'dubitable': 'negative', 'dud':
    'negative', 'dull': 'negative', 'dullard': 'negative', 'dumb': 'negative', 'dumbfound':
    'negative', 'dumbfounded': 'negative', 'dummy': 'negative', 'dump': 'negative', 'dunce':
    'negative', 'dungeon': 'negative', 'dungeons': 'negative', 'dupe': 'negative', 'durability':
    'positive', 'durable': 'positive', 'dusty': 'negative', 'duty': 'neutral', 'dwindle':
    'negative', 'dwindling': 'negative', 'dying': 'negative', 'dynamic': 'positive', 'eager':
    'positive', 'eagerly': 'positive', 'eagerness': 'positive', 'earnest': 'positive', 'earnestly':
    'positive', 'earnestness': 'positive', 'earsplitting': 'negative', 'ease': 'positive',
    'easier': 'positive', 'easiest': 'positive', 'easily': 'positive', 'easiness': 'positive',
    'easy': 'positive', 'easygoing': 'positive', 'ebullience': 'positive', 'ebullient': 'positive',
    'ebulliently': 'positive', 'eccentric': 'negative', 'eccentricity': 'negative', 'eclectic':
    'positive', 'economical': 'positive', 'ecstasies': 'positive', 'ecstasy': 'positive',
    'ecstatic': 'positive', 'ecstatically': 'positive', 'edgy': 'negative', 'edify': 'positive',
    'educable': 'positive', 'educated': 'positive', 'educational': 'positive', 'effective':
    'positive', 'effectively': 'neutral', 'effectiveness': 'positive', 'effectual': 'positive',
    'efficacious': 'positive', 'efficiency': 'positive', 'efficient': 'positive', 'effigy':
    'negative', 'effortless': 'positive', 'effortlessly': 'positive', 'effrontery': 'negative',
    'effusion': 'positive', 'effusive': 'positive', 'effusively': 'positive', 'effusiveness':
    'positive', 'egalitarian': 'positive', 'ego': 'negative', 'egocentric': 'negative', 'egomania':
    'negative', 'egotism': 'negative', 'egotistical': 'negative', 'egotistically': 'negative',
    'egregious': 'negative', 'egregiously': 'negative', 'ejaculate': 'negative', 'elaborate':
    'neutral', 'elan': 'positive', 'elate': 'positive', 'elated': 'positive', 'elatedly':
    'positive', 'elation': 'positive', 'election-rigger': 'negative', 'electrification':
    'positive', 'electrify': 'positive', 'elegance': 'positive', 'elegant': 'positive',
    'elegantly': 'positive', 'elevate': 'positive', 'elevated': 'positive', 'eligible': 'positive',
    'eliminate': 'negative', 'elimination': 'negative', 'elite': 'positive', 'eloquence':
    'positive', 'eloquent': 'positive', 'eloquently': 'positive', 'else': 'neutral', 'emaciated':
    'negative', 'emancipate': 'positive', 'emasculate': 'negative', 'embarrass': 'negative',
    'embarrassing': 'negative', 'embarrassingly': 'negative', 'embarrassment': 'negative',
    'embattled': 'negative', 'embellish': 'positive', 'embodiment': 'neutral', 'embolden':
    'positive', 'embrace': 'positive', 'embroil': 'negative', 'embroiled': 'negative',
    'embroilment': 'negative', 'eminence': 'positive', 'eminent': 'positive', 'emotion': 'neutral',
    'emotional': 'negative', 'emotions': 'neutral', 'empathize': 'negative', 'empathy': 'negative',
    'emphasise': 'neutral', 'emphatic': 'negative', 'emphatically': 'negative', 'empower':
    'positive', 'empowerment': 'positive', 'emptiness': 'negative', 'empty': 'negative', 'enable':
    'positive', 'enchant': 'positive', 'enchanted': 'positive', 'enchanting': 'positive',
    'enchantingly': 'positive', 'encourage': 'positive', 'encouragement': 'positive',
    'encouraging': 'positive', 'encouragingly': 'positive', 'encroach': 'negative', 'encroachment':
    'negative', 'endanger': 'negative', 'endear': 'positive', 'endearing': 'positive', 'endless':
    'negative', 'endorse': 'positive', 'endorsement': 'positive', 'endorser': 'positive',
    'endurable': 'positive', 'endure': 'positive', 'enduring': 'positive', 'enemies': 'negative',
    'enemy': 'negative', 'energetic': 'positive', 'energize': 'positive', 'enervate': 'negative',
    'enfeeble': 'negative', 'enflame': 'negative', 'engage': 'neutral', 'engaging': 'positive',
    'engross': 'neutral', 'engrossing': 'positive', 'engulf': 'negative', 'enhance': 'positive',
    'enhanced': 'positive', 'enhancement': 'positive', 'enjoin': 'negative', 'enjoy': 'positive',
    'enjoyable': 'positive', 'enjoyably': 'positive', 'enjoyment': 'positive', 'enlighten':
    'positive', 'enlightenment': 'positive', 'enliven': 'positive', 'enmity': 'negative',
    'ennoble': 'positive', 'enormities': 'negative', 'enormity': 'negative', 'enormous':
    'negative', 'enormously': 'negative', 'enough': 'neutral', 'enrage': 'negative', 'enraged':
    'negative', 'enrapt': 'positive', 'enrapture': 'positive', 'enraptured': 'positive', 'enrich':
    'positive', 'enrichment': 'positive', 'enslave': 'negative', 'ensure': 'positive', 'entangle':
    'negative', 'entanglement': 'negative', 'enterprising': 'positive', 'entertain': 'positive',
    'entertaining': 'positive', 'enthral': 'positive', 'enthrall': 'positive', 'enthralled':
    'positive', 'enthuse': 'positive', 'enthusiasm': 'positive', 'enthusiast': 'positive',
    'enthusiastic': 'positive', 'enthusiastically': 'positive', 'entice': 'positive', 'enticing':
    'positive', 'enticingly': 'positive', 'entire': 'neutral', 'entirely': 'neutral', 'entrance':
    'positive', 'entranced': 'positive', 'entrancing': 'positive', 'entrap': 'negative',
    'entrapment': 'negative', 'entreat': 'positive', 'entreatingly': 'positive', 'entrenchment':
    'neutral', 'entrust': 'positive', 'enviable': 'positive', 'enviably': 'positive', 'envious':
    'negative', 'enviously': 'negative', 'enviousness': 'negative', 'envision': 'positive',
    'envisions': 'positive', 'envy': 'negative', 'epic': 'positive', 'epidemic': 'negative',
    'epitome': 'positive', 'equality': 'positive', 'equitable': 'positive', 'equivocal':
    'negative', 'eradicate': 'negative', 'erase': 'negative', 'erode': 'negative', 'erosion':
    'negative', 'err': 'negative', 'errant': 'negative', 'erratic': 'negative', 'erratically':
    'negative', 'erroneous': 'negative', 'erroneously': 'negative', 'error': 'negative', 'erudite':
    'positive', 'escapade': 'negative', 'eschew': 'negative', 'esoteric': 'negative', 'especially':
    'positive', 'essential': 'positive', 'established': 'positive', 'esteem': 'positive',
    'estranged': 'negative', 'eternal': 'negative', 'eternity': 'positive', 'ethical': 'positive',
    'eulogize': 'positive', 'euphoria': 'positive', 'euphoric': 'positive', 'euphorically':
    'positive', 'evade': 'negative', 'evaluate': 'neutral', 'evaluation': 'neutral', 'evasion':
    'negative', 'evasive': 'negative', 'even': 'positive', 'evenly': 'positive', 'eventful':
    'positive', 'everlasting': 'positive', 'evident': 'positive', 'evidently': 'positive', 'evil':
    'negative', 'evildoer': 'negative', 'evils': 'negative', 'eviscerate': 'negative', 'evocative':
    'positive', 'exacerbate': 'negative', 'exact': 'neutral', 'exacting': 'negative', 'exactly':
    'neutral', 'exaggerate': 'negative', 'exaggeration': 'negative', 'exalt': 'positive',
    'exaltation': 'positive', 'exalted': 'positive', 'exaltedly': 'positive', 'exalting':
    'positive', 'exaltingly': 'positive', 'exasperate': 'negative', 'exasperating': 'negative',
    'exasperatingly': 'negative', 'exasperation': 'negative', 'exceed': 'positive', 'exceeding':
    'positive', 'exceedingly': 'positive', 'excel': 'positive', 'excellence': 'positive',
    'excellency': 'positive', 'excellent': 'positive', 'excellently': 'positive', 'exceptional':
    'positive', 'exceptionally': 'positive', 'excessive': 'negative', 'excessively': 'negative',
    'excite': 'positive', 'excited': 'positive', 'excitedly': 'positive', 'excitedness':
    'positive', 'excitement': 'positive', 'exciting': 'positive', 'excitingly': 'positive',
    'exclaim': 'negative', 'exclude': 'negative', 'exclusion': 'negative', 'exclusive': 'positive',
    'exclusively': 'neutral', 'excoriate': 'negative', 'excruciating': 'negative',
    'excruciatingly': 'negative', 'excusable': 'positive', 'excuse': 'negative', 'excuses':
    'negative', 'execrate': 'negative', 'exemplar': 'positive', 'exemplary': 'positive', 'exhaust':
    'negative', 'exhaustion': 'negative', 'exhaustive': 'positive', 'exhaustively': 'positive',
    'exhilarate': 'positive', 'exhilarating': 'positive', 'exhilaratingly': 'positive',
    'exhilaration': 'positive', 'exhort': 'negative', 'exile': 'negative', 'exonerate': 'positive',
    'exorbitant': 'negative', 'exorbitantance': 'negative', 'exorbitantly': 'negative',
    'expansive': 'positive', 'expectation': 'neutral', 'expediencies': 'negative', 'expedient':
    'negative', 'expel': 'negative', 'expensive': 'negative', 'experienced': 'positive', 'expert':
    'positive', 'expertly': 'positive', 'expire': 'negative', 'explicit': 'positive', 'explicitly':
    'positive', 'explode': 'negative', 'exploit': 'negative', 'exploitation': 'negative',
    'explosive': 'negative', 'expose': 'negative', 'exposed': 'negative', 'expound': 'neutral',
    'expression': 'neutral', 'expressions': 'neutral', 'expressive': 'positive', 'expropriate':
    'negative', 'expropriation': 'negative', 'expulse': 'negative', 'expunge': 'negative',
    'exquisite': 'positive', 'exquisitely': 'positive', 'extemporize': 'neutral', 'extensive':
    'neutral', 'extensively': 'neutral', 'exterminate': 'negative', 'extermination': 'negative',
    'extinguish': 'negative', 'extol': 'positive', 'extoll': 'positive', 'extort': 'negative',
    'extortion': 'negative', 'extraneous': 'negative', 'extraordinarily': 'positive',
    'extraordinary': 'positive', 'extravagance': 'negative', 'extravagant': 'negative',
    'extravagantly': 'negative', 'extreme': 'negative', 'extremely': 'negative', 'extremism':
    'negative', 'extremist': 'negative', 'extremists': 'negative', 'exuberance': 'positive',
    'exuberant': 'positive', 'exuberantly': 'positive', 'exult': 'positive', 'exultation':
    'positive', 'exultingly': 'positive', 'eyebrows': 'neutral', 'fabricate': 'negative',
    'fabrication': 'negative', 'fabulous': 'positive', 'fabulously': 'positive', 'facetious':
    'negative', 'facetiously': 'negative', 'facilitate': 'positive', 'fact': 'neutral', 'facts':
    'neutral', 'factual': 'neutral', 'fading': 'negative', 'fail': 'negative', 'failing':
    'negative', 'failure': 'negative', 'failures': 'negative', 'faint': 'negative', 'fainthearted':
    'negative', 'fair': 'positive', 'fairly': 'positive', 'fairness': 'positive', 'faith':
    'positive', 'faithful': 'positive', 'faithfully': 'positive', 'faithfulness': 'positive',
    'faithless': 'negative', 'fake': 'negative', 'fall': 'negative', 'fallacies': 'negative',
    'fallacious': 'negative', 'fallaciously': 'negative', 'fallaciousness': 'negative', 'fallacy':
    'negative', 'fallout': 'negative', 'false': 'negative', 'falsehood': 'negative', 'falsely':
    'negative', 'falsify': 'negative', 'falter': 'negative', 'fame': 'positive', 'famed':
    'positive', 'familiar': 'neutral', 'famine': 'negative', 'famished': 'negative', 'famous':
    'positive', 'famously': 'positive', 'fanatic': 'negative', 'fanatical': 'negative',
    'fanatically': 'negative', 'fanaticism': 'negative', 'fanatics': 'negative', 'fanciful':
    'negative', 'fancy': 'positive', 'fanfare': 'positive', 'fantastic': 'positive',
    'fantastically': 'positive', 'fantasy': 'positive', 'far-fetched': 'negative', 'far-reaching':
    'neutral', 'farce': 'negative', 'farcical': 'negative', 'farcical-yet-provocative': 'negative',
    'farcically': 'negative', 'farfetched': 'negative', 'farsighted': 'positive', 'fascinate':
    'positive', 'fascinating': 'positive', 'fascinatingly': 'positive', 'fascination': 'positive',
    'fascism': 'negative', 'fascist': 'negative', 'fashionable': 'positive', 'fashionably':
    'positive', 'fast': 'neutral', 'fast-growing': 'positive', 'fast-paced': 'positive',
    'fastest-growing': 'positive', 'fastidious': 'negative', 'fastidiously': 'negative',
    'fastuous': 'negative', 'fat': 'negative', 'fatal': 'negative', 'fatalistic': 'negative',
    'fatalistically': 'negative', 'fatally': 'negative', 'fateful': 'negative', 'fatefully':
    'negative', 'fathom': 'positive', 'fathomless': 'negative', 'fatigue': 'negative', 'fatty':
    'negative', 'fatuity': 'negative', 'fatuous': 'negative', 'fatuously': 'negative', 'fault':
    'negative', 'faulty': 'negative', 'favor': 'positive', 'favorable': 'positive', 'favored':
    'positive', 'favorite': 'positive', 'favour': 'positive', 'fawn': 'both', 'fawningly':
    'negative', 'faze': 'negative', 'fear': 'negative', 'fearful': 'negative', 'fearfully':
    'negative', 'fearless': 'positive', 'fearlessly': 'positive', 'fears': 'negative', 'fearsome':
    'negative', 'feasible': 'positive', 'feasibly': 'positive', 'feat': 'positive', 'featly':
    'positive', 'feckless': 'negative', 'feeble': 'negative', 'feeblely': 'negative',
    'feebleminded': 'negative', 'feel': 'neutral', 'feeling': 'neutral', 'feelings': 'neutral',
    'feels': 'neutral', 'feign': 'negative', 'feint': 'negative', 'feisty': 'positive',
    'felicitate': 'positive', 'felicitous': 'positive', 'felicity': 'positive', 'fell': 'negative',
    'felon': 'negative', 'felonious': 'negative', 'felt': 'neutral', 'ferocious': 'negative',
    'ferociously': 'negative', 'ferocity': 'negative', 'fertile': 'positive', 'fervent':
    'positive', 'fervently': 'positive', 'fervid': 'positive', 'fervidly': 'positive', 'fervor':
    'positive', 'festive': 'positive', 'fetid': 'negative', 'fever': 'negative', 'feverish':
    'negative', 'fiasco': 'negative', 'fiat': 'negative', 'fib': 'negative', 'fibber': 'negative',
    'fickle': 'negative', 'fiction': 'negative', 'fictional': 'negative', 'fictitious': 'negative',
    'fidelity': 'positive', 'fidget': 'negative', 'fidgety': 'negative', 'fiend': 'negative',
    'fiendish': 'negative', 'fierce': 'negative', 'fiery': 'positive', 'fight': 'negative',
    'figurehead': 'negative', 'filth': 'negative', 'filthy': 'negative', 'finagle': 'negative',
    'finally': 'neutral', 'fine': 'positive', 'finely': 'positive', 'firm': 'neutral', 'firmly':
    'neutral', 'first-class': 'positive', 'first-rate': 'positive', 'fissures': 'negative', 'fist':
    'negative', 'fit': 'positive', 'fitting': 'positive', 'fixer': 'neutral', 'flabbergast':
    'negative', 'flabbergasted': 'negative', 'flagging': 'negative', 'flagrant': 'negative',
    'flagrantly': 'negative', 'flair': 'positive', 'flak': 'negative', 'flake': 'negative',
    'flakey': 'negative', 'flaky': 'negative', 'flame': 'positive', 'flash': 'negative', 'flashy':
    'negative', 'flat-out': 'negative', 'flatter': 'positive', 'flattering': 'positive',
    'flatteringly': 'positive', 'flaunt': 'negative', 'flaw': 'negative', 'flawed': 'negative',
    'flawless': 'positive', 'flawlessly': 'positive', 'flaws': 'negative', 'fleer': 'negative',
    'fleeting': 'negative', 'flexible': 'positive', 'flighty': 'negative', 'flimflam': 'negative',
    'flimsy': 'negative', 'flirt': 'negative', 'flirty': 'negative', 'floor': 'neutral', 'floored':
    'negative', 'flounder': 'negative', 'floundering': 'negative', 'flourish': 'positive',
    'flourishing': 'positive', 'flout': 'negative', 'fluent': 'positive', 'fluster': 'negative',
    'foe': 'negative', 'fond': 'positive', 'fondly': 'positive', 'fondness': 'positive', 'fool':
    'negative', 'foolhardy': 'negative', 'foolish': 'negative', 'foolishly': 'negative',
    'foolishness': 'negative', 'foolproof': 'positive', 'forbid': 'negative', 'forbidden':
    'negative', 'forbidding': 'negative', 'force': 'negative', 'forceful': 'negative',
    'foreboding': 'negative', 'forebodingly': 'negative', 'foremost': 'positive', 'foresight':
    'positive', 'foretell': 'neutral', 'forfeit': 'negative', 'forgave': 'positive', 'forged':
    'negative', 'forget': 'negative', 'forgetful': 'negative', 'forgetfully': 'negative',
    'forgetfulness': 'negative', 'forgive': 'positive', 'forgiven': 'positive', 'forgiveness':
    'positive', 'forgiving': 'positive', 'forgivingly': 'positive', 'forlorn': 'negative',
    'forlornly': 'negative', 'formidable': 'negative', 'forsake': 'negative', 'forsaken':
    'negative', 'forsee': 'neutral', 'forswear': 'negative', 'forthright': 'neutral', 'fortitude':
    'positive', 'fortress': 'neutral', 'fortuitous': 'positive', 'fortuitously': 'positive',
    'fortunate': 'positive', 'fortunately': 'positive', 'fortune': 'positive', 'foul': 'negative',
    'foully': 'negative', 'foulness': 'negative', 'fractious': 'negative', 'fractiously':
    'negative', 'fracture': 'negative', 'fragile': 'negative', 'fragmented': 'negative',
    'fragrant': 'positive', 'frail': 'negative', 'frank': 'positive', 'frankly': 'neutral',
    'frantic': 'negative', 'frantically': 'negative', 'franticly': 'negative', 'fraternize':
    'negative', 'fraud': 'negative', 'fraudulent': 'negative', 'fraught': 'negative', 'frazzle':
    'negative', 'frazzled': 'negative', 'freak': 'negative', 'freakish': 'negative', 'freakishly':
    'negative', 'free': 'positive', 'freedom': 'positive', 'freedoms': 'positive', 'frenetic':
    'negative', 'frenetically': 'negative', 'frenzied': 'negative', 'frenzy': 'negative',
    'frequent': 'neutral', 'fresh': 'positive', 'fret': 'negative', 'fretful': 'negative',
    'friction': 'negative', 'frictions': 'negative', 'friend': 'positive', 'friendliness':
    'positive', 'friendly': 'positive', 'friends': 'positive', 'friendship': 'positive', 'friggin':
    'negative', 'fright': 'negative', 'frighten': 'negative', 'frightening': 'negative',
    'frighteningly': 'negative', 'frightful': 'negative', 'frightfully': 'negative', 'frigid':
    'negative', 'frivolous': 'negative', 'frolic': 'positive', 'frown': 'negative', 'frozen':
    'negative', 'fruitful': 'positive', 'fruitless': 'negative', 'fruitlessly': 'negative',
    'frustrate': 'negative', 'frustrated': 'negative', 'frustrating': 'negative', 'frustratingly':
    'negative', 'frustration': 'negative', 'fudge': 'negative', 'fugitive': 'negative',
    'fulfillment': 'positive', 'full': 'neutral', 'full-blown': 'negative', 'full-fledged':
    'positive', 'full-scale': 'neutral', 'fully': 'neutral', 'fulminate': 'negative', 'fumble':
    'negative', 'fume': 'negative', 'fun': 'negative', 'functional': 'positive', 'fundamental':
    'neutral', 'fundamentalism': 'negative', 'fundamentally': 'neutral', 'funded': 'neutral',
    'funny': 'positive', 'furious': 'negative', 'furiously': 'negative', 'furor': 'negative',
    'further': 'neutral', 'furthermore': 'neutral', 'fury': 'negative', 'fuss': 'negative',
    'fussy': 'negative', 'fustigate': 'negative', 'fusty': 'negative', 'futile': 'negative',
    'futilely': 'negative', 'futility': 'negative', 'fuzzy': 'negative', 'gabble': 'negative',
    'gaff': 'negative', 'gaffe': 'negative', 'gaga': 'negative', 'gaggle': 'negative', 'gaiety':
    'positive', 'gaily': 'positive', 'gain': 'positive', 'gainful': 'positive', 'gainfully':
    'positive', 'gainsay': 'negative', 'gainsayer': 'negative', 'gall': 'negative', 'gallant':
    'positive', 'gallantly': 'positive', 'galling': 'negative', 'gallingly': 'negative', 'galore':
    'positive', 'galvanize': 'neutral', 'gamble': 'negative', 'game': 'negative', 'gape':
    'negative', 'garbage': 'negative', 'garish': 'negative', 'gasp': 'negative', 'gauche':
    'negative', 'gaudy': 'negative', 'gawk': 'negative', 'gawky': 'negative', 'geezer': 'negative',
    'gem': 'positive', 'gems': 'positive', 'generosity': 'positive', 'generous': 'positive',
    'generously': 'positive', 'genial': 'positive', 'genius': 'positive', 'genocide': 'negative',
    'gentle': 'positive', 'genuine': 'positive', 'germane': 'positive', 'gestures': 'neutral',
    'get-rich': 'negative', 'ghastly': 'negative', 'ghetto': 'negative', 'giant': 'neutral',
    'giants': 'neutral', 'gibber': 'negative', 'gibberish': 'negative', 'gibe': 'negative',
    'giddy': 'positive', 'gifted': 'positive', 'gigantic': 'neutral', 'glad': 'positive',
    'gladden': 'positive', 'gladly': 'positive', 'gladness': 'positive', 'glamorous': 'positive',
    'glare': 'negative', 'glaring': 'negative', 'glaringly': 'negative', 'glean': 'neutral',
    'glee': 'positive', 'gleeful': 'positive', 'gleefully': 'positive', 'glib': 'negative',
    'glibly': 'negative', 'glimmer': 'positive', 'glimmering': 'positive', 'glisten': 'positive',
    'glistening': 'positive', 'glitch': 'negative', 'glitter': 'positive', 'gloat': 'both',
    'gloatingly': 'negative', 'gloom': 'negative', 'gloomy': 'negative', 'glorify': 'positive',
    'glorious': 'positive', 'gloriously': 'positive', 'glory': 'positive', 'gloss': 'negative',
    'glossy': 'positive', 'glow': 'positive', 'glower': 'negative', 'glowing': 'positive',
    'glowingly': 'positive', 'glum': 'negative', 'glut': 'negative', 'gnawing': 'negative',
    'go-ahead': 'positive', 'goad': 'negative', 'goading': 'negative', 'god-awful': 'negative',
    'god-given': 'positive', 'goddam': 'negative', 'goddamn': 'negative', 'godlike': 'positive',
    'gold': 'positive', 'golden': 'positive', 'good': 'positive', 'goodly': 'positive', 'goodness':
    'positive', 'goodwill': 'positive', 'goof': 'negative', 'gorgeous': 'positive', 'gorgeously':
    'positive', 'gossip': 'negative', 'grace': 'positive', 'graceful': 'positive', 'gracefully':
    'positive', 'graceless': 'negative', 'gracelessly': 'negative', 'gracious': 'positive',
    'graciously': 'positive', 'graciousness': 'positive', 'graft': 'negative', 'grail': 'positive',
    'grand': 'positive', 'grandeur': 'positive', 'grandiose': 'negative', 'grapple': 'negative',
    'grate': 'negative', 'grateful': 'positive', 'gratefully': 'positive', 'gratification':
    'positive', 'gratify': 'positive', 'gratifying': 'positive', 'gratifyingly': 'positive',
    'grating': 'negative', 'gratitude': 'positive', 'gratuitous': 'negative', 'gratuitously':
    'negative', 'grave': 'negative', 'gravely': 'negative', 'great': 'positive', 'greatest':
    'positive', 'greatly': 'neutral', 'greatness': 'positive', 'greed': 'negative', 'greedy':
    'negative', 'greet': 'positive', 'grief': 'negative', 'grievance': 'negative', 'grievances':
    'negative', 'grieve': 'negative', 'grieving': 'negative', 'grievous': 'negative', 'grievously':
    'negative', 'grill': 'negative', 'grim': 'negative', 'grimace': 'negative', 'grin': 'positive',
    'grind': 'negative', 'gripe': 'negative', 'grisly': 'negative', 'grit': 'positive', 'gritty':
    'negative', 'groove': 'positive', 'gross': 'negative', 'grossly': 'negative', 'grotesque':
    'negative', 'grouch': 'negative', 'grouchy': 'negative', 'groundbreaking': 'positive',
    'groundless': 'negative', 'grouse': 'negative', 'growing': 'neutral', 'growl': 'negative',
    'grudge': 'negative', 'grudges': 'negative', 'grudging': 'negative', 'grudgingly': 'negative',
    'gruesome': 'negative', 'gruesomely': 'negative', 'gruff': 'negative', 'grumble': 'negative',
    'guarantee': 'positive', 'guardian': 'positive', 'guidance': 'positive', 'guile': 'negative',
    'guilt': 'negative', 'guiltily': 'negative', 'guiltless': 'positive', 'guilty': 'negative',
    'gullible': 'negative', 'gumption': 'positive', 'gush': 'positive', 'gusto': 'positive',
    'gutsy': 'positive', 'haggard': 'negative', 'haggle': 'negative', 'hail': 'positive',
    'halcyon': 'positive', 'hale': 'positive', 'halfhearted': 'negative', 'halfheartedly':
    'negative', 'halfway': 'neutral', 'hallowed': 'positive', 'hallucinate': 'negative',
    'hallucination': 'negative', 'halt': 'neutral', 'hamper': 'negative', 'hamstring': 'negative',
    'hamstrung': 'negative', 'handicapped': 'negative', 'handily': 'positive', 'handsome':
    'positive', 'handy': 'positive', 'hanker': 'positive', 'haphazard': 'negative', 'hapless':
    'negative', 'happily': 'positive', 'happiness': 'positive', 'happy': 'positive', 'harangue':
    'negative', 'harass': 'negative', 'harassment': 'negative', 'harboring': 'negative', 'harbors':
    'negative', 'hard': 'negative', 'hard-hit': 'negative', 'hard-line': 'negative', 'hard-liner':
    'negative', 'hard-working': 'positive', 'hardball': 'negative', 'harden': 'negative',
    'hardened': 'negative', 'hardheaded': 'negative', 'hardhearted': 'negative', 'hardier':
    'positive', 'hardliner': 'negative', 'hardliners': 'negative', 'hardly': 'negative',
    'hardship': 'negative', 'hardships': 'negative', 'hardy': 'positive', 'harm': 'negative',
    'harmful': 'negative', 'harmless': 'positive', 'harmonious': 'positive', 'harmoniously':
    'positive', 'harmonize': 'positive', 'harmony': 'positive', 'harms': 'negative', 'harpy':
    'negative', 'harridan': 'negative', 'harried': 'negative', 'harrow': 'negative', 'harsh':
    'negative', 'harshly': 'negative', 'hassle': 'negative', 'haste': 'negative', 'hasty':
    'negative', 'hate': 'negative', 'hateful': 'negative', 'hatefully': 'negative', 'hatefulness':
    'negative', 'hater': 'negative', 'hatred': 'negative', 'haughtily': 'negative', 'haughty':
    'negative', 'haunt': 'negative', 'haunting': 'negative', 'haven': 'positive', 'havoc':
    'negative', 'hawkish': 'negative', 'hazard': 'negative', 'hazardous': 'negative', 'hazy':
    'negative', 'headache': 'negative', 'headaches': 'negative', 'headway': 'positive', 'heady':
    'positive', 'heal': 'positive', 'healthful': 'positive', 'healthy': 'positive', 'heart':
    'positive', 'heartbreak': 'negative', 'heartbreaker': 'negative', 'heartbreaking': 'negative',
    'heartbreakingly': 'negative', 'hearten': 'positive', 'heartening': 'positive', 'heartfelt':
    'positive', 'heartily': 'positive', 'heartless': 'negative', 'heartrending': 'negative',
    'heartwarming': 'positive', 'heathen': 'negative', 'heaven': 'positive', 'heavenly':
    'positive', 'heavily': 'negative', 'heavy-duty': 'neutral', 'heavy-handed': 'negative',
    'heavyhearted': 'negative', 'heck': 'negative', 'heckle': 'negative', 'hectic': 'negative',
    'hedge': 'negative', 'hedonistic': 'negative', 'heedless': 'negative', 'hefty': 'neutral',
    'hegemonism': 'negative', 'hegemonistic': 'negative', 'hegemony': 'negative', 'heinous':
    'negative', 'hell': 'negative', 'hell-bent': 'negative', 'hellion': 'negative', 'help':
    'positive', 'helpful': 'positive', 'helpless': 'negative', 'helplessly': 'negative',
    'helplessness': 'negative', 'herald': 'positive', 'heresy': 'negative', 'heretic': 'negative',
    'heretical': 'negative', 'hero': 'positive', 'heroic': 'positive', 'heroically': 'positive',
    'heroine': 'positive', 'heroize': 'positive', 'heros': 'positive', 'hesitant': 'negative',
    'hideous': 'negative', 'hideously': 'negative', 'hideousness': 'negative', 'high': 'neutral',
    'high-powered': 'neutral', 'high-quality': 'positive', 'highlight': 'positive', 'hilarious':
    'positive', 'hilariously': 'positive', 'hilariousness': 'positive', 'hilarity': 'positive',
    'hinder': 'negative', 'hindrance': 'negative', 'historic': 'positive', 'hm': 'neutral', 'hmm':
    'neutral', 'hoard': 'negative', 'hoax': 'negative', 'hobble': 'negative', 'hole': 'negative',
    'hollow': 'negative', 'holy': 'positive', 'homage': 'positive', 'honest': 'positive',
    'honestly': 'positive', 'honesty': 'positive', 'honeymoon': 'positive', 'honor': 'positive',
    'honorable': 'positive', 'hoodwink': 'negative', 'hope': 'positive', 'hopeful': 'positive',
    'hopefully': 'positive', 'hopefulness': 'positive', 'hopeless': 'negative', 'hopelessly':
    'negative', 'hopelessness': 'negative', 'hopes': 'positive', 'horde': 'negative', 'horrendous':
    'negative', 'horrendously': 'negative', 'horrible': 'negative', 'horribly': 'negative',
    'horrid': 'negative', 'horrific': 'negative', 'horrifically': 'negative', 'horrify':
    'negative', 'horrifying': 'negative', 'horrifyingly': 'negative', 'horror': 'negative',
    'horrors': 'negative', 'hospitable': 'positive', 'hostage': 'negative', 'hostile': 'negative',
    'hostilities': 'negative', 'hostility': 'negative', 'hot': 'positive', 'hotbeds': 'negative',
    'hothead': 'negative', 'hotheaded': 'negative', 'hothouse': 'negative', 'however': 'neutral',
    'hubris': 'negative', 'huckster': 'negative', 'hug': 'positive', 'huge': 'neutral', 'humane':
    'positive', 'humanists': 'positive', 'humanity': 'positive', 'humankind': 'positive', 'humble':
    'positive', 'humbling': 'negative', 'humiliate': 'negative', 'humiliating': 'negative',
    'humiliation': 'negative', 'humility': 'positive', 'humor': 'positive', 'humorous': 'positive',
    'humorously': 'positive', 'humour': 'positive', 'humourous': 'positive', 'hunger': 'negative',
    'hungry': 'negative', 'hurt': 'negative', 'hurtful': 'negative', 'hustler': 'negative',
    'hypnotize': 'neutral', 'hypocrisy': 'negative', 'hypocrite': 'negative', 'hypocrites':
    'negative', 'hypocritical': 'negative', 'hypocritically': 'negative', 'hysteria': 'negative',
    'hysteric': 'negative', 'hysterical': 'negative', 'hysterically': 'negative', 'hysterics':
    'negative', 'icy': 'negative', 'idea': 'neutral', 'ideal': 'positive', 'idealism': 'positive',
    'idealist': 'positive', 'idealize': 'positive', 'ideally': 'positive', 'idiocies': 'negative',
    'idiocy': 'negative', 'idiot': 'negative', 'idiotic': 'negative', 'idiotically': 'negative',
    'idiots': 'negative', 'idle': 'negative', 'idol': 'positive', 'idolize': 'positive',
    'idolized': 'positive', 'idyllic': 'positive', 'ignite': 'neutral', 'ignoble': 'negative',
    'ignominious': 'negative', 'ignominiously': 'negative', 'ignominy': 'negative', 'ignorance':
    'negative', 'ignorant': 'negative', 'ignore': 'negative', 'ill': 'negative', 'ill-advised':
    'negative', 'ill-conceived': 'negative', 'ill-fated': 'negative', 'ill-favored': 'negative',
    'ill-mannered': 'negative', 'ill-natured': 'negative', 'ill-sorted': 'negative',
    'ill-tempered': 'negative', 'ill-treated': 'negative', 'ill-treatment': 'negative',
    'ill-usage': 'negative', 'ill-used': 'negative', 'illegal': 'negative', 'illegally':
    'negative', 'illegitimate': 'negative', 'illicit': 'negative', 'illiquid': 'negative',
    'illiterate': 'negative', 'illness': 'negative', 'illogic': 'negative', 'illogical':
    'negative', 'illogically': 'negative', 'illuminate': 'positive', 'illuminati': 'positive',
    'illuminating': 'positive', 'illumine': 'positive', 'illusion': 'negative', 'illusions':
    'negative', 'illusory': 'negative', 'illustrious': 'positive', 'imaginary': 'negative',
    'imagination': 'neutral', 'imaginative': 'positive', 'imagine': 'neutral', 'imbalance':
    'negative', 'imbecile': 'negative', 'imbroglio': 'negative', 'immaculate': 'positive',
    'immaculately': 'positive', 'immaterial': 'negative', 'immature': 'negative', 'immediate':
    'neutral', 'immediately': 'neutral', 'immense': 'neutral', 'immensely': 'neutral', 'immensity':
    'neutral', 'immensurable': 'neutral', 'imminence': 'negative', 'imminent': 'negative',
    'imminently': 'negative', 'immobilized': 'negative', 'immoderate': 'negative', 'immoderately':
    'negative', 'immodest': 'negative', 'immoral': 'negative', 'immorality': 'negative',
    'immorally': 'negative', 'immovable': 'negative', 'immune': 'neutral', 'impair': 'negative',
    'impaired': 'negative', 'impartial': 'positive', 'impartiality': 'positive', 'impartially':
    'positive', 'impasse': 'negative', 'impassioned': 'positive', 'impassive': 'weakneg',
    'impatience': 'negative', 'impatient': 'negative', 'impatiently': 'negative', 'impeach':
    'negative', 'impeccable': 'positive', 'impeccably': 'positive', 'impedance': 'negative',
    'impede': 'negative', 'impediment': 'negative', 'impel': 'positive', 'impending': 'negative',
    'impenitent': 'negative', 'imperative': 'neutral', 'imperatively': 'neutral', 'imperfect':
    'negative', 'imperfectly': 'negative', 'imperial': 'positive', 'imperialist': 'negative',
    'imperil': 'negative', 'imperious': 'negative', 'imperiously': 'negative', 'impermissible':
    'negative', 'impersonal': 'negative', 'impertinent': 'negative', 'imperturbable': 'positive',
    'impervious': 'positive', 'impetuous': 'negative', 'impetuously': 'negative', 'impetus':
    'positive', 'impiety': 'negative', 'impinge': 'negative', 'impious': 'negative', 'implacable':
    'negative', 'implausible': 'negative', 'implausibly': 'negative', 'implicate': 'negative',
    'implication': 'negative', 'implicit': 'neutral', 'implode': 'negative', 'implore': 'both',
    'imploring': 'both', 'imploringly': 'both', 'imply': 'neutral', 'impolite': 'negative',
    'impolitely': 'negative', 'impolitic': 'negative', 'importance': 'positive', 'important':
    'positive', 'importantly': 'positive', 'importunate': 'negative', 'importune': 'negative',
    'impose': 'negative', 'imposers': 'negative', 'imposing': 'negative', 'imposition': 'negative',
    'impossible': 'negative', 'impossiblity': 'negative', 'impossibly': 'negative', 'impotent':
    'negative', 'impoverish': 'negative', 'impoverished': 'negative', 'impractical': 'negative',
    'imprecate': 'negative', 'imprecise': 'negative', 'imprecisely': 'negative', 'imprecision':
    'negative', 'impregnable': 'positive', 'impress': 'positive', 'impression': 'positive',
    'impressions': 'positive', 'impressive': 'positive', 'impressively': 'positive',
    'impressiveness': 'positive', 'imprison': 'negative', 'imprisonment': 'negative',
    'improbability': 'negative', 'improbable': 'negative', 'improbably': 'negative', 'improper':
    'negative', 'improperly': 'negative', 'impropriety': 'negative', 'improve': 'positive',
    'improved': 'positive', 'improvement': 'positive', 'improving': 'positive', 'improvise':
    'positive', 'imprudence': 'negative', 'imprudent': 'negative', 'impudence': 'negative',
    'impudent': 'negative', 'impudently': 'negative', 'impugn': 'negative', 'impulsive':
    'negative', 'impulsively': 'negative', 'impunity': 'negative', 'impure': 'negative',
    'impurity': 'negative', 'inability': 'negative', 'inaccessible': 'negative', 'inaccuracies':
    'negative', 'inaccuracy': 'negative', 'inaccurate': 'negative', 'inaccurately': 'negative',
    'inaction': 'negative', 'inactive': 'negative', 'inadequacy': 'negative', 'inadequate':
    'negative', 'inadequately': 'negative', 'inadverent': 'negative', 'inadverently': 'negative',
    'inadvisable': 'negative', 'inadvisably': 'negative', 'inalienable': 'positive', 'inane':
    'negative', 'inanely': 'negative', 'inappropriate': 'negative', 'inappropriately': 'negative',
    'inapt': 'negative', 'inaptitude': 'negative', 'inarguable': 'neutral', 'inarguably':
    'neutral', 'inarticulate': 'negative', 'inattentive': 'negative', 'incapable': 'negative',
    'incapably': 'negative', 'incautious': 'negative', 'incendiary': 'negative', 'incense':
    'negative', 'incessant': 'negative', 'incessantly': 'negative', 'incisive': 'positive',
    'incisively': 'positive', 'incisiveness': 'positive', 'incite': 'negative', 'incitement':
    'negative', 'incivility': 'negative', 'inclement': 'negative', 'inclination': 'positive',
    'inclinations': 'positive', 'inclined': 'positive', 'inclusive': 'positive', 'incognizant':
    'negative', 'incoherence': 'negative', 'incoherent': 'negative', 'incoherently': 'negative',
    'incommensurate': 'negative', 'incomparable': 'negative', 'incomparably': 'negative',
    'incompatibility': 'negative', 'incompatible': 'negative', 'incompetence': 'negative',
    'incompetent': 'negative', 'incompetently': 'negative', 'incomplete': 'negative',
    'incompliant': 'negative', 'incomprehensible': 'negative', 'incomprehension': 'negative',
    'inconceivable': 'negative', 'inconceivably': 'negative', 'inconclusive': 'negative',
    'incongruous': 'negative', 'incongruously': 'negative', 'inconsequent': 'negative',
    'inconsequential': 'negative', 'inconsequentially': 'negative', 'inconsequently': 'negative',
    'inconsiderate': 'negative', 'inconsiderately': 'negative', 'inconsistence': 'negative',
    'inconsistencies': 'negative', 'inconsistency': 'negative', 'inconsistent': 'negative',
    'inconsolable': 'negative', 'inconsolably': 'negative', 'inconstant': 'negative',
    'incontestable': 'positive', 'incontrovertible': 'positive', 'inconvenience': 'negative',
    'inconvenient': 'negative', 'inconveniently': 'negative', 'incorrect': 'negative',
    'incorrectly': 'negative', 'incorrigible': 'negative', 'incorrigibly': 'negative',
    'incorruptible': 'positive', 'increasing': 'neutral', 'increasingly': 'neutral', 'incredible':
    'positive', 'incredibly': 'positive', 'incredulous': 'negative', 'incredulously': 'negative',
    'inculcate': 'negative', 'indebted': 'positive', 'indecency': 'negative', 'indecent':
    'negative', 'indecently': 'negative', 'indecision': 'negative', 'indecisive': 'negative',
    'indecisively': 'negative', 'indecorum': 'negative', 'indeed': 'neutral', 'indefatigable':
    'positive', 'indefensible': 'negative', 'indefinite': 'negative', 'indefinitely': 'negative',
    'indelible': 'positive', 'indelibly': 'positive', 'indelicate': 'negative', 'independence':
    'positive', 'independent': 'positive', 'indescribable': 'positive', 'indescribably':
    'positive', 'indestructible': 'positive', 'indeterminable': 'negative', 'indeterminably':
    'negative', 'indeterminate': 'negative', 'indication': 'neutral', 'indicative': 'neutral',
    'indifference': 'negative', 'indifferent': 'negative', 'indigent': 'negative', 'indignant':
    'negative', 'indignantly': 'negative', 'indignation': 'negative', 'indignity': 'negative',
    'indirect': 'neutral', 'indiscernible': 'negative', 'indiscreet': 'negative', 'indiscreetly':
    'negative', 'indiscretion': 'negative', 'indiscriminate': 'negative', 'indiscriminately':
    'negative', 'indiscriminating': 'negative', 'indispensability': 'positive', 'indispensable':
    'positive', 'indisposed': 'negative', 'indisputable': 'positive', 'indistinct': 'negative',
    'indistinctive': 'negative', 'individuality': 'positive', 'indoctrinate': 'negative',
    'indoctrination': 'negative', 'indolent': 'negative', 'indomitable': 'positive', 'indomitably':
    'positive', 'indubitable': 'positive', 'indubitably': 'positive', 'indulge': 'negative',
    'indulgence': 'positive', 'indulgent': 'positive', 'industrious': 'positive', 'ineffective':
    'negative', 'ineffectively': 'negative', 'ineffectiveness': 'negative', 'ineffectual':
    'negative', 'ineffectually': 'negative', 'ineffectualness': 'negative', 'inefficacious':
    'negative', 'inefficacy': 'negative', 'inefficiency': 'negative', 'inefficient': 'negative',
    'inefficiently': 'negative', 'inelegance': 'negative', 'inelegant': 'negative', 'ineligible':
    'negative', 'ineloquent': 'negative', 'ineloquently': 'negative', 'inept': 'negative',
    'ineptitude': 'negative', 'ineptly': 'negative', 'inequalities': 'negative', 'inequality':
    'negative', 'inequitable': 'negative', 'inequitably': 'negative', 'inequities': 'negative',
    'inertia': 'negative', 'inescapable': 'negative', 'inescapably': 'negative', 'inessential':
    'negative', 'inestimable': 'positive', 'inestimably': 'positive', 'inevitable': 'negative',
    'inevitably': 'negative', 'inexact': 'negative', 'inexcusable': 'negative', 'inexcusably':
    'negative', 'inexorable': 'negative', 'inexorably': 'negative', 'inexpensive': 'positive',
    'inexperience': 'negative', 'inexperienced': 'negative', 'inexpert': 'negative', 'inexpertly':
    'negative', 'inexpiable': 'negative', 'inexplainable': 'negative', 'inexplicable': 'negative',
    'inextricable': 'negative', 'inextricably': 'negative', 'infallibility': 'positive',
    'infallible': 'positive', 'infallibly': 'positive', 'infamous': 'negative', 'infamously':
    'negative', 'infamy': 'negative', 'infatuated': 'both', 'infected': 'negative', 'infectious':
    'neutral', 'infer': 'neutral', 'inference': 'neutral', 'inferior': 'negative', 'inferiority':
    'negative', 'infernal': 'negative', 'infest': 'negative', 'infested': 'negative', 'infidel':
    'negative', 'infidels': 'negative', 'infiltrator': 'negative', 'infiltrators': 'negative',
    'infirm': 'negative', 'inflame': 'negative', 'inflammatory': 'negative', 'inflated':
    'negative', 'inflationary': 'negative', 'inflexible': 'negative', 'inflict': 'negative',
    'influence': 'neutral', 'influential': 'positive', 'informational': 'neutral', 'informative':
    'positive', 'infraction': 'negative', 'infringe': 'negative', 'infringement': 'negative',
    'infringements': 'negative', 'infuriate': 'negative', 'infuriated': 'negative', 'infuriating':
    'negative', 'infuriatingly': 'negative', 'ingenious': 'positive', 'ingeniously': 'positive',
    'ingenuity': 'positive', 'ingenuous': 'positive', 'ingenuously': 'positive', 'inglorious':
    'negative', 'ingrate': 'negative', 'ingratiate': 'positive', 'ingratiating': 'positive',
    'ingratiatingly': 'positive', 'ingratitude': 'negative', 'inherent': 'neutral', 'inhibit':
    'negative', 'inhibition': 'negative', 'inhospitable': 'negative', 'inhospitality': 'negative',
    'inhuman': 'negative', 'inhumane': 'negative', 'inhumanity': 'negative', 'inimical':
    'negative', 'inimically': 'negative', 'iniquitous': 'negative', 'iniquity': 'negative',
    'injudicious': 'negative', 'injure': 'negative', 'injurious': 'negative', 'injury': 'negative',
    'injustice': 'negative', 'injustices': 'negative', 'inkling': 'neutral', 'inklings': 'neutral',
    'innocence': 'positive', 'innocent': 'positive', 'innocently': 'positive', 'innocuous':
    'positive', 'innovation': 'positive', 'innovative': 'positive', 'innuendo': 'negative',
    'innumerable': 'neutral', 'innumerably': 'neutral', 'innumerous': 'neutral', 'inoffensive':
    'positive', 'inopportune': 'negative', 'inordinate': 'negative', 'inordinately': 'negative',
    'inquisitive': 'positive', 'insane': 'negative', 'insanely': 'negative', 'insanity':
    'negative', 'insatiable': 'negative', 'insecure': 'negative', 'insecurity': 'negative',
    'insensible': 'negative', 'insensitive': 'negative', 'insensitively': 'negative',
    'insensitivity': 'negative', 'insidious': 'negative', 'insidiously': 'negative', 'insight':
    'positive', 'insightful': 'positive', 'insightfully': 'positive', 'insights': 'neutral',
    'insignificance': 'negative', 'insignificant': 'negative', 'insignificantly': 'negative',
    'insincere': 'negative', 'insincerely': 'negative', 'insincerity': 'negative', 'insinuate':
    'negative', 'insinuating': 'negative', 'insinuation': 'negative', 'insist': 'positive',
    'insistence': 'positive', 'insistent': 'positive', 'insistently': 'positive', 'insociable':
    'negative', 'insolence': 'negative', 'insolent': 'negative', 'insolently': 'negative',
    'insolvent': 'negative', 'insouciance': 'negative', 'inspiration': 'positive', 'inspirational':
    'positive', 'inspire': 'positive', 'inspiring': 'positive', 'instability': 'negative',
    'instable': 'negative', 'instigate': 'negative', 'instigator': 'negative', 'instigators':
    'negative', 'instructive': 'positive', 'instrumental': 'positive', 'insubordinate': 'negative',
    'insubstantial': 'negative', 'insubstantially': 'negative', 'insufferable': 'negative',
    'insufferably': 'negative', 'insufficiency': 'negative', 'insufficient': 'negative',
    'insufficiently': 'negative', 'insular': 'negative', 'insult': 'negative', 'insulted':
    'negative', 'insulting': 'negative', 'insultingly': 'negative', 'insupportable': 'negative',
    'insupportably': 'negative', 'insurmountable': 'negative', 'insurmountably': 'negative',
    'insurrection': 'negative', 'intact': 'positive', 'integral': 'positive', 'integrity':
    'positive', 'intelligence': 'positive', 'intelligent': 'positive', 'intelligible': 'positive',
    'intend': 'neutral', 'intense': 'neutral', 'intensive': 'neutral', 'intensively': 'neutral',
    'intent': 'neutral', 'intention': 'neutral', 'intentions': 'neutral', 'intents': 'neutral',
    'intercede': 'positive', 'interest': 'positive', 'interested': 'positive', 'interesting':
    'positive', 'interests': 'positive', 'interfere': 'negative', 'interference': 'negative',
    'intermittent': 'negative', 'interrupt': 'negative', 'interruption': 'negative', 'intimacy':
    'positive', 'intimate': 'positive', 'intimidate': 'negative', 'intimidating': 'negative',
    'intimidatingly': 'negative', 'intimidation': 'negative', 'intolerable': 'negative',
    'intolerablely': 'negative', 'intolerance': 'negative', 'intolerant': 'negative', 'intoxicate':
    'negative', 'intractable': 'negative', 'intransigence': 'negative', 'intransigent': 'negative',
    'intricate': 'positive', 'intrigue': 'positive', 'intriguing': 'positive', 'intriguingly':
    'positive', 'intrude': 'negative', 'intrusion': 'negative', 'intrusive': 'negative',
    'intuitive': 'positive', 'inundate': 'negative', 'inundated': 'negative', 'invader':
    'negative', 'invalid': 'negative', 'invalidate': 'negative', 'invalidity': 'negative',
    'invaluable': 'positive', 'invaluablely': 'positive', 'invasive': 'negative', 'invective':
    'negative', 'inveigle': 'negative', 'inventive': 'positive', 'invidious': 'negative',
    'invidiously': 'negative', 'invidiousness': 'negative', 'invigorate': 'positive',
    'invigorating': 'positive', 'invincibility': 'positive', 'invincible': 'positive',
    'inviolable': 'positive', 'inviolate': 'positive', 'invisible': 'neutral', 'involuntarily':
    'negative', 'involuntary': 'negative', 'invulnerable': 'positive', 'irate': 'negative',
    'irately': 'negative', 'ire': 'negative', 'irk': 'negative', 'irksome': 'negative', 'ironic':
    'negative', 'ironies': 'negative', 'irony': 'negative', 'irrational': 'negative',
    'irrationality': 'negative', 'irrationally': 'negative', 'irreconcilable': 'negative',
    'irredeemable': 'negative', 'irredeemably': 'negative', 'irreformable': 'negative',
    'irrefutable': 'positive', 'irrefutably': 'positive', 'irregardless': 'neutral', 'irregular':
    'negative', 'irregularity': 'negative', 'irrelevance': 'negative', 'irrelevant': 'negative',
    'irreparable': 'negative', 'irreplacible': 'negative', 'irrepressible': 'negative',
    'irreproachable': 'positive', 'irresistible': 'positive', 'irresistibly': 'positive',
    'irresolute': 'negative', 'irresolvable': 'negative', 'irresponsible': 'negative',
    'irresponsibly': 'negative', 'irretrievable': 'negative', 'irreverence': 'negative',
    'irreverent': 'negative', 'irreverently': 'negative', 'irreversible': 'negative', 'irritable':
    'negative', 'irritably': 'negative', 'irritant': 'negative', 'irritate': 'negative',
    'irritated': 'negative', 'irritating': 'negative', 'irritation': 'negative', 'isolate':
    'negative', 'isolated': 'negative', 'isolation': 'negative', 'itch': 'negative', 'jabber':
    'negative', 'jaded': 'negative', 'jam': 'negative', 'jar': 'negative', 'jaundiced': 'negative',
    'jauntily': 'positive', 'jaunty': 'positive', 'jealous': 'negative', 'jealously': 'negative',
    'jealousness': 'negative', 'jealousy': 'negative', 'jeer': 'negative', 'jeering': 'negative',
    'jeeringly': 'negative', 'jeers': 'negative', 'jeopardize': 'negative', 'jeopardy': 'negative',
    'jerk': 'negative', 'jest': 'positive', 'jittery': 'negative', 'jobless': 'negative', 'joke':
    'positive', 'joker': 'negative', 'jollify': 'positive', 'jolly': 'positive', 'jolt':
    'negative', 'jovial': 'positive', 'joy': 'positive', 'joyful': 'positive', 'joyfully':
    'positive', 'joyless': 'positive', 'joyous': 'positive', 'joyously': 'positive', 'jubilant':
    'positive', 'jubilantly': 'positive', 'jubilate': 'positive', 'jubilation': 'positive',
    'judgement': 'neutral', 'judgements': 'neutral', 'judgment': 'neutral', 'judgments': 'neutral',
    'judicious': 'positive', 'jumpy': 'negative', 'junk': 'negative', 'junky': 'negative', 'just':
    'positive', 'justice': 'positive', 'justifiable': 'positive', 'justifiably': 'positive',
    'justification': 'positive', 'justify': 'positive', 'justly': 'positive', 'juvenile':
    'negative', 'kaput': 'negative', 'keen': 'positive', 'keenly': 'positive', 'keenness':
    'positive', 'kemp': 'positive', 'key': 'neutral', 'kick': 'negative', 'kid': 'positive',
    'kill': 'negative', 'killer': 'negative', 'killjoy': 'negative', 'kind': 'positive',
    'kindliness': 'positive', 'kindly': 'positive', 'kindness': 'positive', 'kingmaker':
    'positive', 'kiss': 'positive', 'knave': 'negative', 'knew': 'neutral', 'knife': 'negative',
    'knock': 'negative', 'know': 'neutral', 'knowing': 'neutral', 'knowingly': 'neutral',
    'knowledge': 'neutral', 'knowledgeable': 'positive', 'kook': 'negative', 'kooky': 'negative',
    'lack': 'negative', 'lackadaisical': 'negative', 'lackey': 'negative', 'lackeys': 'negative',
    'lacking': 'negative', 'lackluster': 'negative', 'laconic': 'negative', 'lag': 'negative',
    'lambast': 'negative', 'lambaste': 'negative', 'lame': 'negative', 'lame-duck': 'negative',
    'lament': 'negative', 'lamentable': 'negative', 'lamentably': 'negative', 'languid':
    'negative', 'languish': 'negative', 'languor': 'negative', 'languorous': 'negative',
    'languorously': 'negative', 'lanky': 'negative', 'lapse': 'negative', 'large': 'neutral',
    'large-scale': 'neutral', 'largely': 'neutral', 'lark': 'positive', 'lascivious': 'negative',
    'last-ditch': 'negative', 'lastly': 'neutral', 'laud': 'positive', 'laudable': 'positive',
    'laudably': 'positive', 'laugh': 'negative', 'laughable': 'negative', 'laughably': 'negative',
    'laughingstock': 'negative', 'laughter': 'negative', 'lavish': 'positive', 'lavishly':
    'positive', 'law-abiding': 'positive', 'lawbreaker': 'negative', 'lawbreaking': 'negative',
    'lawful': 'positive', 'lawfully': 'positive', 'lawless': 'negative', 'lawlessness': 'negative',
    'lax': 'negative', 'lazy': 'negative', 'leading': 'positive', 'leak': 'negative', 'leakage':
    'negative', 'leaky': 'negative', 'lean': 'positive', 'learn': 'neutral', 'learned': 'positive',
    'learning': 'positive', 'least': 'negative', 'lech': 'negative', 'lecher': 'negative',
    'lecherous': 'negative', 'lechery': 'negative', 'lecture': 'negative', 'leech': 'negative',
    'leer': 'negative', 'leery': 'negative', 'left-leaning': 'negative', 'legacies': 'neutral',
    'legacy': 'neutral', 'legalistic': 'neutral', 'legendary': 'positive', 'legitimacy':
    'positive', 'legitimate': 'positive', 'legitimately': 'positive', 'lenient': 'positive',
    'leniently': 'positive', 'less': 'negative', 'less-developed': 'negative', 'less-expensive':
    'positive', 'lessen': 'negative', 'lesser': 'negative', 'lesser-known': 'negative', 'letch':
    'negative', 'lethal': 'negative', 'lethargic': 'negative', 'lethargy': 'negative', 'leverage':
    'positive', 'levity': 'positive', 'lewd': 'negative', 'lewdly': 'negative', 'lewdness':
    'negative', 'liability': 'negative', 'liable': 'negative', 'liar': 'negative', 'liars':
    'negative', 'liberal': 'positive', 'liberalism': 'positive', 'liberally': 'positive',
    'liberate': 'positive', 'liberation': 'positive', 'liberty': 'positive', 'licentious':
    'negative', 'licentiously': 'negative', 'licentiousness': 'negative', 'lie': 'negative',
    'lier': 'negative', 'lies': 'negative', 'life-threatening': 'negative', 'lifeblood':
    'positive', 'lifeless': 'negative', 'lifelong': 'positive', 'light': 'positive',
    'light-hearted': 'positive', 'lighten': 'positive', 'likable': 'positive', 'like': 'positive',
    'likelihood': 'neutral', 'likely': 'neutral', 'likewise': 'neutral', 'liking': 'positive',
    'limit': 'negative', 'limitation': 'negative', 'limited': 'negative', 'limitless': 'neutral',
    'limp': 'negative', 'lionhearted': 'positive', 'listless': 'negative', 'literate': 'positive',
    'litigious': 'negative', 'little': 'negative', 'little-known': 'negative', 'live': 'positive',
    'lively': 'positive', 'livid': 'negative', 'lividly': 'negative', 'loath': 'negative',
    'loathe': 'negative', 'loathing': 'negative', 'loathly': 'negative', 'loathsome': 'negative',
    'loathsomely': 'negative', 'lofty': 'positive', 'logical': 'positive', 'lone': 'negative',
    'loneliness': 'negative', 'lonely': 'negative', 'lonesome': 'negative', 'long': 'negative',
    'longing': 'negative', 'longingly': 'negative', 'look': 'neutral', 'looking': 'neutral',
    'loophole': 'negative', 'loopholes': 'negative', 'loot': 'negative', 'lorn': 'negative',
    'lose': 'negative', 'loser': 'negative', 'losing': 'negative', 'loss': 'negative', 'lost':
    'negative', 'lousy': 'negative', 'lovable': 'positive', 'lovably': 'positive', 'love':
    'positive', 'loveless': 'negative', 'loveliness': 'positive', 'lovelorn': 'negative', 'lovely':
    'positive', 'lover': 'positive', 'low': 'negative', 'low-cost': 'positive', 'low-rated':
    'negative', 'low-risk': 'positive', 'lower-priced': 'positive', 'lowly': 'negative', 'loyal':
    'positive', 'loyalty': 'positive', 'lucid': 'positive', 'lucidly': 'positive', 'luck':
    'positive', 'luckier': 'positive', 'luckiest': 'positive', 'luckily': 'positive', 'luckiness':
    'positive', 'lucky': 'positive', 'lucrative': 'positive', 'ludicrous': 'negative',
    'ludicrously': 'negative', 'lugubrious': 'negative', 'lukewarm': 'negative', 'lull':
    'negative', 'luminous': 'positive', 'lunatic': 'negative', 'lunaticism': 'negative', 'lurch':
    'negative', 'lure': 'negative', 'lurid': 'negative', 'lurk': 'negative', 'lurking': 'negative',
    'lush': 'positive', 'lust': 'both', 'luster': 'positive', 'lustrous': 'positive', 'luxuriant':
    'positive', 'luxuriate': 'positive', 'luxurious': 'positive', 'luxuriously': 'positive',
    'luxury': 'positive', 'lying': 'negative', 'lyrical': 'positive', 'macabre': 'negative', 'mad':
    'negative', 'madden': 'negative', 'maddening': 'negative', 'maddeningly': 'negative', 'madder':
    'negative', 'madly': 'negative', 'madman': 'negative', 'madness': 'negative', 'magic':
    'positive', 'magical': 'positive', 'magnanimous': 'positive', 'magnanimously': 'positive',
    'magnetic': 'positive', 'magnificence': 'positive', 'magnificent': 'positive', 'magnificently':
    'positive', 'magnify': 'positive', 'majestic': 'positive', 'majesty': 'positive', 'major':
    'neutral', 'maladjusted': 'negative', 'maladjustment': 'negative', 'malady': 'negative',
    'malaise': 'negative', 'malcontent': 'negative', 'malcontented': 'negative', 'maledict':
    'negative', 'malevolence': 'negative', 'malevolent': 'negative', 'malevolently': 'negative',
    'malice': 'negative', 'malicious': 'negative', 'maliciously': 'negative', 'maliciousness':
    'negative', 'malign': 'negative', 'malignant': 'negative', 'malodorous': 'negative',
    'maltreatment': 'negative', 'manageable': 'positive', 'maneuver': 'negative', 'mangle':
    'negative', 'mania': 'negative', 'maniac': 'negative', 'maniacal': 'negative', 'manic':
    'negative', 'manifest': 'positive', 'manipulate': 'negative', 'manipulation': 'negative',
    'manipulative': 'negative', 'manipulators': 'negative', 'manly': 'positive', 'mannerly':
    'positive', 'mantra': 'neutral', 'mar': 'negative', 'marginal': 'negative', 'marginally':
    'negative', 'martyrdom': 'negative', 'martyrdom-seeking': 'negative', 'marvel': 'positive',
    'marvellous': 'positive', 'marvelous': 'positive', 'marvelously': 'positive', 'marvelousness':
    'positive', 'marvels': 'positive', 'massacre': 'negative', 'massacres': 'negative', 'massive':
    'neutral', 'master': 'positive', 'masterful': 'positive', 'masterfully': 'positive',
    'masterpiece': 'positive', 'masterpieces': 'positive', 'masters': 'positive', 'mastery':
    'positive', 'matchless': 'positive', 'matter': 'neutral', 'mature': 'positive', 'maturely':
    'positive', 'maturity': 'positive', 'maverick': 'negative', 'mawkish': 'negative', 'mawkishly':
    'negative', 'mawkishness': 'negative', 'maxi-devaluation': 'negative', 'maximize': 'positive',
    'maybe': 'neutral', 'meager': 'negative', 'mean': 'negative', 'meaningful': 'positive',
    'meaningless': 'negative', 'meanness': 'negative', 'meddle': 'negative', 'meddlesome':
    'negative', 'mediocre': 'negative', 'mediocrity': 'negative', 'meek': 'positive', 'melancholy':
    'negative', 'mellow': 'positive', 'melodramatic': 'negative', 'melodramatically': 'negative',
    'memorable': 'positive', 'memorialize': 'positive', 'memories': 'neutral', 'menace':
    'negative', 'menacing': 'negative', 'menacingly': 'negative', 'mend': 'positive', 'mendacious':
    'negative', 'mendacity': 'negative', 'menial': 'negative', 'mentality': 'neutral', 'mentor':
    'positive', 'merciful': 'positive', 'mercifully': 'positive', 'merciless': 'negative',
    'mercilessly': 'negative', 'mercy': 'positive', 'mere': 'negative', 'merely': 'negative',
    'merit': 'positive', 'meritorious': 'positive', 'merrily': 'positive', 'merriment': 'positive',
    'merriness': 'positive', 'merry': 'positive', 'mesmerize': 'positive', 'mesmerizing':
    'positive', 'mesmerizingly': 'positive', 'mess': 'negative', 'messy': 'negative',
    'metaphorize': 'neutral', 'meticulous': 'positive', 'meticulously': 'positive', 'midget':
    'negative', 'miff': 'negative', 'might': 'neutral', 'mightily': 'positive', 'mighty':
    'positive', 'mild': 'positive', 'militancy': 'negative', 'mind': 'negative', 'mindful':
    'positive', 'mindless': 'negative', 'mindlessly': 'negative', 'minister': 'positive', 'minor':
    'neutral', 'miracle': 'positive', 'miracles': 'positive', 'miraculous': 'positive',
    'miraculously': 'positive', 'miraculousness': 'positive', 'mirage': 'negative', 'mire':
    'negative', 'mirth': 'positive', 'misapprehend': 'negative', 'misbecome': 'negative',
    'misbecoming': 'negative', 'misbegotten': 'negative', 'misbehave': 'negative', 'misbehavior':
    'negative', 'miscalculate': 'negative', 'miscalculation': 'negative', 'mischief': 'negative',
    'mischievous': 'negative', 'mischievously': 'negative', 'misconception': 'negative',
    'misconceptions': 'negative', 'miscreant': 'negative', 'miscreants': 'negative',
    'misdirection': 'negative', 'miser': 'negative', 'miserable': 'negative', 'miserableness':
    'negative', 'miserably': 'negative', 'miseries': 'negative', 'miserly': 'negative', 'misery':
    'negative', 'misfit': 'negative', 'misfortune': 'negative', 'misgiving': 'negative',
    'misgivings': 'negative', 'misguidance': 'negative', 'misguide': 'negative', 'misguided':
    'negative', 'mishandle': 'negative', 'mishap': 'negative', 'misinform': 'negative',
    'misinformed': 'negative', 'misinterpret': 'negative', 'misjudge': 'negative', 'misjudgment':
    'negative', 'mislead': 'negative', 'misleading': 'negative', 'misleadingly': 'negative',
    'mislike': 'negative', 'mismanage': 'negative', 'misread': 'negative', 'misreading':
    'negative', 'misrepresent': 'negative', 'misrepresentation': 'negative', 'miss': 'negative',
    'misstatement': 'negative', 'mistake': 'negative', 'mistaken': 'negative', 'mistakenly':
    'negative', 'mistakes': 'negative', 'mistified': 'negative', 'mistrust': 'negative',
    'mistrustful': 'negative', 'mistrustfully': 'negative', 'misunderstand': 'negative',
    'misunderstanding': 'negative', 'misunderstandings': 'negative', 'misunderstood': 'negative',
    'misuse': 'negative', 'mm': 'neutral', 'moan': 'negative', 'mock': 'negative', 'mockeries':
    'negative', 'mockery': 'negative', 'mocking': 'negative', 'mockingly': 'negative', 'moderate':
    'positive', 'moderation': 'positive', 'modern': 'positive', 'modest': 'positive', 'modesty':
    'positive', 'molest': 'negative', 'molestation': 'negative', 'mollify': 'positive',
    'momentous': 'positive', 'monotonous': 'negative', 'monotony': 'negative', 'monster':
    'negative', 'monstrosities': 'negative', 'monstrosity': 'negative', 'monstrous': 'negative',
    'monstrously': 'negative', 'monumental': 'positive', 'monumentally': 'positive', 'moody':
    'negative', 'moon': 'negative', 'moot': 'negative', 'mope': 'negative', 'moral': 'positive',
    'morality': 'positive', 'moralize': 'positive', 'morbid': 'negative', 'morbidly': 'negative',
    'mordant': 'negative', 'mordantly': 'negative', 'moreover': 'neutral', 'moribund': 'negative',
    'mortification': 'negative', 'mortified': 'negative', 'mortify': 'negative', 'mortifying':
    'negative', 'most': 'neutral', 'mostly': 'neutral', 'motionless': 'negative', 'motivate':
    'positive', 'motivated': 'positive', 'motivation': 'positive', 'motive': 'neutral', 'motley':
    'negative', 'mourn': 'negative', 'mourner': 'negative', 'mournful': 'negative', 'mournfully':
    'negative', 'move': 'neutral', 'moving': 'positive', 'much': 'neutral', 'muddle': 'negative',
    'muddy': 'negative', 'mudslinger': 'negative', 'mudslinging': 'negative', 'mulish': 'negative',
    'multi-polarization': 'negative', 'mum': 'neutral', 'mundane': 'negative', 'murder':
    'negative', 'murderous': 'negative', 'murderously': 'negative', 'murky': 'negative',
    'muscle-flexing': 'negative', 'must': 'neutral', 'myriad': 'positive', 'mysterious':
    'negative', 'mysteriously': 'negative', 'mystery': 'negative', 'mystify': 'negative', 'myth':
    'negative', 'nag': 'negative', 'nagging': 'negative', 'naive': 'negative', 'naively':
    'negative', 'nap': 'neutral', 'narrow': 'negative', 'narrower': 'negative', 'nascent':
    'neutral', 'nastily': 'negative', 'nastiness': 'negative', 'nasty': 'negative', 'nationalism':
    'negative', 'natural': 'positive', 'naturally': 'positive', 'nature': 'neutral', 'naughty':
    'negative', 'nauseate': 'negative', 'nauseating': 'negative', 'nauseatingly': 'negative',
    'navigable': 'positive', 'neat': 'positive', 'neatly': 'positive', 'nebulous': 'negative',
    'nebulously': 'negative', 'necessarily': 'positive', 'necessary': 'positive', 'need':
    'negative', 'needful': 'neutral', 'needfully': 'neutral', 'needless': 'negative', 'needlessly':
    'negative', 'needs': 'neutral', 'needy': 'negative', 'nefarious': 'negative', 'nefariously':
    'negative', 'negate': 'negative', 'negation': 'negative', 'negative': 'negative', 'neglect':
    'negative', 'neglected': 'negative', 'negligence': 'negative', 'negligent': 'negative',
    'negligible': 'negative', 'nemesis': 'negative', 'nervous': 'negative', 'nervously':
    'negative', 'nervousness': 'negative', 'nettle': 'negative', 'nettlesome': 'negative',
    'neurotic': 'negative', 'neurotically': 'negative', 'neutralize': 'positive', 'nevertheless':
    'neutral', 'nice': 'positive', 'nicely': 'positive', 'nifty': 'positive', 'niggle': 'negative',
    'nightmare': 'negative', 'nightmarish': 'negative', 'nightmarishly': 'negative', 'nimble':
    'positive', 'nix': 'negative', 'noble': 'positive', 'nobly': 'positive', 'noisy': 'negative',
    'non-confidence': 'negative', 'non-violence': 'positive', 'non-violent': 'positive',
    'nonexistent': 'negative', 'nonsense': 'negative', 'nonviolent': 'neutral', 'normal':
    'positive', 'nosey': 'negative', 'notable': 'positive', 'notably': 'positive', 'noteworthy':
    'positive', 'noticeable': 'positive', 'notion': 'neutral', 'notorious': 'negative',
    'notoriously': 'negative', 'nourish': 'positive', 'nourishing': 'positive', 'nourishment':
    'positive', 'novel': 'positive', 'nuance': 'neutral', 'nuances': 'neutral', 'nuisance':
    'negative', 'numb': 'negative', 'nurture': 'positive', 'nurturing': 'positive', 'oasis':
    'positive', 'obedience': 'positive', 'obedient': 'positive', 'obediently': 'positive', 'obese':
    'negative', 'obey': 'positive', 'object': 'negative', 'objection': 'negative', 'objectionable':
    'negative', 'objections': 'negative', 'objective': 'positive', 'objectively': 'positive',
    'obligation': 'neutral', 'obliged': 'positive', 'oblique': 'negative', 'obliterate':
    'negative', 'obliterated': 'negative', 'oblivious': 'negative', 'obnoxious': 'negative',
    'obnoxiously': 'negative', 'obscene': 'negative', 'obscenely': 'negative', 'obscenity':
    'negative', 'obscure': 'negative', 'obscurity': 'negative', 'obsess': 'negative', 'obsession':
    'negative', 'obsessions': 'negative', 'obsessive': 'negative', 'obsessively': 'negative',
    'obsessiveness': 'negative', 'obsolete': 'negative', 'obstacle': 'negative', 'obstinate':
    'negative', 'obstinately': 'negative', 'obstruct': 'negative', 'obstruction': 'negative',
    'obtrusive': 'negative', 'obtuse': 'negative', 'obviate': 'positive', 'obvious': 'neutral',
    'obviously': 'negative', 'odd': 'negative', 'odder': 'negative', 'oddest': 'negative',
    'oddities': 'negative', 'oddity': 'negative', 'oddly': 'negative', 'offbeat': 'positive',
    'offence': 'negative', 'offend': 'negative', 'offending': 'negative', 'offenses': 'negative',
    'offensive': 'negative', 'offensively': 'negative', 'offensiveness': 'negative', 'officious':
    'negative', 'offset': 'positive', 'oh': 'neutral', 'okay': 'positive', 'olympic': 'neutral',
    'ominous': 'negative', 'ominously': 'negative', 'omission': 'negative', 'omit': 'negative',
    'one-side': 'negative', 'one-sided': 'negative', 'onerous': 'negative', 'onerously':
    'negative', 'onslaught': 'negative', 'onward': 'positive', 'open': 'positive', 'open-ended':
    'neutral', 'openly': 'positive', 'openness': 'positive', 'opinion': 'neutral', 'opinionated':
    'negative', 'opinions': 'neutral', 'opponent': 'negative', 'opportune': 'positive',
    'opportunistic': 'negative', 'opportunity': 'positive', 'oppose': 'negative', 'opposition':
    'negative', 'oppositions': 'negative', 'oppress': 'negative', 'oppression': 'negative',
    'oppressive': 'negative', 'oppressively': 'negative', 'oppressiveness': 'negative',
    'oppressors': 'negative', 'optimal': 'positive', 'optimism': 'positive', 'optimistic':
    'positive', 'opulent': 'positive', 'ordeal': 'negative', 'orderly': 'positive', 'original':
    'positive', 'originality': 'positive', 'orphan': 'negative', 'orthodoxy': 'neutral',
    'ostracize': 'negative', 'ought': 'neutral', 'outbreak': 'negative', 'outburst': 'negative',
    'outbursts': 'negative', 'outcast': 'negative', 'outcry': 'negative', 'outdated': 'negative',
    'outdo': 'positive', 'outgoing': 'positive', 'outlaw': 'negative', 'outlook': 'neutral',
    'outmoded': 'negative', 'outrage': 'negative', 'outraged': 'negative', 'outrageous':
    'negative', 'outrageously': 'negative', 'outrageousness': 'negative', 'outrages': 'negative',
    'outright': 'neutral', 'outshine': 'positive', 'outsider': 'negative', 'outsmart': 'positive',
    'outspoken': 'neutral', 'outstanding': 'positive', 'outstandingly': 'positive', 'outstrip':
    'positive', 'outwit': 'positive', 'ovation': 'positive', 'over-acted': 'negative',
    'over-valuation': 'negative', 'overachiever': 'positive', 'overact': 'negative', 'overacted':
    'negative', 'overawe': 'negative', 'overbalance': 'negative', 'overbalanced': 'negative',
    'overbearing': 'negative', 'overbearingly': 'negative', 'overblown': 'negative', 'overcome':
    'negative', 'overdo': 'negative', 'overdone': 'negative', 'overdue': 'negative',
    'overemphasize': 'negative', 'overjoyed': 'positive', 'overkill': 'negative', 'overlook':
    'negative', 'overplay': 'negative', 'overpower': 'negative', 'overreach': 'negative',
    'overrun': 'negative', 'overshadow': 'negative', 'oversight': 'negative', 'oversimplification':
    'negative', 'oversimplified': 'negative', 'oversimplify': 'negative', 'oversized': 'negative',
    'overstate': 'negative', 'overstatement': 'negative', 'overstatements': 'negative', 'overt':
    'neutral', 'overtaxed': 'negative', 'overthrow': 'negative', 'overture': 'positive',
    'overtures': 'neutral', 'overturn': 'negative', 'overwhelm': 'negative', 'overwhelming':
    'negative', 'overwhelmingly': 'negative', 'overworked': 'negative', 'overzealous': 'negative',
    'overzealously': 'negative', 'pacifist': 'positive', 'pacifists': 'positive', 'pacify':
    'neutral', 'pain': 'negative', 'painful': 'negative', 'painfully': 'negative', 'painless':
    'positive', 'painlessly': 'positive', 'pains': 'negative', 'painstaking': 'positive',
    'painstakingly': 'positive', 'palatable': 'positive', 'palatial': 'positive', 'pale':
    'negative', 'palliate': 'positive', 'paltry': 'negative', 'pamper': 'positive', 'pan':
    'negative', 'pandemonium': 'negative', 'panic': 'negative', 'panicky': 'negative', 'paradise':
    'positive', 'paradoxical': 'negative', 'paradoxically': 'negative', 'paralize': 'negative',
    'paralyzed': 'negative', 'paramount': 'positive', 'paranoia': 'negative', 'paranoid':
    'negative', 'parasite': 'negative', 'pardon': 'positive', 'pariah': 'negative', 'parody':
    'negative', 'partiality': 'negative', 'particular': 'neutral', 'particularly': 'neutral',
    'partisan': 'negative', 'partisans': 'negative', 'passe': 'negative', 'passion': 'positive',
    'passionate': 'positive', 'passionately': 'positive', 'passive': 'negative', 'passiveness':
    'negative', 'pathetic': 'negative', 'pathetically': 'negative', 'patience': 'positive',
    'patient': 'positive', 'patiently': 'positive', 'patriot': 'positive', 'patriotic': 'positive',
    'patronize': 'negative', 'paucity': 'negative', 'pauper': 'negative', 'paupers': 'negative',
    'payback': 'negative', 'peace': 'positive', 'peaceable': 'positive', 'peaceful': 'positive',
    'peacefully': 'positive', 'peacekeepers': 'positive', 'peculiar': 'negative', 'peculiarly':
    'negative', 'pedantic': 'negative', 'pedestrian': 'negative', 'peerless': 'positive', 'peeve':
    'negative', 'peeved': 'negative', 'peevish': 'negative', 'peevishly': 'negative', 'penalize':
    'negative', 'penalty': 'negative', 'penetrating': 'positive', 'penitent': 'positive',
    'perceptions': 'neutral', 'perceptive': 'positive', 'perfect': 'positive', 'perfection':
    'positive', 'perfectly': 'positive', 'perfidious': 'negative', 'perfidity': 'negative',
    'perfunctory': 'negative', 'perhaps': 'neutral', 'peril': 'negative', 'perilous': 'negative',
    'perilously': 'negative', 'peripheral': 'negative', 'perish': 'negative', 'permissible':
    'positive', 'pernicious': 'negative', 'perplex': 'negative', 'perplexed': 'negative',
    'perplexing': 'negative', 'perplexity': 'negative', 'persecute': 'negative', 'persecution':
    'negative', 'perseverance': 'positive', 'persevere': 'positive', 'persistence': 'neutral',
    'persistent': 'positive', 'personages': 'positive', 'personality': 'positive', 'perspective':
    'neutral', 'perspicuous': 'positive', 'perspicuously': 'positive', 'persuade': 'positive',
    'persuasive': 'positive', 'persuasively': 'positive', 'pertinacious': 'negative',
    'pertinaciously': 'negative', 'pertinacity': 'negative', 'pertinent': 'positive', 'perturb':
    'negative', 'perturbed': 'negative', 'pervasive': 'negative', 'perverse': 'negative',
    'perversely': 'negative', 'perversion': 'negative', 'perversity': 'negative', 'pervert':
    'negative', 'perverted': 'negative', 'pessimism': 'negative', 'pessimistic': 'negative',
    'pessimistically': 'negative', 'pest': 'negative', 'pestilent': 'negative', 'petrified':
    'negative', 'petrify': 'negative', 'pettifog': 'negative', 'petty': 'negative', 'phenomenal':
    'positive', 'phenomenally': 'positive', 'philosophize': 'neutral', 'phobia': 'negative',
    'phobic': 'negative', 'phony': 'negative', 'picky': 'negative', 'picturesque': 'positive',
    'piety': 'positive', 'pillage': 'negative', 'pillar': 'positive', 'pillory': 'negative',
    'pinch': 'negative', 'pine': 'negative', 'pinnacle': 'positive', 'pious': 'positive', 'pique':
    'negative', 'pithy': 'positive', 'pitiable': 'negative', 'pitiful': 'negative', 'pitifully':
    'negative', 'pitiless': 'negative', 'pitilessly': 'negative', 'pittance': 'negative', 'pity':
    'negative', 'pivotal': 'neutral', 'placate': 'positive', 'placid': 'positive', 'plagiarize':
    'negative', 'plague': 'negative', 'plain': 'positive', 'plainly': 'positive', 'plausibility':
    'positive', 'plausible': 'positive', 'player': 'neutral', 'playful': 'positive', 'playfully':
    'positive', 'plaything': 'negative', 'plea': 'negative', 'plead': 'both', 'pleading': 'both',
    'pleadingly': 'both', 'pleas': 'negative', 'pleasant': 'positive', 'pleasantly': 'positive',
    'please': 'positive', 'pleased': 'positive', 'pleasing': 'positive', 'pleasingly': 'positive',
    'pleasurable': 'positive', 'pleasurably': 'positive', 'pleasure': 'positive', 'plebeian':
    'negative', 'pledge': 'positive', 'pledges': 'positive', 'plenary': 'neutral', 'plentiful':
    'positive', 'plenty': 'positive', 'plight': 'negative', 'plot': 'negative', 'plotters':
    'negative', 'ploy': 'negative', 'plunder': 'negative', 'plunderer': 'negative', 'plush':
    'positive', 'poetic': 'positive', 'poeticize': 'positive', 'poignant': 'positive', 'point':
    'neutral', 'pointless': 'negative', 'pointlessly': 'negative', 'poise': 'positive', 'poised':
    'positive', 'poison': 'negative', 'poisonous': 'negative', 'poisonously': 'negative',
    'polarisation': 'negative', 'polemize': 'negative', 'polished': 'positive', 'polite':
    'positive', 'politeness': 'positive', 'pollute': 'negative', 'polluter': 'negative',
    'polluters': 'negative', 'polution': 'negative', 'pompous': 'negative', 'ponder': 'neutral',
    'poor': 'negative', 'poorly': 'negative', 'popular': 'positive', 'popularity': 'positive',
    'portable': 'positive', 'posh': 'positive', 'position': 'neutral', 'positive': 'positive',
    'positively': 'positive', 'positiveness': 'positive', 'possibility': 'neutral', 'possible':
    'neutral', 'possibly': 'neutral', 'posterity': 'positive', 'posture': 'neutral', 'posturing':
    'negative', 'potent': 'positive', 'potential': 'positive', 'pout': 'negative', 'poverty':
    'negative', 'power': 'neutral', 'powerful': 'positive', 'powerfully': 'positive', 'powerless':
    'negative', 'practicable': 'positive', 'practical': 'positive', 'practically': 'neutral',
    'pragmatic': 'positive', 'praise': 'positive', 'praiseworthy': 'positive', 'praising':
    'positive', 'prate': 'negative', 'pratfall': 'negative', 'prattle': 'negative', 'pray':
    'neutral', 'pre-eminent': 'positive', 'preach': 'positive', 'preaching': 'positive',
    'precarious': 'negative', 'precariously': 'negative', 'precaution': 'positive', 'precautions':
    'positive', 'precedent': 'positive', 'precious': 'positive', 'precipitate': 'negative',
    'precipitous': 'negative', 'precise': 'positive', 'precisely': 'positive', 'precision':
    'positive', 'predatory': 'negative', 'predicament': 'negative', 'predictable': 'neutral',
    'predictablely': 'neutral', 'predominant': 'neutral', 'preeminent': 'positive', 'preemptive':
    'positive', 'prefer': 'positive', 'preferable': 'positive', 'preferably': 'positive',
    'preference': 'positive', 'preferences': 'positive', 'prejudge': 'negative', 'prejudice':
    'negative', 'prejudicial': 'negative', 'premeditated': 'negative', 'premier': 'positive',
    'premium': 'positive', 'preoccupy': 'negative', 'prepared': 'positive', 'preponderance':
    'positive', 'preposterous': 'negative', 'preposterously': 'negative', 'press': 'positive',
    'pressing': 'negative', 'pressure': 'neutral', 'pressures': 'neutral', 'prestige': 'positive',
    'prestigious': 'positive', 'presumably': 'neutral', 'presume': 'negative', 'presumptuous':
    'negative', 'presumptuously': 'negative', 'pretence': 'negative', 'pretend': 'negative',
    'pretense': 'negative', 'pretentious': 'negative', 'pretentiously': 'negative', 'prettily':
    'positive', 'pretty': 'positive', 'prevalent': 'neutral', 'prevaricate': 'negative',
    'priceless': 'positive', 'pricey': 'negative', 'prickle': 'negative', 'prickles': 'negative',
    'pride': 'positive', 'prideful': 'negative', 'primarily': 'neutral', 'primary': 'neutral',
    'prime': 'neutral', 'primitive': 'negative', 'principle': 'positive', 'principled': 'positive',
    'prison': 'negative', 'prisoner': 'negative', 'privilege': 'positive', 'privileged':
    'positive', 'prize': 'positive', 'pro': 'positive', 'pro-American': 'positive', 'pro-Beijing':
    'positive', 'pro-Cuba': 'positive', 'pro-peace': 'positive', 'proactive': 'positive',
    'problem': 'negative', 'problematic': 'negative', 'problems': 'negative', 'proclaim':
    'neutral', 'procrastinate': 'negative', 'procrastination': 'negative', 'prodigious':
    'positive', 'prodigiously': 'positive', 'prodigy': 'positive', 'productive': 'positive',
    'profane': 'negative', 'profanity': 'negative', 'profess': 'positive', 'proficient':
    'positive', 'proficiently': 'positive', 'profit': 'positive', 'profitable': 'positive',
    'profound': 'positive', 'profoundly': 'positive', 'profuse': 'positive', 'profusely':
    'positive', 'profusion': 'positive', 'prognosticate': 'neutral', 'progress': 'positive',
    'progressive': 'positive', 'prohibit': 'negative', 'prohibitive': 'negative', 'prohibitively':
    'negative', 'prolific': 'positive', 'prominence': 'positive', 'prominent': 'positive',
    'promise': 'positive', 'promising': 'positive', 'promoter': 'positive', 'prompt': 'positive',
    'promptly': 'positive', 'propaganda': 'negative', 'propagandize': 'negative', 'proper':
    'positive', 'properly': 'positive', 'prophesy': 'neutral', 'propitious': 'positive',
    'propitiously': 'positive', 'proportionate': 'neutral', 'proportionately': 'neutral',
    'proscription': 'negative', 'proscriptions': 'negative', 'prosecute': 'negative', 'prospect':
    'positive', 'prospects': 'positive', 'prosper': 'positive', 'prosperity': 'positive',
    'prosperous': 'positive', 'protect': 'positive', 'protection': 'positive', 'protective':
    'positive', 'protector': 'positive', 'protest': 'negative', 'protests': 'negative',
    'protracted': 'negative', 'proud': 'positive', 'prove': 'neutral', 'providence': 'positive',
    'provocation': 'negative', 'provocative': 'negative', 'provoke': 'negative', 'prowess':
    'positive', 'prudence': 'positive', 'prudent': 'positive', 'prudently': 'positive', 'pry':
    'negative', 'pugnacious': 'negative', 'pugnaciously': 'negative', 'pugnacity': 'negative',
    'punch': 'negative', 'punctual': 'positive', 'pundits': 'positive', 'punish': 'negative',
    'punishable': 'negative', 'punitive': 'negative', 'puny': 'negative', 'puppet': 'negative',
    'puppets': 'negative', 'pure': 'positive', 'purification': 'positive', 'purify': 'positive',
    'purity': 'positive', 'purposeful': 'positive', 'puzzle': 'negative', 'puzzled': 'negative',
    'puzzlement': 'negative', 'puzzling': 'negative', 'quack': 'negative', 'quaint': 'positive',
    'qualified': 'positive', 'qualify': 'positive', 'qualms': 'negative', 'quandary': 'negative',
    'quarrel': 'negative', 'quarrellous': 'negative', 'quarrellously': 'negative', 'quarrels':
    'negative', 'quarrelsome': 'negative', 'quash': 'negative', 'quasi-ally': 'positive', 'queer':
    'negative', 'quench': 'positive', 'questionable': 'negative', 'quibble': 'negative', 'quick':
    'neutral', 'quicken': 'positive', 'quiet': 'neutral', 'quit': 'negative', 'quite': 'neutral',
    'quitter': 'negative', 'racism': 'negative', 'racist': 'negative', 'racists': 'negative',
    'rack': 'negative', 'radiance': 'positive', 'radiant': 'positive', 'radical': 'negative',
    'radicalization': 'negative', 'radically': 'negative', 'radicals': 'negative', 'rage':
    'negative', 'ragged': 'negative', 'raging': 'negative', 'rail': 'negative', 'rally':
    'positive', 'rampage': 'negative', 'rampant': 'negative', 'ramshackle': 'negative', 'rancor':
    'negative', 'rank': 'negative', 'rankle': 'negative', 'rant': 'negative', 'ranting':
    'negative', 'rantingly': 'negative', 'rapid': 'neutral', 'rapport': 'positive',
    'rapprochement': 'positive', 'rapt': 'positive', 'rapture': 'positive', 'raptureous':
    'positive', 'raptureously': 'positive', 'rapturous': 'positive', 'rapturously': 'positive',
    'rare': 'neutral', 'rarely': 'neutral', 'rascal': 'negative', 'rash': 'negative', 'rat':
    'negative', 'rather': 'neutral', 'rational': 'positive', 'rationality': 'positive',
    'rationalize': 'negative', 'rattle': 'negative', 'ravage': 'negative', 'rave': 'positive',
    'raving': 'negative', 're-conquest': 'positive', 'react': 'neutral', 'reaction': 'neutral',
    'reactionary': 'negative', 'reactions': 'neutral', 'readily': 'positive', 'readiness':
    'neutral', 'ready': 'positive', 'reaffirm': 'positive', 'reaffirmation': 'positive', 'real':
    'positive', 'realist': 'positive', 'realistic': 'positive', 'realistically': 'positive',
    'realization': 'neutral', 'really': 'neutral', 'reason': 'positive', 'reasonable': 'positive',
    'reasonably': 'positive', 'reasoned': 'positive', 'reassurance': 'positive', 'reassure':
    'positive', 'rebellious': 'negative', 'rebuff': 'negative', 'rebuke': 'negative',
    'recalcitrant': 'negative', 'recant': 'negative', 'receptive': 'positive', 'recession':
    'negative', 'recessionary': 'negative', 'reckless': 'negative', 'recklessly': 'negative',
    'recklessness': 'negative', 'reclaim': 'positive', 'recognition': 'positive', 'recognizable':
    'neutral', 'recoil': 'negative', 'recommend': 'positive', 'recommendation': 'positive',
    'recommendations': 'positive', 'recommended': 'positive', 'recompense': 'positive',
    'reconcile': 'positive', 'reconciliation': 'positive', 'record-setting': 'positive',
    'recourses': 'negative', 'recover': 'positive', 'rectification': 'positive', 'rectify':
    'positive', 'rectifying': 'positive', 'redeem': 'positive', 'redeeming': 'positive',
    'redemption': 'positive', 'redundancy': 'negative', 'redundant': 'negative', 'reestablish':
    'positive', 'refine': 'positive', 'refined': 'positive', 'refinement': 'positive',
    'reflecting': 'neutral', 'reflective': 'neutral', 'reform': 'positive', 'refresh': 'positive',
    'refreshing': 'positive', 'refuge': 'positive', 'refusal': 'negative', 'refuse': 'negative',
    'refutation': 'negative', 'refute': 'negative', 'regal': 'positive', 'regally': 'positive',
    'regard': 'positive', 'regardless': 'neutral', 'regardlessly': 'neutral', 'regress':
    'negative', 'regression': 'negative', 'regressive': 'negative', 'regret': 'negative',
    'regretful': 'negative', 'regretfully': 'negative', 'regrettable': 'negative', 'regrettably':
    'negative', 'rehabilitate': 'positive', 'rehabilitation': 'positive', 'reinforce': 'positive',
    'reinforcement': 'positive', 'reiterate': 'neutral', 'reiterated': 'neutral', 'reiterates':
    'neutral', 'reject': 'negative', 'rejection': 'negative', 'rejoice': 'positive', 'rejoicing':
    'positive', 'rejoicingly': 'positive', 'relapse': 'negative', 'relations': 'neutral', 'relax':
    'positive', 'relaxed': 'positive', 'relent': 'positive', 'relentless': 'negative',
    'relentlessly': 'negative', 'relentlessness': 'negative', 'relevance': 'positive', 'relevant':
    'positive', 'reliability': 'positive', 'reliable': 'positive', 'reliably': 'positive',
    'relief': 'positive', 'relieve': 'positive', 'relish': 'positive', 'reluctance': 'negative',
    'reluctant': 'negative', 'reluctantly': 'negative', 'remark': 'neutral', 'remarkable':
    'positive', 'remarkably': 'positive', 'remedy': 'positive', 'reminiscent': 'positive',
    'remorse': 'negative', 'remorseful': 'negative', 'remorsefully': 'negative', 'remorseless':
    'negative', 'remorselessly': 'negative', 'remorselessness': 'negative', 'remunerate':
    'positive', 'renaissance': 'positive', 'renewable': 'neutral', 'renewal': 'positive',
    'renounce': 'negative', 'renovate': 'positive', 'renovation': 'positive', 'renown': 'positive',
    'renowned': 'positive', 'renunciation': 'negative', 'repair': 'positive', 'reparation':
    'positive', 'repay': 'positive', 'repel': 'negative', 'repent': 'positive', 'repentance':
    'positive', 'repetitive': 'negative', 'replete': 'neutral', 'reprehensible': 'negative',
    'reprehensibly': 'negative', 'reprehension': 'negative', 'reprehensive': 'negative', 'repress':
    'negative', 'repression': 'negative', 'repressive': 'negative', 'reprimand': 'negative',
    'reproach': 'negative', 'reproachful': 'negative', 'reprove': 'negative', 'reprovingly':
    'negative', 'repudiate': 'negative', 'repudiation': 'negative', 'repugn': 'negative',
    'repugnance': 'negative', 'repugnant': 'negative', 'repugnantly': 'negative', 'repulse':
    'negative', 'repulsed': 'negative', 'repulsing': 'negative', 'repulsive': 'negative',
    'repulsively': 'negative', 'repulsiveness': 'negative', 'reputable': 'positive', 'reputed':
    'neutral', 'rescue': 'positive', 'resent': 'negative', 'resentful': 'negative', 'resentment':
    'negative', 'reservations': 'negative', 'resignation': 'negative', 'resigned': 'negative',
    'resilient': 'positive', 'resistance': 'negative', 'resistant': 'negative', 'resolute':
    'positive', 'resolve': 'positive', 'resolved': 'positive', 'resound': 'positive', 'resounding':
    'positive', 'resourceful': 'positive', 'resourcefulness': 'positive', 'respect': 'positive',
    'respectable': 'positive', 'respectful': 'positive', 'respectfully': 'positive', 'respite':
    'positive', 'resplendent': 'positive', 'responsibility': 'positive', 'responsible': 'positive',
    'responsibly': 'positive', 'responsive': 'positive', 'restful': 'positive', 'restless':
    'negative', 'restlessness': 'negative', 'restoration': 'positive', 'restore': 'positive',
    'restraint': 'positive', 'restrict': 'negative', 'restricted': 'negative', 'restriction':
    'negative', 'restrictive': 'negative', 'resurgent': 'positive', 'retaliate': 'negative',
    'retaliatory': 'negative', 'retard': 'negative', 'reticent': 'negative', 'retire': 'negative',
    'retract': 'negative', 'retreat': 'negative', 'reunite': 'positive', 'reveal': 'neutral',
    'revealing': 'neutral', 'revel': 'positive', 'revelation': 'positive', 'revelatory': 'neutral',
    'revenge': 'negative', 'revengeful': 'negative', 'revengefully': 'negative', 'revere':
    'positive', 'reverence': 'positive', 'reverent': 'positive', 'reverently': 'positive',
    'revert': 'negative', 'revile': 'negative', 'reviled': 'negative', 'revitalize': 'positive',
    'revival': 'positive', 'revive': 'positive', 'revoke': 'negative', 'revolt': 'negative',
    'revolting': 'negative', 'revoltingly': 'negative', 'revolution': 'positive', 'revulsion':
    'negative', 'revulsive': 'negative', 'reward': 'positive', 'rewarding': 'positive',
    'rewardingly': 'positive', 'rhapsodize': 'negative', 'rhetoric': 'negative', 'rhetorical':
    'negative', 'rich': 'positive', 'riches': 'positive', 'richly': 'positive', 'richness':
    'positive', 'rid': 'negative', 'ridicule': 'negative', 'ridiculous': 'negative',
    'ridiculously': 'negative', 'rife': 'negative', 'rift': 'negative', 'rifts': 'negative',
    'right': 'positive', 'righten': 'positive', 'righteous': 'positive', 'righteously': 'positive',
    'righteousness': 'positive', 'rightful': 'positive', 'rightfully': 'positive', 'rightly':
    'positive', 'rightness': 'positive', 'rights': 'positive', 'rigid': 'negative', 'rigor':
    'negative', 'rigorous': 'negative', 'rile': 'negative', 'riled': 'negative', 'ripe':
    'positive', 'risk': 'negative', 'risk-free': 'positive', 'risky': 'negative', 'rival':
    'negative', 'rivalry': 'negative', 'roadblocks': 'negative', 'robust': 'positive', 'rocky':
    'negative', 'rogue': 'negative', 'rollercoaster': 'negative', 'romantic': 'positive',
    'romantically': 'positive', 'romanticize': 'positive', 'rosy': 'positive', 'rot': 'negative',
    'rotten': 'negative', 'rough': 'negative', 'rousing': 'positive', 'rubbish': 'negative',
    'rude': 'negative', 'rue': 'negative', 'ruffian': 'negative', 'ruffle': 'negative', 'ruin':
    'negative', 'ruinous': 'negative', 'rumbling': 'negative', 'rumor': 'negative', 'rumors':
    'negative', 'rumours': 'negative', 'rumple': 'negative', 'run-down': 'negative', 'runaway':
    'negative', 'rupture': 'negative', 'rusty': 'negative', 'ruthless': 'negative', 'ruthlessly':
    'negative', 'ruthlessness': 'negative', 'sabotage': 'negative', 'sacred': 'positive',
    'sacrifice': 'negative', 'sad': 'negative', 'sadden': 'negative', 'sadly': 'negative',
    'sadness': 'negative', 'safe': 'positive', 'safeguard': 'positive', 'sag': 'negative',
    'sagacity': 'positive', 'sage': 'positive', 'sagely': 'positive', 'saint': 'positive',
    'saintliness': 'positive', 'saintly': 'positive', 'salable': 'positive', 'salacious':
    'negative', 'salivate': 'positive', 'salutary': 'positive', 'salute': 'positive', 'salvation':
    'positive', 'sanctify': 'positive', 'sanctimonious': 'negative', 'sanction': 'positive',
    'sanctity': 'positive', 'sanctuary': 'positive', 'sane': 'positive', 'sanguine': 'positive',
    'sanity': 'positive', 'sap': 'negative', 'sarcasm': 'negative', 'sarcastic': 'negative',
    'sarcastically': 'negative', 'sardonic': 'negative', 'sardonically': 'negative', 'sass':
    'negative', 'satirical': 'negative', 'satirize': 'negative', 'satisfaction': 'positive',
    'satisfactorily': 'positive', 'satisfactory': 'positive', 'satisfy': 'positive', 'satisfying':
    'positive', 'savage': 'negative', 'savaged': 'negative', 'savagely': 'negative', 'savagery':
    'negative', 'savages': 'negative', 'savor': 'positive', 'savvy': 'positive', 'scandal':
    'negative', 'scandalize': 'negative', 'scandalized': 'negative', 'scandalous': 'negative',
    'scandalously': 'negative', 'scandals': 'negative', 'scant': 'negative', 'scapegoat':
    'negative', 'scar': 'negative', 'scarce': 'negative', 'scarcely': 'negative', 'scarcity':
    'negative', 'scare': 'negative', 'scared': 'negative', 'scarier': 'negative', 'scariest':
    'negative', 'scarily': 'negative', 'scarred': 'negative', 'scars': 'negative', 'scary':
    'negative', 'scathing': 'negative', 'scathingly': 'negative', 'scenic': 'positive', 'scheme':
    'negative', 'scheming': 'negative', 'scholarly': 'neutral', 'scoff': 'negative', 'scoffingly':
    'negative', 'scold': 'negative', 'scolding': 'negative', 'scoldingly': 'negative', 'scorching':
    'negative', 'scorchingly': 'negative', 'scorn': 'negative', 'scornful': 'negative',
    'scornfully': 'negative', 'scoundrel': 'negative', 'scourge': 'negative', 'scowl': 'negative',
    'scream': 'negative', 'screaming': 'neutral', 'screamingly': 'neutral', 'screech': 'negative',
    'screw': 'negative', 'scruples': 'positive', 'scrupulous': 'positive', 'scrupulously':
    'positive', 'scrutinize': 'neutral', 'scrutiny': 'neutral', 'scum': 'negative', 'scummy':
    'negative', 'seamless': 'positive', 'seasoned': 'positive', 'second-class': 'negative',
    'second-tier': 'negative', 'secretive': 'negative', 'secure': 'positive', 'securely':
    'positive', 'security': 'positive', 'sedentary': 'negative', 'seductive': 'positive', 'seedy':
    'negative', 'seem': 'neutral', 'seemingly': 'neutral', 'seethe': 'negative', 'seething':
    'negative', 'selective': 'positive', 'self-coup': 'negative', 'self-criticism': 'negative',
    'self-defeating': 'negative', 'self-destructive': 'negative', 'self-determination': 'positive',
    'self-examination': 'neutral', 'self-humiliation': 'negative', 'self-interest': 'negative',
    'self-interested': 'negative', 'self-respect': 'positive', 'self-satisfaction': 'positive',
    'self-serving': 'negative', 'self-sufficiency': 'positive', 'self-sufficient': 'positive',
    'selfinterested': 'negative', 'selfish': 'negative', 'selfishly': 'negative', 'selfishness':
    'negative', 'semblance': 'positive', 'senile': 'negative', 'sensation': 'positive',
    'sensational': 'positive', 'sensationalize': 'negative', 'sensationally': 'positive',
    'sensations': 'positive', 'sense': 'positive', 'senseless': 'negative', 'senselessly':
    'negative', 'sensible': 'positive', 'sensibly': 'positive', 'sensitive': 'positive',
    'sensitively': 'positive', 'sensitivity': 'positive', 'sentiment': 'positive',
    'sentimentality': 'positive', 'sentimentally': 'positive', 'sentiments': 'positive', 'serene':
    'positive', 'serenity': 'positive', 'serious': 'negative', 'seriously': 'negative',
    'seriousness': 'negative', 'sermonize': 'negative', 'servitude': 'negative', 'set-up':
    'negative', 'settle': 'positive', 'sever': 'negative', 'severe': 'negative', 'severely':
    'negative', 'severity': 'negative', 'sexy': 'positive', 'shabby': 'negative', 'shadow':
    'negative', 'shadowy': 'negative', 'shady': 'negative', 'shake': 'negative', 'shaky':
    'negative', 'shallow': 'negative', 'sham': 'negative', 'shambles': 'negative', 'shame':
    'negative', 'shameful': 'negative', 'shamefully': 'negative', 'shamefulness': 'negative',
    'shameless': 'negative', 'shamelessly': 'negative', 'shamelessness': 'negative', 'shark':
    'negative', 'sharp': 'negative', 'sharply': 'negative', 'shatter': 'negative', 'sheer':
    'negative', 'shelter': 'positive', 'shield': 'positive', 'shimmer': 'positive', 'shimmering':
    'positive', 'shimmeringly': 'positive', 'shine': 'positive', 'shiny': 'positive', 'shipwreck':
    'negative', 'shirk': 'negative', 'shirker': 'negative', 'shiver': 'negative', 'shock':
    'negative', 'shocking': 'negative', 'shockingly': 'negative', 'shoddy': 'negative',
    'short-lived': 'negative', 'shortage': 'negative', 'shortchange': 'negative', 'shortcoming':
    'negative', 'shortcomings': 'negative', 'shortsighted': 'negative', 'shortsightedness':
    'negative', 'should': 'neutral', 'show': 'neutral', 'showdown': 'negative', 'shred':
    'negative', 'shrew': 'negative', 'shrewd': 'positive', 'shrewdly': 'positive', 'shrewdness':
    'positive', 'shriek': 'negative', 'shrill': 'negative', 'shrilly': 'negative', 'shrivel':
    'negative', 'shroud': 'negative', 'shrouded': 'negative', 'shrug': 'negative', 'shun':
    'negative', 'shunned': 'negative', 'shy': 'negative', 'shyly': 'negative', 'shyness':
    'negative', 'sick': 'negative', 'sicken': 'negative', 'sickening': 'negative', 'sickeningly':
    'negative', 'sickly': 'negative', 'sickness': 'negative', 'sidetrack': 'negative',
    'sidetracked': 'negative', 'siege': 'negative', 'signals': 'neutral', 'significance':
    'positive', 'significant': 'positive', 'signify': 'positive', 'sillily': 'negative', 'silly':
    'negative', 'simmer': 'negative', 'simple': 'positive', 'simplicity': 'positive', 'simplified':
    'positive', 'simplify': 'positive', 'simplistic': 'negative', 'simplistically': 'negative',
    'simply': 'neutral', 'sin': 'negative', 'sincere': 'positive', 'sincerely': 'positive',
    'sincerity': 'positive', 'sinful': 'negative', 'sinfully': 'negative', 'sinister': 'negative',
    'sinisterly': 'negative', 'sinking': 'negative', 'skeletons': 'negative', 'skeptical':
    'negative', 'skeptically': 'negative', 'skepticism': 'negative', 'sketchy': 'negative',
    'skill': 'positive', 'skilled': 'positive', 'skillful': 'positive', 'skillfully': 'positive',
    'skimpy': 'negative', 'skittish': 'negative', 'skittishly': 'negative', 'skulk': 'negative',
    'skyrocketing': 'negative', 'slack': 'negative', 'slander': 'negative', 'slanderer':
    'negative', 'slanderous': 'negative', 'slanderously': 'negative', 'slanders': 'negative',
    'slap': 'negative', 'slashing': 'negative', 'slaughter': 'negative', 'slaughtered': 'negative',
    'slaves': 'negative', 'sleazy': 'negative', 'sleek': 'positive', 'sleepy': 'neutral',
    'slender': 'positive', 'slight': 'negative', 'slightly': 'negative', 'slim': 'positive',
    'slime': 'negative', 'sloppily': 'negative', 'sloppy': 'negative', 'sloth': 'negative',
    'slothful': 'negative', 'slow': 'negative', 'slow-moving': 'negative', 'slowly': 'negative',
    'slug': 'negative', 'sluggish': 'negative', 'slump': 'negative', 'slur': 'negative', 'sly':
    'negative', 'smack': 'negative', 'smart': 'positive', 'smarter': 'positive', 'smartest':
    'positive', 'smartly': 'positive', 'smash': 'negative', 'smear': 'negative', 'smelling':
    'negative', 'smile': 'positive', 'smiling': 'positive', 'smilingly': 'positive', 'smitten':
    'positive', 'smokescreen': 'negative', 'smolder': 'negative', 'smoldering': 'negative',
    'smooth': 'positive', 'smother': 'negative', 'smoulder': 'negative', 'smouldering': 'negative',
    'smug': 'negative', 'smugly': 'negative', 'smut': 'negative', 'smuttier': 'negative',
    'smuttiest': 'negative', 'smutty': 'negative', 'snare': 'negative', 'snarl': 'negative',
    'snatch': 'negative', 'sneak': 'negative', 'sneakily': 'negative', 'sneaky': 'negative',
    'sneer': 'negative', 'sneering': 'negative', 'sneeringly': 'negative', 'snub': 'negative',
    'so': 'neutral', 'so-cal': 'negative', 'so-called': 'negative', 'sob': 'negative', 'sober':
    'negative', 'sobering': 'negative', 'sociable': 'positive', 'soft-spoken': 'positive',
    'soften': 'positive', 'solace': 'positive', 'solemn': 'negative', 'solicitous': 'positive',
    'solicitously': 'positive', 'solicitude': 'positive', 'solid': 'positive', 'solidarity':
    'positive', 'soliloquize': 'neutral', 'somber': 'negative', 'soothe': 'positive', 'soothingly':
    'positive', 'sophisticated': 'positive', 'sore': 'negative', 'sorely': 'negative', 'soreness':
    'negative', 'sorrow': 'negative', 'sorrowful': 'negative', 'sorrowfully': 'negative', 'sorry':
    'negative', 'sound': 'positive', 'sounding': 'negative', 'soundness': 'positive', 'sour':
    'negative', 'sourly': 'negative', 'sovereignty': 'neutral', 'spacious': 'positive', 'spade':
    'negative', 'spank': 'negative', 'spare': 'positive', 'sparing': 'positive', 'sparingly':
    'positive', 'sparkle': 'positive', 'sparkling': 'positive', 'special': 'positive', 'specific':
    'neutral', 'specifically': 'neutral', 'spectacular': 'positive', 'spectacularly': 'positive',
    'speculate': 'neutral', 'speculation': 'neutral', 'speedy': 'positive', 'spellbind':
    'positive', 'spellbinding': 'positive', 'spellbindingly': 'positive', 'spellbound': 'positive',
    'spilling': 'negative', 'spinster': 'negative', 'spirit': 'positive', 'spirited': 'positive',
    'spiritless': 'negative', 'spiritual': 'positive', 'spite': 'negative', 'spiteful': 'negative',
    'spitefully': 'negative', 'spitefulness': 'negative', 'splayed-finger': 'neutral', 'splendid':
    'positive', 'splendidly': 'positive', 'splendor': 'positive', 'split': 'negative', 'splitting':
    'negative', 'spoil': 'negative', 'spook': 'negative', 'spookier': 'negative', 'spookiest':
    'negative', 'spookily': 'negative', 'spooky': 'negative', 'spoon-fed': 'negative',
    'spoon-feed': 'negative', 'spoonfed': 'negative', 'sporadic': 'negative', 'spot': 'negative',
    'spotless': 'positive', 'spotty': 'negative', 'sprightly': 'positive', 'spur': 'positive',
    'spurious': 'negative', 'spurn': 'negative', 'sputter': 'negative', 'squabble': 'negative',
    'squabbling': 'negative', 'squander': 'negative', 'squarely': 'positive', 'squash': 'negative',
    'squirm': 'negative', 'stab': 'negative', 'stability': 'positive', 'stabilize': 'positive',
    'stable': 'positive', 'stagger': 'negative', 'staggering': 'negative', 'staggeringly':
    'negative', 'stagnant': 'negative', 'stagnate': 'negative', 'stagnation': 'negative', 'staid':
    'negative', 'stain': 'negative', 'stainless': 'positive', 'stake': 'negative', 'stale':
    'negative', 'stalemate': 'negative', 'stammer': 'negative', 'stampede': 'negative', 'stance':
    'neutral', 'stances': 'neutral', 'stand': 'positive', 'stands': 'neutral', 'standstill':
    'negative', 'star': 'positive', 'stark': 'negative', 'starkly': 'negative', 'stars':
    'positive', 'startle': 'negative', 'startling': 'negative', 'startlingly': 'negative',
    'starvation': 'negative', 'starve': 'negative', 'stately': 'positive', 'statements': 'neutral',
    'static': 'negative', 'statuesque': 'positive', 'staunch': 'positive', 'staunchly': 'positive',
    'staunchness': 'positive', 'steadfast': 'positive', 'steadfastly': 'positive', 'steadfastness':
    'positive', 'steadiness': 'positive', 'steady': 'positive', 'steal': 'negative', 'stealing':
    'negative', 'steep': 'negative', 'steeply': 'negative', 'stellar': 'positive', 'stellarly':
    'positive', 'stench': 'negative', 'stereotype': 'negative', 'stereotypical': 'negative',
    'stereotypically': 'negative', 'stern': 'negative', 'stew': 'negative', 'sticky': 'negative',
    'stiff': 'negative', 'stifle': 'negative', 'stifling': 'negative', 'stiflingly': 'negative',
    'stigma': 'negative', 'stigmatize': 'negative', 'still': 'neutral', 'stimulate': 'positive',
    'stimulating': 'positive', 'stimulative': 'positive', 'sting': 'negative', 'stinging':
    'negative', 'stingingly': 'negative', 'stink': 'negative', 'stinking': 'negative', 'stir':
    'neutral', 'stirring': 'positive', 'stirringly': 'positive', 'stodgy': 'negative', 'stole':
    'negative', 'stolen': 'negative', 'stood': 'positive', 'stooge': 'negative', 'stooges':
    'negative', 'storm': 'negative', 'stormy': 'negative', 'straggle': 'negative', 'straggler':
    'negative', 'straight': 'positive', 'straightforward': 'positive', 'strain': 'negative',
    'strained': 'negative', 'strange': 'negative', 'strangely': 'negative', 'stranger': 'negative',
    'strangest': 'negative', 'strangle': 'negative', 'streamlined': 'positive', 'strength':
    'neutral', 'strenuous': 'negative', 'stress': 'negative', 'stressful': 'negative',
    'stressfully': 'negative', 'stricken': 'negative', 'strict': 'negative', 'strictly':
    'negative', 'stride': 'positive', 'strident': 'negative', 'stridently': 'negative', 'strides':
    'positive', 'strife': 'negative', 'strike': 'negative', 'striking': 'positive', 'strikingly':
    'positive', 'stringent': 'negative', 'stringently': 'negative mpqapolarity=strongneg',
    'striving': 'positive', 'strong': 'positive', 'stronger-than-expected': 'neutral', 'struck':
    'negative', 'struggle': 'negative', 'strut': 'negative', 'stubborn': 'negative', 'stubbornly':
    'negative', 'stubbornness': 'negative', 'studious': 'positive', 'studiously': 'positive',
    'stuffed': 'neutral', 'stuffy': 'negative', 'stumble': 'negative', 'stump': 'negative', 'stun':
    'negative', 'stunned': 'positive', 'stunning': 'positive', 'stunningly': 'positive', 'stunt':
    'negative', 'stunted': 'negative', 'stupefy': 'neutral', 'stupendous': 'positive',
    'stupendously': 'positive', 'stupid': 'negative', 'stupidity': 'negative', 'stupidly':
    'negative', 'stupified': 'negative', 'stupify': 'negative', 'stupor': 'negative', 'sturdy':
    'positive', 'sty': 'negative', 'stylish': 'positive', 'stylishly': 'positive', 'suave':
    'positive', 'subdued': 'negative', 'subjected': 'negative', 'subjection': 'negative',
    'subjugate': 'negative', 'subjugation': 'negative', 'sublime': 'positive', 'submissive':
    'negative', 'subordinate': 'negative', 'subscribe': 'positive', 'subservience': 'negative',
    'subservient': 'negative', 'subside': 'negative', 'substandard': 'negative', 'substantial':
    'positive', 'substantially': 'positive', 'substantive': 'positive', 'subtle': 'positive',
    'subtract': 'negative', 'subversion': 'negative', 'subversive': 'negative', 'subversively':
    'negative', 'subvert': 'negative', 'succeed': 'positive', 'success': 'positive', 'successful':
    'positive', 'successfully': 'positive', 'succumb': 'negative', 'such': 'neutral', 'sucker':
    'negative', 'suffer': 'negative', 'sufferer': 'negative', 'sufferers': 'negative', 'suffering':
    'negative', 'suffice': 'positive', 'sufficient': 'positive', 'sufficiently': 'positive',
    'suffocate': 'negative', 'sugar-coat': 'negative', 'sugar-coated': 'negative', 'sugarcoated':
    'negative', 'suggest': 'positive', 'suggestions': 'positive', 'suicidal': 'negative',
    'suicide': 'negative', 'suit': 'positive', 'suitable': 'positive', 'sulk': 'negative',
    'sullen': 'negative', 'sully': 'negative', 'sumptuous': 'positive', 'sumptuously': 'positive',
    'sumptuousness': 'positive', 'sunder': 'negative', 'sunny': 'positive', 'super': 'positive',
    'superb': 'positive', 'superbly': 'positive', 'superficial': 'negative', 'superficiality':
    'negative', 'superficially': 'negative', 'superfluous': 'negative', 'superior': 'positive',
    'superiority': 'negative', 'superlative': 'positive', 'superstition': 'negative',
    'superstitious': 'negative', 'support': 'positive', 'supporter': 'positive', 'supportive':
    'positive', 'suppose': 'neutral', 'supposed': 'negative', 'supposing': 'neutral', 'suppress':
    'negative', 'suppression': 'negative', 'supremacy': 'negative', 'supreme': 'positive',
    'supremely': 'positive', 'supurb': 'positive', 'supurbly': 'positive', 'sure': 'positive',
    'surely': 'positive', 'surge': 'positive', 'surging': 'positive', 'surmise': 'positive',
    'surmount': 'positive', 'surpass': 'positive', 'surprise': 'neutral', 'surprising': 'neutral',
    'surprisingly': 'neutral', 'surrender': 'negative', 'survival': 'positive', 'survive':
    'positive', 'survivor': 'positive', 'susceptible': 'negative', 'suspect': 'negative',
    'suspicion': 'negative', 'suspicions': 'negative', 'suspicious': 'negative', 'suspiciously':
    'negative', 'sustainability': 'positive', 'sustainable': 'positive', 'sustained': 'positive',
    'swagger': 'negative', 'swamped': 'negative', 'swear': 'negative', 'sweeping': 'positive',
    'sweet': 'positive', 'sweeten': 'positive', 'sweetheart': 'positive', 'sweetly': 'positive',
    'sweetness': 'positive', 'swift': 'positive', 'swiftness': 'positive', 'swindle': 'negative',
    'swing': 'neutral', 'swipe': 'negative', 'swoon': 'negative', 'swore': 'negative', 'sworn':
    'positive', 'sympathetic': 'negative', 'sympathetically': 'negative', 'sympathies': 'negative',
    'sympathize': 'negative', 'sympathy': 'negative', 'symptom': 'negative', 'syndrome':
    'negative', 'systematic': 'neutral', 'taboo': 'negative', 'tact': 'positive', 'taint':
    'negative', 'tainted': 'negative', 'tale': 'neutral', 'talent': 'positive', 'talented':
    'positive', 'tall': 'neutral', 'tamper': 'negative', 'tangled': 'negative', 'tantalize':
    'positive', 'tantalizing': 'positive', 'tantalizingly': 'positive', 'tantamount': 'neutral',
    'tantrum': 'negative', 'tardy': 'negative', 'tarnish': 'negative', 'taste': 'positive',
    'tattered': 'negative', 'taunt': 'negative', 'taunting': 'negative', 'tauntingly': 'negative',
    'taunts': 'negative', 'tawdry': 'negative', 'taxing': 'negative', 'tease': 'negative',
    'teasingly': 'negative', 'tedious': 'negative', 'tediously': 'negative', 'temerity':
    'negative', 'temper': 'negative', 'temperance': 'positive', 'temperate': 'positive', 'tempest':
    'negative', 'tempt': 'positive', 'temptation': 'negative', 'tempting': 'positive',
    'temptingly': 'positive', 'tenacious': 'positive', 'tenaciously': 'positive', 'tenacity':
    'positive', 'tendency': 'neutral', 'tender': 'positive', 'tenderly': 'positive', 'tenderness':
    'positive', 'tense': 'negative', 'tension': 'negative', 'tentative': 'negative', 'tentatively':
    'negative', 'tenuous': 'negative', 'tenuously': 'negative', 'tepid': 'negative', 'terrible':
    'negative', 'terribleness': 'negative', 'terribly': 'negative', 'terrific': 'positive',
    'terrifically': 'positive', 'terrified': 'positive', 'terrify': 'positive', 'terrifying':
    'positive', 'terrifyingly': 'positive', 'terror': 'negative', 'terror-genic': 'negative',
    'terrorism': 'negative', 'terrorize': 'negative', 'thank': 'positive', 'thankful': 'positive',
    'thankfully': 'positive', 'thankless': 'negative', 'theoretize': 'neutral', 'therefore':
    'neutral', 'think': 'neutral', 'thinkable': 'positive', 'thinking': 'neutral', 'thirst':
    'negative', 'thorny': 'negative', 'thorough': 'positive', 'though': 'neutral', 'thought':
    'neutral', 'thoughtful': 'positive', 'thoughtfully': 'positive', 'thoughtfulness': 'positive',
    'thoughtless': 'negative', 'thoughtlessly': 'negative', 'thoughtlessness': 'negative',
    'thrash': 'negative', 'threat': 'negative', 'threaten': 'negative', 'threatening': 'negative',
    'threats': 'negative', 'thrift': 'positive', 'thrifty': 'positive', 'thrill': 'positive',
    'thrilling': 'positive', 'thrillingly': 'positive', 'thrills': 'positive', 'thrive':
    'positive', 'thriving': 'positive', 'throttle': 'negative', 'throw': 'negative', 'thumb':
    'negative', 'thumbs': 'negative', 'thus': 'neutral', 'thusly': 'neutral', 'thwart': 'negative',
    'tickle': 'positive', 'tidy': 'positive', 'time-honored': 'positive', 'timely': 'positive',
    'timid': 'negative', 'timidity': 'negative', 'timidly': 'negative', 'timidness': 'negative',
    'tingle': 'positive', 'tint': 'neutral', 'tiny': 'negative', 'tire': 'negative', 'tired':
    'negative', 'tiresome': 'negative', 'tiring': 'negative', 'tiringly': 'negative', 'titillate':
    'positive', 'titillating': 'positive', 'titillatingly': 'positive', 'toast': 'positive',
    'togetherness': 'positive', 'toil': 'negative', 'tolerable': 'positive', 'tolerably':
    'positive', 'tolerance': 'positive', 'tolerant': 'positive', 'tolerantly': 'positive',
    'tolerate': 'positive', 'toleration': 'positive', 'toll': 'negative', 'too': 'negative', 'top':
    'positive', 'topple': 'negative', 'torment': 'negative', 'tormented': 'negative', 'torrent':
    'negative', 'torrid': 'positive', 'torridly': 'positive', 'tortuous': 'negative', 'torture':
    'negative', 'tortured': 'negative', 'torturous': 'negative', 'torturously': 'negative',
    'totalitarian': 'negative', 'touch': 'neutral', 'touches': 'neutral', 'touchy': 'negative',
    'toughness': 'negative', 'toxic': 'negative', 'tradition': 'positive', 'traditional':
    'positive', 'traduce': 'negative', 'tragedy': 'negative', 'tragic': 'negative', 'tragically':
    'negative', 'traitor': 'negative', 'traitorous': 'negative', 'traitorously': 'negative',
    'tramp': 'negative', 'trample': 'negative', 'tranquil': 'positive', 'tranquility': 'positive',
    'transgress': 'negative', 'transgression': 'negative', 'transparency': 'neutral',
    'transparent': 'neutral', 'transport': 'neutral', 'trauma': 'negative', 'traumatic':
    'negative', 'traumatically': 'negative', 'traumatize': 'negative', 'traumatized': 'negative',
    'travesties': 'negative', 'travesty': 'negative', 'treacherous': 'negative', 'treacherously':
    'negative', 'treachery': 'negative', 'treason': 'negative', 'treasonous': 'negative',
    'treasure': 'positive', 'treat': 'positive', 'tremendous': 'positive', 'tremendously':
    'positive', 'trendy': 'positive', 'trepidation': 'positive', 'trial': 'negative', 'tribute':
    'positive', 'trick': 'negative', 'trickery': 'negative', 'tricky': 'negative', 'trim':
    'positive', 'triumph': 'positive', 'triumphal': 'positive', 'triumphant': 'positive',
    'triumphantly': 'positive', 'trivial': 'negative', 'trivialize': 'negative', 'trivially':
    'negative', 'trouble': 'negative', 'troublemaker': 'negative', 'troublesome': 'negative',
    'troublesomely': 'negative', 'troubling': 'negative', 'troublingly': 'negative', 'truant':
    'negative', 'truculent': 'positive', 'truculently': 'positive', 'true': 'positive', 'truly':
    'positive', 'trump': 'positive', 'trumpet': 'positive', 'trust': 'positive', 'trusting':
    'positive', 'trustingly': 'positive', 'trustworthiness': 'positive', 'trustworthy': 'positive',
    'truth': 'positive', 'truthful': 'positive', 'truthfully': 'positive', 'truthfulness':
    'positive', 'try': 'negative', 'trying': 'negative', 'tumultuous': 'negative', 'turbulent':
    'negative', 'turmoil': 'negative', 'twinkly': 'positive', 'twist': 'negative', 'twisted':
    'negative', 'twists': 'negative', 'tyrannical': 'negative', 'tyrannically': 'negative',
    'tyranny': 'negative', 'tyrant': 'negative', 'ugh': 'negative', 'ugliness': 'negative', 'ugly':
    'negative', 'ulterior': 'negative', 'ultimate': 'positive', 'ultimately': 'positive',
    'ultimatum': 'negative', 'ultimatums': 'negative', 'ultra': 'positive', 'ultra-hardline':
    'negative', 'unabashed': 'positive', 'unabashedly': 'positive', 'unable': 'negative',
    'unacceptable': 'negative', 'unacceptablely': 'negative', 'unaccustomed': 'negative',
    'unanimous': 'positive', 'unassailable': 'positive', 'unattractive': 'negative', 'unaudited':
    'neutral', 'unauthentic': 'negative', 'unavailable': 'negative', 'unavoidable': 'negative',
    'unavoidably': 'negative', 'unbearable': 'negative', 'unbearablely': 'negative',
    'unbelievable': 'negative', 'unbelievably': 'negative', 'unbiased': 'positive', 'unbosom':
    'positive', 'unbound': 'positive', 'unbroken': 'positive', 'uncertain': 'negative', 'uncivil':
    'negative', 'uncivilized': 'negative', 'unclean': 'negative', 'unclear': 'negative',
    'uncollectible': 'negative', 'uncomfortable': 'negative', 'uncommon': 'positive', 'uncommonly':
    'positive', 'uncompetitive': 'negative', 'uncompromising': 'negative', 'uncompromisingly':
    'negative', 'unconcerned': 'positive', 'unconditional': 'positive', 'unconfirmed': 'negative',
    'unconstitutional': 'negative', 'uncontrolled': 'negative', 'unconventional': 'positive',
    'unconvincing': 'negative', 'unconvincingly': 'negative', 'uncouth': 'negative', 'undaunted':
    'positive', 'undecided': 'negative', 'undefined': 'negative', 'undependability': 'negative',
    'undependable': 'negative', 'underdog': 'negative', 'underestimate': 'negative', 'underlings':
    'negative', 'undermine': 'negative', 'underpaid': 'negative', 'understand': 'positive',
    'understandable': 'positive', 'understanding': 'positive', 'understate': 'positive',
    'understated': 'positive', 'understatedly': 'positive', 'understood': 'positive',
    'undesirable': 'negative', 'undetermined': 'negative', 'undid': 'negative', 'undignified':
    'negative', 'undisputable': 'positive', 'undisputably': 'positive', 'undisputed': 'positive',
    'undo': 'negative', 'undocumented': 'negative', 'undone': 'negative', 'undoubted': 'positive',
    'undoubtedly': 'positive', 'undue': 'negative', 'unease': 'negative', 'uneasily': 'negative',
    'uneasiness': 'negative', 'uneasy': 'negative', 'uneconomical': 'negative', 'unencumbered':
    'positive', 'unequal': 'negative', 'unequivocal': 'positive', 'unequivocally': 'positive',
    'unethical': 'negative', 'uneven': 'negative', 'uneventful': 'negative', 'unexpected':
    'negative', 'unexpectedly': 'negative', 'unexplained': 'negative', 'unfair': 'negative',
    'unfairly': 'negative', 'unfaithful': 'negative', 'unfaithfully': 'negative', 'unfamiliar':
    'negative', 'unfavorable': 'negative', 'unfazed': 'positive', 'unfeeling': 'negative',
    'unfettered': 'positive', 'unfinished': 'negative', 'unfit': 'negative', 'unforeseen':
    'negative', 'unforgettable': 'positive', 'unfortunate': 'negative', 'unfortunately':
    'negative', 'unfounded': 'negative', 'unfriendly': 'negative', 'unfulfilled': 'negative',
    'unfunded': 'negative', 'ungovernable': 'negative', 'ungrateful': 'negative', 'unhappily':
    'negative', 'unhappiness': 'negative', 'unhappy': 'negative', 'unhealthy': 'negative',
    'uniform': 'positive', 'uniformly': 'positive', 'unilateralism': 'negative', 'unimaginable':
    'negative', 'unimaginably': 'negative', 'unimportant': 'negative', 'uninformed': 'negative',
    'uninsured': 'negative', 'unipolar': 'negative', 'unique': 'positive', 'unity': 'positive',
    'universal': 'positive', 'unjust': 'negative', 'unjustifiable': 'negative', 'unjustifiably':
    'negative', 'unjustified': 'negative', 'unjustly': 'negative', 'unkind': 'negative',
    'unkindly': 'negative', 'unlamentable': 'negative', 'unlamentably': 'negative', 'unlawful':
    'negative', 'unlawfully': 'negative', 'unlawfulness': 'negative', 'unleash': 'negative',
    'unlicensed': 'negative', 'unlikely': 'negative', 'unlimited': 'positive', 'unlucky':
    'negative', 'unmoved': 'negative', 'unnatural': 'negative', 'unnaturally': 'negative',
    'unnecessary': 'negative', 'unneeded': 'negative', 'unnerve': 'negative', 'unnerved':
    'negative', 'unnerving': 'negative', 'unnervingly': 'negative', 'unnoticed': 'negative',
    'unobserved': 'negative', 'unorthodox': 'negative', 'unorthodoxy': 'negative', 'unparalleled':
    'positive', 'unpleasant': 'negative', 'unpleasantries': 'negative', 'unpopular': 'negative',
    'unprecedent': 'negative', 'unprecedented': 'negative', 'unpredictable': 'negative',
    'unprepared': 'negative', 'unpretentious': 'positive', 'unproductive': 'negative',
    'unprofitable': 'negative', 'unqualified': 'negative', 'unquestionable': 'positive',
    'unquestionably': 'positive', 'unravel': 'negative', 'unraveled': 'negative', 'unrealistic':
    'negative', 'unreasonable': 'negative', 'unreasonably': 'negative', 'unrelenting': 'negative',
    'unrelentingly': 'negative', 'unreliability': 'negative', 'unreliable': 'negative',
    'unresolved': 'negative', 'unrest': 'negative', 'unrestricted': 'positive', 'unruly':
    'negative', 'unsafe': 'negative', 'unsatisfactory': 'negative', 'unsavory': 'negative',
    'unscathed': 'positive', 'unscrupulous': 'negative', 'unscrupulously': 'negative', 'unseemly':
    'negative', 'unselfish': 'positive', 'unsettle': 'negative', 'unsettled': 'negative',
    'unsettling': 'negative', 'unsettlingly': 'negative', 'unskilled': 'negative',
    'unsophisticated': 'negative', 'unsound': 'negative', 'unspeakable': 'negative',
    'unspeakablely': 'negative', 'unspecified': 'negative', 'unstable': 'negative', 'unsteadily':
    'negative', 'unsteadiness': 'negative', 'unsteady': 'negative', 'unsuccessful': 'negative',
    'unsuccessfully': 'negative', 'unsupported': 'negative', 'unsure': 'negative', 'unsuspecting':
    'negative', 'unsustainable': 'negative', 'untenable': 'negative', 'untested': 'negative',
    'unthinkable': 'negative', 'unthinkably': 'negative', 'untimely': 'negative', 'untouched':
    'positive', 'untrained': 'positive', 'untrue': 'negative', 'untrustworthy': 'negative',
    'untruthful': 'negative', 'unusual': 'negative', 'unusually': 'negative', 'unwanted':
    'negative', 'unwarranted': 'negative', 'unwelcome': 'negative', 'unwieldy': 'negative',
    'unwilling': 'negative', 'unwillingly': 'negative', 'unwillingness': 'negative', 'unwise':
    'negative', 'unwisely': 'negative', 'unworkable': 'negative', 'unworthy': 'negative',
    'unyielding': 'negative', 'upbeat': 'positive', 'upbraid': 'negative', 'upfront': 'positive',
    'upgrade': 'positive', 'upheaval': 'negative', 'upheld': 'positive', 'uphold': 'positive',
    'uplift': 'positive', 'uplifting': 'positive', 'upliftingly': 'positive', 'upliftment':
    'positive', 'upright': 'positive', 'uprising': 'negative', 'uproar': 'negative', 'uproarious':
    'negative', 'uproariously': 'negative', 'uproarous': 'negative', 'uproarously': 'negative',
    'uproot': 'negative', 'upscale': 'positive', 'upset': 'negative', 'upsetting': 'negative',
    'upsettingly': 'negative', 'upside': 'positive', 'upward': 'positive', 'urge': 'positive',
    'urgency': 'negative', 'urgent': 'negative', 'urgently': 'negative', 'usable': 'positive',
    'useful': 'positive', 'usefulness': 'positive', 'useless': 'negative', 'usurp': 'negative',
    'usurper': 'negative', 'utilitarian': 'positive', 'utmost': 'positive', 'utter': 'negative',
    'utterances': 'neutral', 'utterly': 'negative', 'uttermost': 'positive', 'vagrant': 'negative',
    'vague': 'negative', 'vagueness': 'negative', 'vain': 'negative', 'vainly': 'negative',
    'valiant': 'positive', 'valiantly': 'positive', 'valid': 'positive', 'validity': 'positive',
    'valor': 'positive', 'valuable': 'positive', 'value': 'positive', 'values': 'positive',
    'vanish': 'negative', 'vanity': 'negative', 'vanquish': 'positive', 'vast': 'positive',
    'vastly': 'positive', 'vastness': 'positive', 'vehement': 'negative', 'vehemently': 'negative',
    'venerable': 'positive', 'venerably': 'positive', 'venerate': 'positive', 'vengeance':
    'negative', 'vengeful': 'negative', 'vengefully': 'negative', 'vengefulness': 'negative',
    'venom': 'negative', 'venomous': 'negative', 'venomously': 'negative', 'vent': 'negative',
    'verifiable': 'positive', 'veritable': 'positive', 'versatile': 'positive', 'versatility':
    'positive', 'very': 'neutral', 'vestiges': 'negative', 'veto': 'negative', 'vex': 'negative',
    'vexation': 'negative', 'vexing': 'negative', 'vexingly': 'negative', 'viability': 'positive',
    'viable': 'positive', 'vibrant': 'positive', 'vibrantly': 'positive', 'vice': 'negative',
    'vicious': 'negative', 'viciously': 'negative', 'viciousness': 'negative', 'victimize':
    'negative', 'victorious': 'positive', 'victory': 'positive', 'vie': 'negative', 'view':
    'neutral', 'viewpoints': 'neutral', 'views': 'neutral', 'vigilance': 'positive', 'vigilant':
    'positive', 'vigorous': 'positive', 'vigorously': 'positive', 'vile': 'negative', 'vileness':
    'negative', 'vilify': 'negative', 'villainous': 'negative', 'villainously': 'negative',
    'villains': 'negative', 'villian': 'negative', 'villianous': 'negative', 'villianously':
    'negative', 'villify': 'negative', 'vindicate': 'positive', 'vindictive': 'negative',
    'vindictively': 'negative', 'vindictiveness': 'negative', 'vintage': 'positive', 'violate':
    'negative', 'violation': 'negative', 'violator': 'negative', 'violent': 'negative',
    'violently': 'negative', 'viper': 'negative', 'virtue': 'positive', 'virtuous': 'positive',
    'virtuously': 'positive', 'virulence': 'negative', 'virulent': 'negative', 'virulently':
    'negative', 'virus': 'negative', 'visionary': 'positive', 'vital': 'positive', 'vitality':
    'positive', 'vivacious': 'positive', 'vivid': 'positive', 'vocal': 'neutral', 'vocally':
    'negative', 'vociferous': 'negative', 'vociferously': 'negative', 'void': 'negative',
    'volatile': 'negative', 'volatility': 'negative', 'voluntarily': 'positive', 'voluntary':
    'positive', 'vomit': 'negative', 'vouch': 'positive', 'vouchsafe': 'positive', 'vow':
    'positive', 'vulgar': 'negative', 'vulnerable': 'positive', 'wail': 'negative', 'wallow':
    'negative', 'wane': 'negative', 'waning': 'negative', 'want': 'positive', 'wanton': 'negative',
    'war': 'negative', 'war-like': 'negative', 'warfare': 'negative', 'warily': 'negative',
    'wariness': 'negative', 'warlike': 'negative', 'warm': 'positive', 'warmhearted': 'positive',
    'warmly': 'positive', 'warmth': 'positive', 'warning': 'negative', 'warp': 'negative',
    'warped': 'negative', 'wary': 'negative', 'waste': 'negative', 'wasteful': 'negative',
    'wastefulness': 'negative', 'watchdog': 'negative', 'wayward': 'negative', 'weak': 'negative',
    'weaken': 'negative', 'weakening': 'negative', 'weakness': 'negative', 'weaknesses':
    'negative', 'wealthy': 'positive', 'weariness': 'negative', 'wearisome': 'negative', 'weary':
    'negative', 'wedge': 'negative', 'wee': 'negative', 'weed': 'negative', 'weep': 'negative',
    'weird': 'negative', 'weirdly': 'negative', 'welcome': 'positive', 'welfare': 'positive',
    'well': 'positive', 'well-being': 'positive', 'well-connected': 'positive', 'well-educated':
    'positive', 'well-established': 'positive', 'well-informed': 'positive', 'well-intentioned':
    'positive', 'well-managed': 'positive', 'well-positioned': 'positive', 'well-publicized':
    'positive', 'well-received': 'positive', 'well-regarded': 'positive', 'well-run': 'positive',
    'well-wishers': 'positive', 'wellbeing': 'positive', 'whatever': 'negative', 'wheedle':
    'negative', 'whiff': 'neutral', 'whimper': 'negative', 'whimsical': 'positive', 'whine':
    'negative', 'whips': 'negative', 'white': 'positive', 'wholeheartedly': 'positive',
    'wholesome': 'positive', 'wicked': 'negative', 'wickedly': 'negative', 'wickedness':
    'negative', 'wide': 'positive', 'wide-open': 'positive', 'wide-ranging': 'positive',
    'widespread': 'negative', 'wild': 'negative', 'wildly': 'negative', 'wiles': 'negative',
    'will': 'positive', 'willful': 'positive', 'willfully': 'positive', 'willing': 'positive',
    'willingness': 'positive', 'wilt': 'negative', 'wily': 'negative', 'wince': 'negative', 'wink':
    'positive', 'winnable': 'positive', 'winners': 'positive', 'wisdom': 'positive', 'wise':
    'positive', 'wisely': 'positive', 'wish': 'positive', 'wishes': 'positive', 'wishing':
    'positive', 'withheld': 'negative', 'withhold': 'negative', 'witty': 'positive', 'woe':
    'negative', 'woebegone': 'negative', 'woeful': 'negative', 'woefully': 'negative', 'wonder':
    'positive', 'wonderful': 'positive', 'wonderfully': 'positive', 'wonderous': 'positive',
    'wonderously': 'positive', 'wondrous': 'positive', 'woo': 'positive', 'workable': 'positive',
    'world-famous': 'positive', 'worn': 'negative', 'worried': 'negative', 'worriedly': 'negative',
    'worrier': 'negative', 'worries': 'negative', 'worrisome': 'negative', 'worry': 'negative',
    'worrying': 'negative', 'worryingly': 'negative', 'worse': 'negative', 'worsen': 'negative',
    'worsening': 'negative', 'worship': 'positive', 'worst': 'negative', 'worth': 'positive',
    'worth-while': 'positive', 'worthiness': 'positive', 'worthless': 'negative', 'worthlessly':
    'negative', 'worthlessness': 'negative', 'worthwhile': 'positive', 'worthy': 'positive',
    'would': 'neutral', 'wound': 'negative', 'wounds': 'negative', 'wow': 'positive', 'wrangle':
    'negative', 'wrath': 'negative', 'wreck': 'negative', 'wrest': 'negative', 'wrestle':
    'negative', 'wretch': 'negative', 'wretched': 'negative', 'wretchedly': 'negative',
    'wretchedness': 'negative', 'writhe': 'negative', 'wrong': 'negative', 'wrongful': 'negative',
    'wrongly': 'negative', 'wrought': 'negative', 'wry': 'positive', 'yawn': 'negative', 'yeah':
    'neutral', 'yearn': 'positive', 'yearning': 'positive', 'yearningly': 'positive', 'yelp':
    'negative', 'yep': 'positive', 'yes': 'positive', 'youthful': 'positive', 'zeal': 'positive',
    'zealot': 'negative', 'zealous': 'negative', 'zealously': 'negative', 'zenith': 'positive',
    'zest': 'positive'
}

SENTIMENT_SET = set(SENTIMENT_DICT.keys())

def get_sentiment(list_of_tweets):
    tweet_sentiment = {}
    for tweet in list_of_tweets:
        tweet_string = str(tweet)
        tweet_sentiment[tweet_string] = {'positive': 0, 'negative': 0, 'neutral': 0, 'both': 0}

    current_tweet = re.compile(tweet)
    for tweet in list_of_tweets:
        if current_tweet.search(tweet) is not None:
            tweet_words = re.findall(r"['a-zA-Z]+\b", list_of_tweets)
            for word in tweet_words:
                if word in SENTIMENT_SET:
                    sentiment_count = tweet_sentiment[tweet_string][SENTIMENT_DICT[word]]
                    tweet_sentiment[tweet_string][SENTIMENT_DICT[word]] = sentiment_count + 1

    #to percentify everything
    percent_tweet_sentiment = {}
    for tweet in tweet_sentiment:
        positive = tweet_sentiment[tweet]['positive']
        negative = tweet_sentiment[tweet]['negative']
        neutral = tweet_sentiment[tweet]['neutral']
        both = tweet_sentiment[tweet]['both']
        total = positive + negative + both + math.exp(-10)

    return tweet_sentiment, percent_tweet_sentiment
