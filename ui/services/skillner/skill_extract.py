import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
nlp = spacy.load("en_core_web_lg")
# init skill extractor
skill_extractor_instance = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

def extract_skills(content):
    try:
        annotations = skill_extractor_instance.annotate(content)
        skill_list = [skill["doc_node_value"] for skill in annotations["results"]["full_matches"]]
        skill_list.extend([skill["doc_node_value"] for skill in annotations["results"]["ngram_scored"]])
        return skill_list
    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    