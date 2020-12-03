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

        finally:
            print("Closing connection")
            if self.conn:
                self.conn.close()

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

    def __del__(self):
        if self.conn:
            self.conn.close()
