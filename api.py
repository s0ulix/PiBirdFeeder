import flask
from flask import request, jsonify
import datetime
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import pickle
from PIL import Image
import base64
from keras.models import load_model
import numpy as np

model = load_model('model_tuned_95.30_260B.h5')
#model = pickle.load(open('model_tuned_95.30_260B.h5','rb'))

app = flask.Flask(__name__)
#app.config["DEBUG"] = True


result = {
    "spieces_com_name": "crow"
}

@app.route('/api/getImageClassification', methods=['POST'])
def imageClassify():
    data = request.json
    imagestr = data["image"]
    timestamp = datetime.datetime.now().strftime("%s")
    
    ext = imagestr.split(";")[0].split("/")[1]
    base64str = imagestr.split(",")[1]
    
    # create file name and save to uploads folder
    filename = "uploads/bird_detect_" + timestamp + "." + ext
    imagedata = base64.b64decode(base64str)
    with open(filename, "wb") as fh:
        fh.write(imagedata)


    img = Image.open(filename)
   
    Categories = ['AFRICAN CROWNED CRANE','AFRICAN FIREFINCH','ALBATROSS','ALEXANDRINE PARAKEET','AMERICAN AVOCET','AMERICAN BITTERN','AMERICAN COOT','AMERICAN GOLDFINCH','AMERICAN KESTREL','AMERICAN PIPIT','AMERICAN REDSTART','ANHINGA','ANNAS HUMMINGBIRD','ANTBIRD','ARARIPE MANAKIN','ASIAN CRESTED IBIS','BALD EAGLE','BALI STARLING','BALTIMORE ORIOLE','BANANAQUIT','BANDED BROADBILL','BAR-TAILED GODWIT','BARN OWL','BARN SWALLOW','BARRED PUFFBIRD','BAY-BREASTED WARBLER','BEARDED BARBET','BELTED KINGFISHER','BIRD OF PARADISE','BLACK FRANCOLIN','BLACK SKIMMER','BLACK SWAN','BLACK TAIL CRAKE','BLACK THROATED WARBLER','BLACK VULTURE','BLACK-CAPPED CHICKADEE','BLACK-NECKED GREBE','BLACK-THROATED SPARROW','BLACKBURNIAM WARBLER','BLUE GROUSE','BLUE HERON','BOBOLINK','BROWN NOODY','BROWN THRASHER','CACTUS WREN','CALIFORNIA CONDOR','CALIFORNIA GULL','CALIFORNIA QUAIL','CANARY','CAPE MAY WARBLER','CAPUCHINBIRD','CARMINE BEE-EATER','CASPIAN TERN','CASSOWARY','CHARA DE COLLAR','CHIPPING SPARROW','CHUKAR PARTRIDGE','CINNAMON TEAL','COCK OF THE  ROCK','COCKATOO','COMMON FIRECREST','COMMON GRACKLE','COMMON HOUSE MARTIN','COMMON LOON','COMMON POORWILL','COMMON STARLING','COUCHS KINGBIRD','CRESTED AUKLET','CRESTED CARACARA','CRESTED NUTHATCH','CROW','CROWNED PIGEON','CUBAN TODY','CURL CRESTED ARACURI','D-ARNAUDS BARBET','DARK EYED JUNCO','DOWNY WOODPECKER','EASTERN BLUEBIRD','EASTERN MEADOWLARK','EASTERN ROSELLA','EASTERN TOWEE','ELEGANT TROGON','ELLIOTS  PHEASANT','EMPEROR PENGUIN','EMU','ENGGANO MYNA','EURASIAN GOLDEN ORIOLE','EURASIAN MAGPIE','EVENING GROSBEAK','FIRE TAILLED MYZORNIS','FLAME TANAGER','FLAMINGO','FRIGATE','GAMBELS QUAIL','GANG GANG COCKATOO','GILA WOODPECKER','GILDED FLICKER','GLOSSY IBIS','GO AWAY BIRD','GOLD WING WARBLER','GOLDEN CHEEKED WARBLER','GOLDEN CHLOROPHONIA','GOLDEN EAGLE','GOLDEN PHEASANT','GOLDEN PIPIT','GOULDIAN FINCH','GRAY CATBIRD','GRAY PARTRIDGE','GREAT POTOO','GREATOR SAGE GROUSE','GREEN JAY','GREY PLOVER','GUINEA TURACO','GUINEAFOWL','GYRFALCON','HARPY EAGLE','HAWAIIAN GOOSE','HELMET VANGA','HIMALAYAN MONAL','HOATZIN','HOODED MERGANSER','HOOPOES','HORNBILL','HORNED GUAN','HORNED SUNGEM','HOUSE FINCH','HOUSE SPARROW','IMPERIAL SHAQ','INCA TERN','INDIAN BUSTARD','INDIAN PITTA','INDIGO BUNTING','JABIRU','JAVA SPARROW','JAVAN MAGPIE','KAKAPO','KILLDEAR','KING VULTURE','KIWI','KOOKABURRA','LARK BUNTING','LEARS MACAW','LILAC ROLLER','LONG-EARED OWL','MAGPIE GOOSE','MALABAR HORNBILL','MALACHITE KINGFISHER','MALEO','MALLARD DUCK','MANDRIN DUCK','MARABOU STORK','MASKED BOOBY','MASKED LAPWING','MIKADO  PHEASANT','MOURNING DOVE','MYNA','NICOBAR PIGEON','NOISY FRIARBIRD','NORTHERN BALD IBIS','NORTHERN CARDINAL','NORTHERN FLICKER','NORTHERN GANNET','NORTHERN GOSHAWK','NORTHERN JACANA','NORTHERN MOCKINGBIRD','NORTHERN PARULA','NORTHERN RED BISHOP','NORTHERN SHOVELER','OCELLATED TURKEY','OKINAWA RAIL','OSPREY','OSTRICH','OYSTER CATCHER','PAINTED BUNTIG','PALILA','PARADISE TANAGER','PARUS MAJOR','PEACOCK','PELICAN','PEREGRINE FALCON','PHILIPPINE EAGLE','PINK ROBIN','PUFFIN','PURPLE FINCH','PURPLE GALLINULE','PURPLE MARTIN','PURPLE SWAMPHEN','QUETZAL','RAINBOW LORIKEET','RAZORBILL','RED BEARDED BEE EATER','RED BELLIED PITTA','RED FACED CORMORANT','RED FACED WARBLER','RED HEADED DUCK','RED HEADED WOODPECKER','RED HONEY CREEPER','RED TAILED THRUSH','RED WINGED BLACKBIRD','RED WISKERED BULBUL','REGENT BOWERBIRD','RING-NECKED PHEASANT','ROADRUNNER','ROBIN','ROCK DOVE','ROSY FACED LOVEBIRD','ROUGH LEG BUZZARD','RUBY THROATED HUMMINGBIRD','RUFOUS KINGFISHER','RUFUOS MOTMOT','SAMATRAN THRUSH','SAND MARTIN','SCARLET IBIS','SCARLET MACAW','SHOEBILL','SHORT BILLED DOWITCHER','SMITHS LONGSPUR','SNOWY EGRET','SNOWY OWL','SORA','SPANGLED COTINGA','SPLENDID WREN','SPOON BILED SANDPIPER','SPOONBILL','SRI LANKA BLUE MAGPIE','STEAMER DUCK','STORK BILLED KINGFISHER','STRAWBERRY FINCH','STRIPPED SWALLOW','SUPERB STARLING','SWINHOES PHEASANT','TAIWAN MAGPIE','TAKAHE','TASMANIAN HEN','TEAL DUCK','TIT MOUSE','TOUCHAN','TOWNSENDS WARBLER','TREE SWALLOW','TRUMPTER SWAN','TURKEY VULTURE','TURQUOISE MOTMOT','UMBRELLA BIRD','VARIED THRUSH','VENEZUELIAN TROUPIAL','VERMILION FLYCATHER','VICTORIA CROWNED PIGEON','VIOLET GREEN SWALLOW','VULTURINE GUINEAFOWL','WATTLED CURASSOW','WHIMBREL','WHITE CHEEKED TURACO','WHITE NECKED RAVEN','WHITE TAILED TROPIC','WILD TURKEY','WILSONS BIRD OF PARADISE','WOOD DUCK','YELLOW BELLIED FLOWERPECKER','YELLOW CACIQUE','YELLOW HEADED BLACKBIRD']
    
    img = np.array(img)
    img_resized = np.expand_dims(resize(img, (150, 150,3)), 0)
    y_out = model.predict(img_resized)
    y_out = y_out.argmax(axis=-1)
    y_out = Categories[y_out[0]]
    result["spieces_com_name"] = y_out

    return jsonify(result)

app.run(host="0.0.0.0", port=8501)
