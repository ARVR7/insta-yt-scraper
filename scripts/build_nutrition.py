#!/usr/bin/env python3
"""Regenerate data/nutrition.json (per 100 g of the raw/as-listed ingredient) and sanity-check it.

Values are rounded from USDA FoodData Central and the Indian Food Composition Tables (IFCT 2017),
typical packaged-product labels where noted. Treat results as accurate to roughly +/-10%.
To add an ingredient: append a row below, run this script (it rejects rows whose calories disagree
with 4P+4(C-fibre)+2fibre+9F by more than 15%, which, for foods above 100 kcal and not very fibrous, catches typos), and log the source in decision.md.

Row: key | aliases (;) | kcal | protein g | carbs g | fat g | fibre g | category | units (g per unit)
Categories: veg fruit grain legume nut seed fat sugar dairy egg meat fish spice sauce liquid other
Unit keys: tsp tbsp cup piece clove slice pinch ml(density g/ml). Missing units fall back per category.
"""
import json
import re
import sys
from pathlib import Path

ROWS = """
paneer|cottage cheese indian;panir|290|18|3|22|0|dairy|tbsp=15;cup=225;cube=10
milk (whole)|whole milk;full cream milk;milk|61|3.2|4.8|3.3|0|dairy|cup=244;density=1.03
milk (toned)|toned milk;low fat milk;2% milk|50|3.4|4.9|2|0|dairy|cup=244;density=1.03
milk (skim)|skim milk;skimmed milk;nonfat milk|34|3.4|5|0.1|0|dairy|cup=245;density=1.03
curd (plain, whole milk)|curd;dahi;plain yogurt;yoghurt;yogurt|61|3.5|4.7|3.3|0|dairy|tbsp=15;cup=245
greek yogurt (2%)|greek yogurt;hung curd;strained yogurt|73|9.9|3.9|1.9|0|dairy|tbsp=17;cup=245
greek yogurt (nonfat)|nonfat greek yogurt;fat free greek yogurt|59|10.2|3.6|0.4|0|dairy|tbsp=17;cup=245
butter|salted butter;unsalted butter|717|0.9|0.1|81|0|fat|tsp=4.7;tbsp=14;cup=227
ghee|clarified butter|900|0|0|100|0|fat|tsp=4.7;tbsp=14;cup=218
cheddar cheese|cheddar;cheese|403|24.9|1.3|33.1|0|dairy|slice=21;tbsp=7;cup=113
mozzarella (low moisture)|mozzarella;pizza cheese;processed cheese|300|22|2.2|22.4|0|dairy|slice=21;tbsp=7;cup=112
parmesan|parmesan cheese;parmigiano|431|38|4.1|29|0|dairy|tbsp=5;cup=100
cream cheese|philadelphia|342|6|4.1|34|0|dairy|tbsp=14.5
heavy cream|cream;fresh cream;whipping cream|340|2.8|2.8|36|0|dairy|tbsp=15;cup=238;density=0.99
sour cream|soured cream|198|2.4|4.6|19.4|0|dairy|tbsp=12
condensed milk|sweetened condensed milk|321|7.9|54.4|8.7|0|dairy|tbsp=19
egg|eggs;whole egg|143|12.6|0.7|9.5|0|egg|piece=50
egg white|egg whites|52|10.9|0.7|0.2|0|egg|piece=33;cup=243
egg yolk|egg yolks|322|15.9|3.6|26.5|0|egg|piece=17
chicken breast|chicken breast raw;boneless chicken;chicken|120|22.5|0|2.6|0|meat|piece=174;cup=140
chicken thigh|boneless chicken thigh|121|19.7|0|4.1|0|meat|piece=100
chicken (minced)|minced chicken;ground chicken;chicken mince|143|17.4|0|8.1|0|meat|cup=225
mutton|lamb;goat meat;mutton curry cut|209|20|0|14|0|meat|cup=140
beef (lean mince)|lean beef;ground beef 95%|137|21.4|0|5|0|meat|cup=225
beef (80/20 mince)|ground beef;beef mince;beef|254|17.2|0|20|0|meat|cup=225
pork loin|pork|143|21.4|0|5.7|0|meat|cup=140
bacon (cooked)|bacon|541|37|1.4|42|0|meat|slice=8
salmon|salmon fillet|208|20.4|0|13.4|0|fish|piece=170
tuna (canned in water)|tuna;canned tuna|116|25.5|0|0.8|0|fish|can=140
shrimp|prawns;prawn|85|20.1|0.2|0.5|0|fish|piece=7
white fish|cod;fish fillet;basa;fish|82|17.8|0|0.7|0|fish|piece=150
rice (white, raw)|rice;raw rice|365|7.1|80|0.7|1.3|grain|cup=185
rice (basmati, raw)|basmati rice;basmati|350|8|78|0.6|1|grain|cup=185
rice (white, cooked)|cooked rice;steamed rice|130|2.7|28.2|0.3|0.4|grain|cup=158
rice (brown, raw)|brown rice|370|7.9|77.2|2.9|3.5|grain|cup=190
whole wheat flour (atta)|atta;whole wheat flour;wheat flour;chapati flour|340|13.2|72|2.5|10.7|grain|tbsp=7.5;cup=120
all-purpose flour (maida)|maida;all purpose flour;plain flour;refined flour;flour|364|10.3|76.3|1|2.7|grain|tbsp=8;cup=125
oats (rolled)|oats;rolled oats;oatmeal|379|13.2|67.7|6.5|10.1|grain|tbsp=5;cup=80
besan (gram flour)|besan;gram flour;chickpea flour|387|22.4|57.8|6.7|10.8|grain|tbsp=7;cup=92
semolina (suji)|suji;rava;sooji;semolina|360|12.7|72.8|1.1|3.9|grain|tbsp=10;cup=167
cornflour|corn starch;cornstarch;corn flour|381|0.3|91.3|0.1|0.9|grain|tbsp=8;cup=128
poha (flattened rice)|poha;flattened rice;beaten rice|346|6.6|77.3|1.2|2|grain|cup=60
pasta (dry)|pasta;spaghetti;penne;macaroni|371|13|74.7|1.5|3.2|grain|cup=100
quinoa (raw)|quinoa|368|14.1|64.2|6.1|7|grain|cup=170
bread (white)|white bread;bread|266|8.9|49.4|3.3|2.7|grain|slice=28;piece=28
bread (whole wheat)|brown bread;whole wheat bread;multigrain bread|252|12.5|42.7|3.5|6|grain|slice=32;piece=32
tortilla (flour)|tortilla;wrap;flour tortilla|312|8.3|51.7|8|2.5|grain|piece=45
roti (store-bought)|roti;chapati;phulka|297|9.6|50|5.9|7|grain|piece=40
toor dal (raw)|toor dal;arhar dal;pigeon pea;tur dal|335|22.3|57.6|1.7|15|legume|cup=200
moong dal (raw)|moong dal;green gram split;yellow moong dal|348|24|59.9|1.3|16|legume|cup=200
masoor dal (raw)|masoor dal;red lentils;lentils|352|24.6|63.4|1.1|10.7|legume|cup=192
chana dal (raw)|chana dal;split chickpeas;bengal gram dal|372|20.8|59.8|5.6|17|legume|cup=200
chickpeas (dry)|kabuli chana;chole;dry chickpeas|378|20.5|63|6|12.2|legume|cup=200
chickpeas (cooked)|boiled chickpeas;canned chickpeas;cooked chickpeas;chana|164|8.9|27.4|2.6|7.6|legume|cup=164
rajma (dry)|kidney beans;rajma;red kidney beans|337|23.6|61.3|0.8|15.2|legume|cup=184
black beans (dry)|black beans|341|21.6|62.4|1.4|15.5|legume|cup=194
tofu (firm)|tofu;soy paneer|144|17.3|2.8|8.7|2.3|legume|cup=252;piece=85
soya chunks (dry)|soya chunks;soy chunks;nutrela;meal maker;textured soy protein|345|52|33|0.5|13|legume|cup=90
peanut butter|peanut butter smooth;pb|588|25|20|50|6|nut|tbsp=16;cup=258
peanuts|groundnuts;roasted peanuts;moongphali|567|25.8|16.1|49.2|8.5|nut|tbsp=9;cup=146
almonds|badam|579|21.2|21.6|49.9|12.5|nut|tbsp=9;cup=143;piece=1.2
cashews|kaju|553|18.2|30.2|43.9|3.3|nut|tbsp=8;cup=130;piece=1.5
walnuts|akhrot|654|15.2|13.7|65.2|6.7|nut|tbsp=7;cup=117
pistachios|pista|562|20.2|27.2|45.3|10.3|nut|tbsp=8;cup=123
chia seeds|chia|486|16.5|42.1|30.7|34.4|seed|tsp=4;tbsp=12;cup=170
flax seeds|flaxseed;alsi|534|18.3|28.9|42.2|27.3|seed|tsp=3.5;tbsp=10;cup=168
sesame seeds|til;sesame|573|17.7|23.5|49.7|11.8|seed|tsp=3;tbsp=9;cup=144
sunflower seeds|sunflower seed|584|20.8|20|51.5|8.6|seed|tbsp=9;cup=140
tahini|sesame paste|595|17|21.2|53.8|9.3|seed|tbsp=15
desiccated coconut|coconut powder;dry coconut|660|6.9|23.7|64.5|16.3|nut|tbsp=5;cup=93
coconut (fresh)|fresh coconut;grated coconut;nariyal|354|3.3|15.2|33.5|9|nut|tbsp=8;cup=80
coconut milk|coconut milk canned|197|2|2.8|21.3|0|liquid|cup=226;density=0.97
onion|onions;pyaz;red onion;white onion|40|1.1|9.3|0.1|1.7|veg|piece=110;cup=160
tomato|tomatoes;tamatar|18|0.9|3.9|0.2|1.2|veg|piece=123;cup=180
potato|potatoes;aloo|77|2|17.5|0.1|2.2|veg|piece=170;cup=150
sweet potato|shakarkandi;sweet potatoes|86|1.6|20.1|0.1|3|veg|piece=130;cup=133
carrot|carrots;gajar|41|0.9|9.6|0.2|2.8|veg|piece=61;cup=128
bell pepper|capsicum;shimla mirch;bell peppers|31|1|6|0.3|2.1|veg|piece=119;cup=92
green chili|green chilli;hari mirch;green chillies|40|2|9|0.2|1.5|veg|piece=6
garlic|lehsun|149|6.4|33.1|0.5|2.1|veg|clove=3;tsp=3;tbsp=9
ginger|adrak;fresh ginger|80|1.8|17.8|0.8|2|veg|tsp=2;tbsp=6;piece=11
spinach|palak|23|2.9|3.6|0.4|2.2|veg|cup=30
cauliflower|gobi;phool gobhi|25|1.9|5|0.3|2|veg|cup=107
broccoli|broccoli florets|34|2.8|6.6|0.4|2.6|veg|cup=91
cucumber|kheera;cucumbers|15|0.7|3.6|0.1|0.5|veg|piece=200;cup=104
cabbage|patta gobi|25|1.3|5.8|0.1|2.5|veg|cup=70
green peas|peas;matar;frozen peas|81|5.4|14.5|0.4|5.7|veg|cup=145
sweet corn|corn;corn kernels;bhutta|86|3.3|19|1.4|2|veg|cup=154
mushrooms|mushroom;button mushrooms|22|3.1|3.3|0.3|1|veg|cup=70;piece=18
zucchini|courgette|17|1.2|3.1|0.3|1|veg|piece=196;cup=124
lettuce|iceberg lettuce;romaine|15|1.4|2.9|0.2|1.3|veg|cup=36
avocado|avocados|160|2|8.5|14.7|6.7|fruit|piece=136;cup=150
beetroot|beet;chukandar|43|1.6|9.6|0.2|2.8|veg|piece=82;cup=136
pumpkin|kaddu|26|1|6.5|0.1|0.5|veg|cup=116
eggplant|brinjal;baingan;aubergine|25|1|5.9|0.2|3|veg|piece=458;cup=82
okra|bhindi;lady finger|33|1.9|7.5|0.2|3.2|veg|cup=100
green beans|french beans;beans|31|1.8|7|0.2|2.7|veg|cup=110
coriander leaves|cilantro;dhania;fresh coriander|23|2.1|3.7|0.5|2.8|veg|tbsp=1;cup=16
mint leaves|pudina;mint|44|3.3|8.4|0.7|6.8|veg|tbsp=1.5;cup=24
lemon juice|lemon;lime juice;nimbu|22|0.4|6.9|0.2|0.3|liquid|tbsp=15;tsp=5;piece=30;density=1.03
banana|bananas|89|1.1|22.8|0.3|2.6|fruit|piece=118;cup=150
apple|apples|52|0.3|13.8|0.2|2.4|fruit|piece=182;cup=125
orange|oranges|47|0.9|11.8|0.1|2.4|fruit|piece=131
mango|mangoes|60|0.8|15|0.4|1.6|fruit|piece=336;cup=165
blueberries|blueberry|57|0.7|14.5|0.3|2.4|fruit|cup=148
strawberries|strawberry|32|0.7|7.7|0.3|2|fruit|cup=152;piece=12
dates|khajoor;medjool dates;date|282|2.5|75|0.4|8|fruit|piece=24;cup=147
raisins|kishmish|299|3.1|79.2|0.5|3.7|fruit|tbsp=9;cup=145
pineapple|pineapple chunks|50|0.5|13.1|0.1|1.4|fruit|cup=165
watermelon|tarbooz|30|0.6|7.6|0.2|0.4|fruit|cup=152
olive oil|extra virgin olive oil|884|0|0|100|0|fat|tsp=4.5;tbsp=13.5;cup=216;density=0.91
vegetable oil|oil;cooking oil;sunflower oil;refined oil;canola oil;mustard oil|884|0|0|100|0|fat|tsp=4.5;tbsp=13.5;cup=218;density=0.92
coconut oil|nariyal tel|862|0|0|100|0|fat|tsp=4.5;tbsp=13.6;cup=218
sugar|white sugar;cheeni;powdered sugar|387|0|100|0|0|sugar|tsp=4.2;tbsp=12.5;cup=200
brown sugar|demerara|380|0.1|98.1|0|0|sugar|tsp=4.5;tbsp=14;cup=220
jaggery|gur|383|0.4|98|0.1|0|sugar|tsp=5;tbsp=15;piece=10
honey|shahad|304|0.3|82.4|0|0.2|sugar|tsp=7;tbsp=21;cup=339
maple syrup|maple|260|0|67|0.1|0|sugar|tbsp=20
dark chocolate (70-85%)|dark chocolate;chocolate|598|7.8|45.9|42.6|10.9|sugar|piece=10;tbsp=10
cocoa powder|cocoa|228|19.6|57.9|13.7|33.2|sugar|tsp=2.7;tbsp=5.4
whey protein powder|whey;protein powder;whey protein|400|80|8|6|0|other|scoop=30;tbsp=10
black pepper|pepper;kali mirch|251|10.4|64|3.3|25|spice|tsp=2.3;tbsp=6.9
turmeric|haldi;turmeric powder|312|9.7|67.1|3.3|22.7|spice|tsp=3;tbsp=9
red chili powder|chili powder;chilli powder;lal mirch;red chilli powder;kashmiri chili|282|13.5|49.7|14.3|34.8|spice|tsp=2.7;tbsp=8
cumin seeds|jeera;cumin;jeera powder|375|17.8|44.2|22.3|10.5|spice|tsp=2.1;tbsp=6.3
coriander powder|dhania powder;coriander seeds|298|12.4|55|17.8|41.9|spice|tsp=1.8;tbsp=5.4
garam masala|spice mix;masala;chaat masala;tikka masala powder;spices|330|12|55|13|30|spice|tsp=2.5;tbsp=7.5
cinnamon|dalchini|247|4|80.6|1.2|53.1|spice|tsp=2.6;tbsp=7.8
cardamom|elaichi|311|10.8|68.5|6.7|28|spice|tsp=2;pod=0.3
cloves|laung|274|6|65|13|33.9|spice|tsp=2.1;piece=0.2
mustard seeds|rai;sarson|508|26.1|28.1|36.2|12.2|spice|tsp=3.3;tbsp=10
salt|namak;table salt;rock salt|0|0|0|0|0|spice|tsp=6;tbsp=18;pinch=0.4
baking powder|baking soda|53|0|27.7|0|0.2|other|tsp=4.6
yeast|dry yeast|325|40|41|7.6|27|other|tsp=3;packet=7
soy sauce|soya sauce|53|8.1|4.9|0.6|0.8|sauce|tsp=5.3;tbsp=16;density=1.2
tomato ketchup|ketchup|101|1|27.4|0.1|0.3|sauce|tbsp=17
tomato puree|tomato paste;tomato sauce|82|4.3|18.9|0.5|4.1|sauce|tbsp=16;cup=262
mayonnaise|mayo|680|1|0.6|75|0|sauce|tbsp=14
mustard (prepared)|mustard|66|4.4|5.8|4|3.3|sauce|tsp=5;tbsp=15
vinegar|apple cider vinegar;white vinegar|18|0|0|0|0|liquid|tsp=5;tbsp=15;density=1.01
hummus|houmous|166|7.9|14.3|9.6|6|sauce|tbsp=15
water|ice|0|0|0|0|0|liquid|cup=240;density=1
stock (vegetable/chicken)|broth;stock;chicken stock;vegetable stock|7|0.6|0.9|0.1|0|liquid|cup=240;density=1
coffee (brewed)|coffee;black coffee;espresso|1|0.1|0|0|0|liquid|cup=237;density=1
"""

CAT_UNITS = {  # grams per unit when a row does not say
    "liquid": {"tsp": 5, "tbsp": 15, "cup": 240},
    "fat": {"tsp": 4.5, "tbsp": 13.5, "cup": 216},
    "sugar": {"tsp": 4.2, "tbsp": 12.5, "cup": 200},
    "spice": {"tsp": 2.5, "tbsp": 7.5, "pinch": 0.4},
}


def parse():
    out = {}
    for line in ROWS.strip().splitlines():
        key, aliases, kcal, p, c, f, fib, cat, units = line.split("|")
        u = {}
        for part in filter(None, units.split(";")):
            k, v = part.split("=")
            u[k] = float(v)
        kcal, p, c, f, fib = map(float, (kcal, p, c, f, fib))
        est = 4 * p + 4 * (c - fib) + 2 * fib + 9 * f  # fibre gives about 2 kcal/g
        if kcal >= 100 and fib < 15 and abs(est - kcal) > 0.15 * kcal:  # very fibrous foods (cocoa, spices, seeds) use USDA's special energy factors
            sys.exit(f"nutrition row '{key}': {kcal} kcal disagrees with 4P+4C+9F={est:.0f}")
        out[key] = {"aliases": [a for a in aliases.split(";") if a], "kcal": kcal, "protein": p, "carbs": c, "fat": f,
                    "fibre": fib, "category": cat, "units": {**CAT_UNITS.get(cat, {}), **u}}
    return out


def main():
    data = parse()
    names = {}
    for k, v in data.items():
        for n in [k] + v["aliases"]:
            n = re.sub(r"\s+", " ", n.lower().strip())
            if n in names and names[n] != k:
                sys.exit(f"alias '{n}' is used by both '{names[n]}' and '{k}'")
            names[n] = k
    meta = {"_about": "Per 100 g. Rounded from USDA FoodData Central and IFCT 2017; labels for packaged items vary. Accurate to about +/-10%. Source: scripts/build_nutrition.py",
            "items": data}
    p = Path(__file__).resolve().parent.parent / "data" / "nutrition.json"
    p.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(data)} ingredients, {len(names)} names -> {p.name}")


if __name__ == "__main__":
    main()
