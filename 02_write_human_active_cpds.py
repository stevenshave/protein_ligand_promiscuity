"""Generate list of human proteins and their ecnumbers


"""

from pathlib import Path
from easy_chembl_queries import *
import json

# Define the 3 easy queriers - one for ChEMBL (reading SQLite ChEMBLv27)
# one to read a chembl -> uniprot id mapping
# and a final one to query the uniprot web service and retrieve EC numbers.

chembl=chemblquerier.ChEMBLQuerier(Path("d:\chembl_27.db"))

print("Getting human protein chemblids")
human_protein_chemblids=[p[0] for p in chembl.get_human_proteins()]
print("Got", len(human_protein_chemblids), "human protein ids")

molregnumbers=chembl.get_cpds_molreg_active_against_chemblid_target_list([str(cid) for cid in human_protein_chemblids])
smiles_molreg_list=chembl.get_smiles_for_molregs(molregnumbers)

json.dump(smiles_molreg_list, open("dat_active_smiles_with_molreg.json", "w"))



