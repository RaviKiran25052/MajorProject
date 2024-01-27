from langdetect import detect,detect_langs

op = detect_langs("ఉద్యమాలు - a group of people")

languages = [lang.lang for lang in op]
print(languages)


from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

mykey = "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"
model = OpenAI(temperature=0, openai_api_key=mykey)

prompt = PromptTemplate(
   template = "give the text in {x} by summarizing it within 30 words. text: {y}.",
   input_variables = ["x", "y"]
)

# query = prompt.format(x="english", y="The freedom fighter who fought for the people's rights with his actions, Gandhiji, is a leader of people's movements. He strongly advocated for the dignity of life and said that Telugu people should be self-reliant in their country. We remember Gandhiji's sacrifice and pray to the Almighty for peace and prosperity in his memory. We also express our deep gratitude to the members of his family and the people of Nandamuri Balakrishna Pattl Gaddar.")
query = prompt.format(x="telugu", y="దీపావళిపై విద్యార్థులకు ప్రసంగం: మనందరి జీవితాల్లో దీపావళి పండుగకు ప్రత్యేక ప్రాముఖ్యత ఉంది. దీపావళి అంటే వెలుగుల పండుగ, కానీ నేటికి దశాబ్దాలుగా మనం ఈ రోజును పటాకులు కాల్చి జరుపుకుంటున్నాం. పటాకులు వాయు కాలుష్యాన్ని మాత్రమే కాకుండా శబ్ద కాలుష్యాన్ని కూడా కలిగిస్తాయి.వాయు కాలుష్యం ఎక్కువగా ఉన్న ప్రపంచంలోని కొన్ని అగ్ర దేశాల జాబితాను తయారు చేస్తే, మొదటి ఐదు నగరాలు భారతదేశంలోనే ఉన్నాయి. చిన్న పిల్లలు, జంతువులు, రోగులు మొదలైనవారు దీని బారిన పడుతున్నారు.కాబట్టి ఈసారి దీపావళిని దీపాల అలంకరణతో జరుపుకుంటామని, ఎలాంటి కాలుష్యం వ్యాపించబోమని ప్రతిజ్ఞ చేయండి. హిందీకిదునియా కామ్ మెరుగుపరుస్తుంది కానీ చాలా ఇతరులు")
translated_text = model(prompt=query)

print(translated_text)


# Split the sentence into words
words = translated_text.split()

# Count the number of words
word_count = len(words)

print("Word count:", word_count)