"""Generate list of human proteins and their docstrings.


"""

from pathlib import Path
from easy_chembl_queries import *

# Define the 3 easy queriers - one for ChEMBL (reading SQLite ChEMBLv27)
# one to read a chembl -> uniprot id mapping
# and a final one to query the uniprot web service and retrieve EC numbers.

chembl=chemblquerier.ChEMBLQuerier(Path("/home/stevens/data/chembl_27.db"))
uniprot_mapper=ChEMBLIDtoUniprotMapper("~/data/chembl_27_uniprot_mapping.txt")
uniprot_web=UniProtWebQuerier()


human_proteins=chembl.get_human_proteins()
human_proteins_with_uniprotids=[[p[0], p[1], uniprot_mapper.query_chemblid(p[0]), uniprot_web.uniprotid_to_ecnumber(uniprot_mapper.query_chemblid(p[0]))] for p in human_proteins]


print(human_proteins_with_uniprotids)