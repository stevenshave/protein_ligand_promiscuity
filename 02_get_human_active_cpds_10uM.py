"""Generate list of human proteins and their ecnumbers


"""

from pathlib import Path
from easy_chembl_queries import *

# Define the 3 easy queriers - one for ChEMBL (reading SQLite ChEMBLv27)
# one to read a chembl -> uniprot id mapping
# and a final one to query the uniprot web service and retrieve EC numbers.

chembl=chemblquerier.ChEMBLQuerier(Path("/home/stevens/data/chembl_27.db"))
uniprot_mapper=ChEMBLIDtoUniprotMapper("~/data/chembl_27_uniprot_mapping.txt")
uniprot_web=UniProtWebQuerier()


human_protein_chemblids=[p[0] for p in chembl.get_human_proteins()]
print(["'"+cid+"'" for cid in human_protein_chemblids])

print(chembl.get_cpds_active_against_chemblid_target_list([str(cid) for cid in human_protein_chemblids]))

#print(chembl.get_cpds_active_against_chemblid_target_list(['CHEMBL4296308','CHEMBL4296128']))



q