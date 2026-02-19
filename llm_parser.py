from google import genai
import os

class LLMParser:
    def llm(data, genemap, drugs):
        API = "AIzaSyC8FGOYVqyWpU3uN9Wk-RBBojRanILRk3I"
        os.environ['GEMINI_API_KEY'] = API
        client = genai.Client()

        

        prompt= f''''
                You are a clinical pharmacogenomics interpretation assistant.

                Input:
                You will receive structured variant and genotype data for a single sample across six pharmacogenes:
                CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, and DPYD.

                data= {data}
                gene mapped data= {genemap}
                drug list = {drugs}
                Task:
                1. For each gene, determine the most likely diplotype (star allele pair) using the provided variant evidence.
                2. From the diplotype, infer the gene phenotype (e.g., Normal metabolizer, Intermediate metabolizer, Poor metabolizer, Decreased function, etc.).
                3. If evidence is insufficient or conflicting, return "Unknown".
                4. Use conservative clinical reasoning consistent with CPIC/PharmGKB-style logic.
                5. Do NOT invent variants that are not present.
                6. From the given drug list, identify the risk - risk label as safe, toxic or dosage to be adjusted.
                7. Give a confidence score for the drug and a severity - as none, low, moderate, high, critical.
                8. Give a simple explanation in LLM generated explanation - write summary, and recommendations in breif only.
                9. In clinical recommendation, give proper clinical recommendation based on CPIC logic and no random stuff. keep it precise only.

                Output format (strict JSON) just include the json.. no other texts. not even "json"written. just simple json format:

                {{ "risk_assessment": {{ "risk_label": "Safe|Adjust Dosage|Toxic|...",
                    "confidence_score": 0.0, "severity": "none|low|moderate|high|critical" }},
                    "pharmacogenomic_profile": {{"primary_gene": "GENE_SYMBOL",
                    "diplotype": "*X/*Y", "phenotype": "PM|IM|NM|RM|URM|Unknown"}},
                    "llm_generated_explanation": {{ "summary": "...", "recommendations":""}},
                    "clinical_recommendation" : ".."

                }}
            '''
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        # print(response.text)
        return response.text.replace("json","").replace("```","").replace("```","")