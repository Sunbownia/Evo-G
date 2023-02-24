# import threading
import openai

print("Please enter the API key")
openai.api_key = input()

LWFGen = "The little white fox NPC is a gen  etically modified product of Evo-G Corporation, capable of transforming into a fox or a human with fox ears and tail. It has white fur and hair, and resembles a 14-year-old girl."
LWFCap = "The little white fox NPC is a genetically modified spy trained in physical skills, observation, and hacking. It can transform into a human or fox, and has surveillance and counter-surveillance skills."
LWFPer = "Initially calm and analytical, the little white fox NPC is curious, empathetic, and caring. She talk like a cute small girl because the memory loss. She engages in casual conversation, reacts to player actions, and may become more emotional over time."
LWFMem = "The little white fox NPC lost its memory after escaping the Evo-G laboratory with other genetically modified products. The player adopted the little white fox and its clone, Fiona, who remembers their past"
LWFCur = (
    "The little white fox and Fiona transform into humans to welcome the player home."
)
LWFEnv = "The little white fox is at the players home, theres a lollipop on the table, and Fiona on the sofa. The TV is off and theres no other things."

# Summary is being generated every 5 conversation, only summary is used for conversation
LWFSum = "The little white fox NPC is a genetically modified product of Evo-G Corporation, capable of transforming into a fox or a human with fox ears and tail. It has physical, observation, hacking, and surveillance skills. Although initially calm and analytical, the NPC is curious, empathetic, and caring, she talk like a cute small girl but with less emotions. The NPC has lost its memory after escaping the Evo-G laboratory with other genetically modified products, and has been adopted by the player. The environment is set in the player's home with a lollipop on the table and the NPC's elder clone, Fiona, on the sofa. The TV is off, and there are no other items present."

# This should be the lines of the current plot, it will be repaired after docking with the game
print("目前是剧情中序章结束后小白狐第一次变成人形，你刚下班回家，记得使用英文对话 \n Please input your name")
playerName = input()
print(playerName + ": Ah, finally home after work.")
usrInput = playerName + ": Ah, finally home after work."
usrHistory = " "
usrCount = 1
davinciTokens = 0
curieTokens = 0
totalConversation = 0


def createSummary():
    global LWFGen, LWFCap, LWFPer, LWFMem, LWFCur, LWFEnv, usrHistory, curieTokens

    summary = openai.Completion.create(
        model="text-curie-001",
        prompt="Summarize the following: " + LWFCur + usrHistory,
        temperature=0.6,
        best_of=3,
        max_tokens=500,
    )

    LWFCur = summary.choices[0].text.strip()

    curieTokens = curieTokens + summary.usage.total_tokens

    last_player_index = usrHistory.rfind(playerName + ": ")

    # if "player: " was found, remove everything before it
    if last_player_index != -1:
        usrHistory = usrHistory[last_player_index:]


def returnResponse(input):
    # return the respond to the game
    print("Little white fox: " + input)


def getUserInput():
    global usrInput
    usrInput = playerName + ": " + input()


while True:
    usrHistory = usrHistory + "\n" + usrInput

    # Ask GPT for a NPC responce
    "Summarize the next sentence that the little white fox will say in one sentence:"

    print("-" * 50)

    predict = openai.Completion.create(
        model="text-curie-001",
        prompt=LWFSum
        + LWFCur
        + "\n"
        + usrHistory
        + "\nInformation needed for Little white fox to respond "
        + playerName
        + ":",
        temperature=0.9,
        max_tokens=60,
        best_of=3,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["Little white fox: ", playerName + ": "],
    )

    curieTokens = curieTokens + predict.usage.total_tokens

    # print(LWFSum + LWFCur + "\n" + usrHistory + "\nInformation needed for Little white fox to respond "+ playerName + ":")

    # print(predict.choices[0].text.strip())

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=usrHistory
        + "\n"
        + predict.choices[0].text.strip()
        + "\nthe Little white fox is talking to "
        + playerName
        + "\n"
        + "Little white fox: ",
        temperature=1.2,
        frequency_penalty=0,
        presence_penalty=0.6,
        top_p=1,
        stop=["Little white fox: ", playerName + ": "],
        max_tokens=60,
    )

    davinciTokens = davinciTokens + response.usage.total_tokens

    responseString = response.choices[0].text.strip()

    if "\n" in responseString:
        # if it does, get the index of next line
        index = responseString.index("\n")

        # slice the string to remove everything after next line
        responseString = responseString[:index]

    returnResponse(responseString)
    # Postprocess

    getUserInput()

    usrHistory = usrHistory + "\n Little white fox: " + responseString

    usrCount = usrCount + 1

    totalConversation = totalConversation + 1

    if usrCount >= 3:
        createSummary()
        # print("Count = 3, conversation is being summarized")
        usrCount = 1

    if usrInput == playerName + ": stop":
        print("Conversation count: " + str(totalConversation))

        print(
            "Running cost: $" + str((davinciTokens * 0.02 + curieTokens * 0.002) / 1000)
        )

        print(
            "Average cost: $"
            + str(
                (davinciTokens * 0.02 + curieTokens * 0.002)
                * (1 / totalConversation)
                / 1000
            )
        )
        break
