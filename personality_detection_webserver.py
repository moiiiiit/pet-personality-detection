from re import match
from flask import Flask
from flask import request
import math
import json
from personality_detection import predictHumanPersonality, predictPetPersonality

app = Flask(__name__)
userdatafile = "./jsondb/userdata.json"
userdata = json.loads(open(userdatafile).read())


def calculatePersonalities(name):
    petPersonality = predictPetPersonality(
        userdata[name]["pet_data"]["adjectives"])
    userPersonality = predictHumanPersonality(
        userdata[name]["pet_data"]["essay"])
    userdata[name]["pet_data"]["fear"] = float(petPersonality["fear"])
    userdata[name]["pet_data"]["anger"] = float(petPersonality["anger"])
    userdata[name]["pet_data"]["anticip"] = float(petPersonality["anticip"])
    userdata[name]["pet_data"]["trust"] = float(petPersonality["trust"])
    userdata[name]["pet_data"]["surprise"] = float(petPersonality["surprise"])
    userdata[name]["pet_data"]["positive"] = float(petPersonality["positive"])
    userdata[name]["pet_data"]["negative"] = float(petPersonality["negative"])
    userdata[name]["pet_data"]["sadness"] = float(petPersonality["sadness"])
    userdata[name]["pet_data"]["disgust"] = float(petPersonality["disgust"])
    userdata[name]["pet_data"]["joy"] = float(petPersonality["joy"])
    userdata[name]["openness"] = int(userPersonality[0])
    userdata[name]["conscientiousness"] = int(userPersonality[3])
    userdata[name]["extraversion"] = int(userPersonality[4])
    userdata[name]["agreeableness"] = int(userPersonality[2])
    userdata[name]["neuroticism"] = int(userPersonality[1])
    with open(userdatafile, "w") as f:
        json.dump(userdata, f)
        f.close()


def calculateDistances(name1, name2):
    petprofile1 = userdata[name1]["pet_data"]
    petprofile2 = userdata[name2]["pet_data"]
    distance1 = math.sqrt(
        math.pow(float(petprofile1["fear"]), 2) +
        math.pow(float(petprofile1["anger"]), 2) +
        math.pow(float(petprofile1["anticip"]), 2) +
        math.pow(float(petprofile1["trust"]), 2) +
        math.pow(float(petprofile1["surprise"]), 2) +
        math.pow(float(petprofile1["positive"]), 2) +
        math.pow(float(petprofile1["negative"]), 2) +
        math.pow(float(petprofile1["sadness"]), 2) +
        math.pow(float(petprofile1["disgust"]), 2) +
        math.pow(float(petprofile1["joy"]), 2) +
        math.pow(float(petprofile2["fear"]), 2) +
        math.pow(float(petprofile2["anger"]), 2) +
        math.pow(float(petprofile2["anticip"]), 2) +
        math.pow(float(petprofile2["trust"]), 2) +
        math.pow(float(petprofile2["surprise"]), 2) +
        math.pow(float(petprofile2["positive"]), 2) +
        math.pow(float(petprofile2["negative"]), 2) +
        math.pow(float(petprofile2["sadness"]), 2) +
        math.pow(float(petprofile2["disgust"]), 2) +
        math.pow(float(petprofile2["joy"]), 2)

    )
    distance2 = math.sqrt(
        math.pow(float(userdata[name1]["openness"]), 2) +
        math.pow(float(userdata[name1]["conscientiousness"]), 2) +
        math.pow(float(userdata[name1]["extraversion"]), 2) +
        math.pow(float(userdata[name1]["agreeableness"]), 2) +
        math.pow(float(userdata[name1]["neuroticism"]), 2) +
        math.pow(float(userdata[name2]["openness"]), 2) +
        math.pow(float(userdata[name2]["conscientiousness"]), 2) +
        math.pow(float(userdata[name2]["extraversion"]), 2) +
        math.pow(float(userdata[name2]["agreeableness"]), 2) +
        math.pow(float(userdata[name2]["neuroticism"]), 2)
    )/math.sqrt(10)/5
    return(distance1+distance2)

def findMatches(name):
    metrics = []
    for attribute in userdata:
        if attribute == name:
            continue
        dist = calculateDistances(name, attribute)
        metrics.append({"name": attribute, "distance": dist})
    metrics.sort(key= lambda x: x["distance"])
    return(metrics)
    

@app.route('/woof/<string:name>/', methods=['GET'])
def welcome(name):
    name = name.lower()
    for attribute in userdata:
        calculatePersonalities(attribute)
    return ("Woof Woof " + name)


@app.route('/getuser/<string:name>/', methods=['GET'])
def getuser(name):
    name = name.lower()
    return json.dumps(userdata[name])


@app.route('/setuser/<string:name>/', methods=['POST'])
def postuser(name):
    name = name.lower()
    requestdata = request.json
    userdata[name] = requestdata
    calculatePersonalities(name)
    return "User creation successfull"


@app.route('/getprofiles/', methods=['GET'])
def getprofiles():
    return json.dumps(userdata)


@app.route('/getmatches/<string:name>/', methods=['GET'])
def getmatches(name):
    name = name.lower()
    metrics = findMatches(name)
    matches = []
    for metric in metrics:
        temp = userdata[metric["name"]]
        temp["name"] = metric["name"]
        temp["compatibility"] = metric["distance"]
        matches.append(userdata[metric["name"]])
    return json.dumps(matches)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
