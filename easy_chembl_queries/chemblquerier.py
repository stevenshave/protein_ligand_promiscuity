from pathlib import Path
import sqlite3
from sqlite3 import Error


class ChEMBLQuerier:
    """ChEMBLQuerier, simple interface to SQLite version of ChEMBL


    Developed on ChEMBL v27
    Returns:
        ChEMBLQuerier: Easy querying of ChEMBL
    """

    conn = None
    cur = None

    def __init__(self, sqlite_file: [Path, str]):
        if isinstance(sqlite_file, str):
            sqlite_file = Path(sqlite_file)
        sqlite_file = sqlite_file.expanduser()
        assert sqlite_file.exists(), "SQL file does not exist"
        try:
            self.conn = sqlite3.connect(str(sqlite_file))
            self.cur = self.conn.cursor()
            print("Connected to ", str(sqlite_file))
        except Error as e:
            print(e)

    def query(self, query: str):
        try:
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
        except Error as e:
            print(e)



    def get_human_proteins(
        self,
        single_protein=True,
        protein=True,
        protein_protein_interaction=True,
        protein_family=True,
    ):
        assert any(
            [single_protein, protein, protein_protein_interaction, protein_family]
        ), "No target_type specified"
        allowed_target_types = []
        if single_protein:
            allowed_target_types.append("'SINGLE PROTEIN'")
        if protein:
            allowed_target_types.append("'PROTEIN'")
        if protein_protein_interaction:
            allowed_target_types.append("'PROTEIN-PROTEIN INTERACTION'")
        if protein_family:
            allowed_target_types.append("'PROTEIN FAMILY'")

        allowed_target_types_str = ",".join(allowed_target_types)
        query = (
            "select CHEMBL_ID, PREF_NAME from target_dictionary where organism='Homo sapiens' and target_type in ("
            + allowed_target_types_str
            + ")"
        )
        return self.query(query)


    def get_cpds_active_against_chemblid_target_list(self, chembl_ids_list, std_val_cutoff=10000,standard_types="'Inhibition', 'IC50','Kd', 'Ac50','IC90', 'EC50'",standard_relations="'<','<=','='"):
        """Get all compounds recorded as active against proteins in a list

        Args:
            chembl_ids_list ([str]): list of ChEMBL IDS of targets
            std_val_cutoff (int, optional): Standard value cutoff in nM. Defaults to 10000.
            standard_types (str, optional): Comma separated, quote delimited list of activity types to consider. Defaults to "'Inhibition', 'IC50','Kd', 'Ac50','IC90', 'EC50'".
            standard_relations (str, optional): Comma separated, quote delimited list of relations.  Basically we want <= std_val_cutoff. Defaults to "'<','<=','='".
        """        
        
        # SQLite seems extremely slow at running deeply nested queies.  Trials showed it was much more efficient to perform it in steps rather than one big long query

        chembl_ids_str=",".join("'"+t+"'" for t in chembl_ids_list)
        activities_string=f"STANDARD_VALUE<={std_val_cutoff} and STANDARD_TYPE in ({standard_types}) and STANDARD_RELATION in ({standard_relations})"
        
        assay_ids=self.query(f"select assay_id from assays where tid in (select tid from target_dictionary where chembl_id in ({chembl_ids_str}))")
        assay_ids=[str(a[0]) for a in assay_ids]
        
        activity_ids=self.query("select molregno from activities where assay_id in ("+",".join("'"+t+"'" for t in assay_ids)+f") and {activities_string}")
        print("select molregno from activities where assay_id in ("+",".join(t for t in assay_ids)+f") and {activities_string}")
        
        print("select chembl_id from molecule_dictionary where molregno in (select molregno from activities where assay_id in ("+",".join("'"+assay_id+"'" for assay_id in activity_ids)+")")
        print(activity_ids)
        cpd_chembl_ids=self.query("select chembl_id from molecule_dictionary where molregno in (select molregno from activities where assay_id in ("+",".join("'"+str(assay_id)+"'" for assay_id in assay_ids)+")")
        return cpd_chembl_ids        
        #query_str=f"select chembl_id from molecule_dictionary where molregno in (select molregno from activities where assay_id in (select assay_id from assays where tid in (select tid from target_dictionary where chembl_id in ({chembl_ids_str})) and {activities_string}  ) )"
        #print(query_str)
        #print(self.query(query_str))
        #return assay_ids


    def __del__(self):
        if self.conn:
            self.conn.close()
