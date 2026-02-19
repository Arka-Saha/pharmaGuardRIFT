from pathlib import Path
# from math
import math
import gzip
import pandas as pd
# from cyvcf2 import VCF

class VCFParse:

    def parse(file_path):
        fields = []
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("##"):
                    pass
                elif line.startswith("#CHROM"):
                    header = line.split(" ")
                    names= []
                    for h in header: 
                        if h!='':
                            h=h.replace("\n","") 
                            names.append(h)
                    sample_names = names[9:]
                else:
                    field_final = []

                    field = line.split(" ")
                    for f in field: 
                        if f!='': field_final.append(f)
                    # sample_names = names[9:]
                    fields.append(field_final)
# ['20', '14370', 'rs6054257', 'G', 'A', '29', 'PASS', 'NS=3;DP=14;AF=0.5;DB;H2', 'GT:GQ:DP:HQ', '0|0:48:1:51,51', '1|0:48:8:51,51', '1/1:43:5:.,.\n']
                field_dicts = []
                for each in fields:
                    values = []
                    for val in each[9:]:
                        val_list = val.split(":")
                        values.append(val_list)

                    temp_dict = {
                        "chromosome": each[0],
                        "position": each[1],
                        "variant_id": each[2],
                        "reference_allele": each[3],
                        "alternate_allele": each[4].replace("\n","").split(","),
                        "quality_score" : each[5],
                        "filter_status": each[6],
                        "info": {k: (v if v else True) for part in each[7].split(';') for k, v in [part.split('=') if '=' in part else (part, True)]},
                        "format": each[8],
                        "samples":dict(zip(sample_names, values))   

                    }

                    field_dicts.append(temp_dict)
                    # print(temp_dict)
        return field_dicts
        # print(len(field_dicts), end="\n")
        
    def validate(file_path):
        success = False
        file_path = Path(file_path)
        extension = file_path.suffix
        size_bytes = file_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        # success = False
        if int(size_mb) > 5: success = False
        else: 
            if extension == ".vcf": 
                success= True
        header_check = False
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("##"):
                    pass
                elif line.startswith("#CHROM"):
                    header_check = True
                else: pass
        output = {
            "vcf_parsing_success": success,
            "extension": extension,
            "file_size": size_mb,
            "header": header_check
        }
        return output

    def gene_match(data):
        filtered_variant = {}

        PGX_GENES = {
            "CYP2D6":  {"chrom": "22", "start": 42126499, "end": 42130865},
            "CYP2C19": {"chrom": "10", "start": 96521600, "end": 96614400},
            "CYP2C9":  {"chrom": "10", "start": 96600000, "end": 96652000},
            "SLCO1B1": {"chrom": "12", "start": 21140000, "end": 21220000},
            "TPMT":    {"chrom": "6",  "start": 18130000, "end": 18137000},
            "DPYD":    {"chrom": "1",  "start": 97770000, "end": 98350000},
        }

        genes = ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]
        chrom = [22, 10, 10, 12, 6, 1]

        length = len(data)

        g = "NULL"

        for i in range(length):
            for j in genes:
                if str(data[i].get("chromosome")) == str(PGX_GENES[j]["chrom"]):
                    g = j
                    # print(j)
            filtered_variant.update({data[i]['variant_id']:g})

        # print(filtered_variant)
        return filtered_variant
