from nrclex import NRCLex
from personality_detection_essay.predict import predict_personality

def predictPetPersonality(adjectives):
    text_object = NRCLex(adjectives)
    # print(text_object.raw_emotion_scores)
    # print(text_object.top_emotions)
    return(text_object.affect_frequencies)

def predictHumanPersonality(essay):
    return(predict_personality(essay))
    

if __name__ == '__main__':
    print(predictPetPersonality("cuddly, loving, caring, curious, lively, confident, talkative, food, motivated, personable"))
    print(predictPetPersonality("cuddly, loving, caring, nervous, lively, shy, timid, food, motivated, personable"))
    print(predictPetPersonality("cuddly, loving, curious, lively, timid, hide, food, motivated, impersonable"))
    print(predictPetPersonality("aggressive, loving, caring, apathy, lively, confident, talkative, food, motivated, attack"))
    print(predictPetPersonality("skiddish, loving, apathetic, lively, timid, quiet, food, unmotivated, distant"))
    print(predictHumanPersonality("We cuddle in the bathtub, Not with the water obviously, because cats and water is definitely not a fun thing, but sometimes he'll jump in the tub, and i'll scoot in beside him and we'll just lay there, him on my chest, and have some time together. And it's our time. And it sounds so weird writing that, because actually it is weird, but we'll still keep doing it."))
    print(predictHumanPersonality("Yes really. I love when I'm dozing off to sleep, and he thumps onto the bed, and wants to get under the covers for a little snuggle. Those precious moments can't be disrupted with - whatever time of night."))
    print(predictHumanPersonality("We've lost 700,000 Americans now and fully 200,000 of those folks have died since vaccines have been available almost to everyone in this country, and every one of those deaths is unnecessary. So even though the news is great for this antiviral agent, really the message that people need to receive is \'get vaccinated.\' No one needs to die from this virus, he said."))