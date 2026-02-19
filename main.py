from vcf_parser import VCFParse
# import streamlit as st
from llm_parser import LLMParser
import json, datetime

import debug

llmparse = LLMParser
parser = VCFParse

drugs = ["CODEINE", "WARFARIN"]

##
debug_status = True
##
patient_id = 10

if debug_status:
    for i in range(len(drugs)):
        print(debug.outputs[i])
else:
    for drug in drugs:
        parsed = parser.parse('meow.vcf')
        gene_match = parser.gene_match(parser.parse("meow.vcf"))
        llm_output = LLMParser.llm(parser.parse('meow.vcf'),parser.gene_match(parser.parse("meow.vcf")), drug)
        # llm_output.replace('json','')
        # print(llm_output)
        j = json.loads(llm_output)
        d = j['pharmacogenomic_profile']
        d['detected_variants'] = [ gene_match ]
        output = { "patient_id": f"PATIENT {patient_id}",
            "drug": drug,
            "timestamp": str(datetime.datetime.now()).replace("-", "").replace(".","").replace(" ", ""),
            "risk_assessment": j['risk_assessment'],
            "pharmacogenomic_profile": d,
            "clinical_recommendation": j['clinical_recommendation'],
            "llm_generated_explanation": j['llm_generated_explanation'],
            "quality_metrics": VCFParse.validate("meow.vcf")
            }

        print(output)