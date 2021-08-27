

#importing modules
import time
import picamera
import RPi.GPIO as GPIO
from datetime import datetime
from keras.models import load_model
import numpy as np
from PIL import Image
from skimage.transform import resize

#loading model
model = load_model('model_tuned_95.30_260B.h5')

#function to identify bird
def imageClassify(filename):

    #loading image file
    img = Image.open(filename)

    #categories of birds
    Categories = ['AFRICAN CROWNED CRANE','AFRICAN FIREFINCH','ALBATROSS','ALEXANDRINE PARAKEET','AMERICAN AVOCET','AMERICAN BITTERN','AMERICAN COOT','AMERICAN GOLDFINCH','AMERICAN KESTREL','AMERICAN PIPIT','AMERICAN REDSTART','ANHINGA','ANNAS HUMMINGBIRD','ANTBIRD','ARARIPE MANAKIN','ASIAN CRESTED IBIS','BALD EAGLE','BALI STARLING','BALTIMORE ORIOLE','BANANAQUIT','BANDED BROADBILL','BAR-TAILED GODWIT','BARN OWL','BARN SWALLOW','BARRED PUFFBIRD','BAY-BREASTED WARBLER','BEARDED BARBET','BELTED KINGFISHER','BIRD OF PARADISE','BLACK FRANCOLIN','BLACK SKIMMER','BLACK SWAN','BLACK TAIL CRAKE','BLACK THROATED WARBLER','BLACK VULTURE','BLACK-CAPPED CHICKADEE','BLACK-NECKED GREBE','BLACK-THROATED SPARROW','BLACKBURNIAM WARBLER','BLUE GROUSE','BLUE HERON','BOBOLINK','BROWN NOODY','BROWN THRASHER','CACTUS WREN','CALIFORNIA CONDOR','CALIFORNIA GULL','CALIFORNIA QUAIL','CANARY','CAPE MAY WARBLER','CAPUCHINBIRD','CARMINE BEE-EATER','CASPIAN TERN','CASSOWARY','CHARA DE COLLAR','CHIPPING SPARROW','CHUKAR PARTRIDGE','CINNAMON TEAL','COCK OF THE  ROCK','COCKATOO','COMMON FIRECREST','COMMON GRACKLE','COMMON HOUSE MARTIN','COMMON LOON','COMMON POORWILL','COMMON STARLING','COUCHS KINGBIRD','CRESTED AUKLET','CRESTED CARACARA','CRESTED NUTHATCH','CROW','CROWNED PIGEON','CUBAN TODY','CURL CRESTED ARACURI','D-ARNAUDS BARBET','DARK EYED JUNCO','DOWNY WOODPECKER','EASTERN BLUEBIRD','EASTERN MEADOWLARK','EASTERN ROSELLA','EASTERN TOWEE','ELEGANT TROGON','ELLIOTS  PHEASANT','EMPEROR PENGUIN','EMU','ENGGANO MYNA','EURASIAN GOLDEN ORIOLE','EURASIAN MAGPIE','EVENING GROSBEAK','FIRE TAILLED MYZORNIS','FLAME TANAGER','FLAMINGO','FRIGATE','GAMBELS QUAIL','GANG GANG COCKATOO','GILA WOODPECKER','GILDED FLICKER','GLOSSY IBIS','GO AWAY BIRD','GOLD WING WARBLER','GOLDEN CHEEKED WARBLER','GOLDEN CHLOROPHONIA','GOLDEN EAGLE','GOLDEN PHEASANT','GOLDEN PIPIT','GOULDIAN FINCH','GRAY CATBIRD','GRAY PARTRIDGE','GREAT POTOO','GREATOR SAGE GROUSE','GREEN JAY','GREY PLOVER','GUINEA TURACO','GUINEAFOWL','GYRFALCON','HARPY EAGLE','HAWAIIAN GOOSE','HELMET VANGA','HIMALAYAN MONAL','HOATZIN','HOODED MERGANSER','HOOPOES','HORNBILL','HORNED GUAN','HORNED SUNGEM','HOUSE FINCH','HOUSE SPARROW','IMPERIAL SHAQ','INCA TERN','INDIAN BUSTARD','INDIAN PITTA','INDIGO BUNTING','JABIRU','JAVA SPARROW','JAVAN MAGPIE','KAKAPO','KILLDEAR','KING VULTURE','KIWI','KOOKABURRA','LARK BUNTING','LEARS MACAW','LILAC ROLLER','LONG-EARED OWL','MAGPIE GOOSE','MALABAR HORNBILL','MALACHITE KINGFISHER','MALEO','MALLARD DUCK','MANDRIN DUCK','MARABOU STORK','MASKED BOOBY','MASKED LAPWING','MIKADO  PHEASANT','MOURNING DOVE','MYNA','NICOBAR PIGEON','NOISY FRIARBIRD','NORTHERN BALD IBIS','NORTHERN CARDINAL','NORTHERN FLICKER','NORTHERN GANNET','NORTHERN GOSHAWK','NORTHERN JACANA','NORTHERN MOCKINGBIRD','NORTHERN PARULA','NORTHERN RED BISHOP','NORTHERN SHOVELER','OCELLATED TURKEY','OKINAWA RAIL','OSPREY','OSTRICH','OYSTER CATCHER','PAINTED BUNTIG','PALILA','PARADISE TANAGER','PARUS MAJOR','PEACOCK','PELICAN','PEREGRINE FALCON','PHILIPPINE EAGLE','PINK ROBIN','PUFFIN','PURPLE FINCH','PURPLE GALLINULE','PURPLE MARTIN','PURPLE SWAMPHEN','QUETZAL','RAINBOW LORIKEET','RAZORBILL','RED BEARDED BEE EATER','RED BELLIED PITTA','RED FACED CORMORANT','RED FACED WARBLER','RED HEADED DUCK','RED HEADED WOODPECKER','RED HONEY CREEPER','RED TAILED THRUSH','RED WINGED BLACKBIRD','RED WISKERED BULBUL','REGENT BOWERBIRD','RING-NECKED PHEASANT','ROADRUNNER','ROBIN','ROCK DOVE','ROSY FACED LOVEBIRD','ROUGH LEG BUZZARD','RUBY THROATED HUMMINGBIRD','RUFOUS KINGFISHER','RUFUOS MOTMOT','SAMATRAN THRUSH','SAND MARTIN','SCARLET IBIS','SCARLET MACAW','SHOEBILL','SHORT BILLED DOWITCHER','SMITHS LONGSPUR','SNOWY EGRET','SNOWY OWL','SORA','SPANGLED COTINGA','SPLENDID WREN','SPOON BILED SANDPIPER','SPOONBILL','SRI LANKA BLUE MAGPIE','STEAMER DUCK','STORK BILLED KINGFISHER','STRAWBERRY FINCH','STRIPPED SWALLOW','SUPERB STARLING','SWINHOES PHEASANT','TAIWAN MAGPIE','TAKAHE','TASMANIAN HEN','TEAL DUCK','TIT MOUSE','TOUCHAN','TOWNSENDS WARBLER','TREE SWALLOW','TRUMPTER SWAN','TURKEY VULTURE','TURQUOISE MOTMOT','UMBRELLA BIRD','VARIED THRUSH','VENEZUELIAN TROUPIAL','VERMILION FLYCATHER','VICTORIA CROWNED PIGEON','VIOLET GREEN SWALLOW','VULTURINE GUINEAFOWL','WATTLED CURASSOW','WHIMBREL','WHITE CHEEKED TURACO','WHITE NECKED RAVEN','WHITE TAILED TROPIC','WILD TURKEY','WILSONS BIRD OF PARADISE','WOOD DUCK','YELLOW BELLIED FLOWERPECKER','YELLOW CACIQUE','YELLOW HEADED BLACKBIRD']

    #reading image to numpy array
    img = np.array(img)

    #resizing image for the model
    img_resized = np.expand_dims(resize(img, (150, 150,3)), 0)

    #predicting species
    y_out = model.predict(img_resized)
    y_out = y_out.argmax(axis=-1)
    y_out = Categories[y_out[0]]

    return "Species ="+str(y_out)




#function to capture the image from the camera
def cap_img():

    #opening camera object
    with picamera.PiCamera() as camera:

        #configuring resolution of the camera
        camera.resolution = (1024, 768)

        #loop for taking n pitures chnge the range value to your preferred number of images when motion detected
        for i in range(3):

            #getting present time
            now = datetime.now()

            #creating a file name as per the present time
            img_name = "/home/pi/Desktop/cv/Pi_Image_{}.png".format(now)

            #capturing the image and saving it by the name of the file name created above
            camera.capture(img_name)

            #printing that the image is captured
            print("{} written!".format(img_name))

            #calling the function to get the name of the bird
            res=imageClassify(img_name)

            #opening result txt file to add the result into the result.txt
            with open("/home/pi/Desktop/cv/result.txt","a+") as txt_file:

                #writing result with the name of the image
                txt_file.write(img_name+" - "+str(res)+"\n")

            #printing result
            print(img_name+"-"+str(res))

#GPIO configurations
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#pin number where the motion detector is attached
#Note: its the physical pin no not the gpio number
pin_no=40

#stting the pin for the input from motion detector
GPIO.setup(pin_no, GPIO.IN)

#while true loop to work untill the program is not stopped 
while True:

    #getting output of the motion detector in variable i, 1 for motion and 0 for no motion
    i=GPIO.input(pin_no)

    #if motion is detected execute if block
    if i==1:

        #printing the motion detected
        print( "Motion detected")

        #calling the function to capture the image which will futhur call the api function
        cap_img()

        #waiting for one second
        time.sleep(1)
    else:
        
        #waiting for 1 second
        time.sleep(1)
